from flask import Flask, request, jsonify
from TopicRepositoryModule import TopicsRepository  # Adjust the import statement based on your actual module name and location
from datetime import datetime
import requests

app = Flask(__name__)
topics_repository = TopicsRepository()

@app.route('/hello_world', methods=['GET'])
def hello_world():
    return 'Hello, World!'


@app.route('/topics/<topic>', methods=['GET'])
def get_topic_appearances(topic):
    year = request.args.get('year')
    start_month = request.args.get('startmonth')
    end_month = request.args.get('endmonth')
    print(f"Got request with: year:{year} start_month:{start_month} end_month:{end_month}")
    if not all([year, start_month, end_month]):
        return jsonify({"error": "Missing query parameters: year, startmonth, and/or endmonth are required."}), 400

    try:
        # Convert parameters to integers for the database query
        year = int(year)
        start_month = int(start_month)
        end_month = int(end_month)
    except ValueError:
        return jsonify({"error": "Query parameters year, startmonth, and endmonth must be integers."}), 400

    data = topics_repository.get_all_topics_appearences(topic, year, start_month, end_month)
    return jsonify(data)

@app.route('/get_k_topics_by_date', methods=['GET'])
def get_k_topics_by_date():
    # Extracting query parameters
    k = request.args.get('k')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    # Basic input validation
    if not k or not start_date_str or not end_date_str:
        return jsonify({"error": "Missing required parameters"}), 400

    start_date =""
    end_date = ""
    try:
        k = int(k)
        # Validating and converting date strings to date objects
        start_date = datetime.strptime(start_date_str, "%Y%m%d").date()
        end_date = datetime.strptime(end_date_str, "%Y%m%d").date()

        if start_date > end_date:
            raise ValueError("start_date cannot be after end_date")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    try:
        url = 'http://trends-engine-service:5001/get_k_topics_by_date'  # Adjust the URL based on your setup
        print(k, start_date.strftime("%Y%m%d"),end_date.strftime("%Y%m%d"))
        params = {
            'k': k,
            'start_date': start_date.strftime("%Y%m%d"),
            'end_date': end_date.strftime("%Y%m%d")
        }
        print(f"out going request to: {url} with params: {params}")
        response = requests.get(url, params=params)
        response_code = response.status_code
        return response.json(), response_code
    except Exception as e:
        return jsonify({"error": f"public: Failed to fetch topics: {e}"}), 500

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)