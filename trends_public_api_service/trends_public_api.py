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
    print(f"Got topic trend request with: year:{year} for topic:{topic}.")
    if not all([year, topic]):
        return jsonify({"error": "Missing query parameters: year, startmonth, and/or endmonth are required."}), 400

    try:
        year = int(year)
    except ValueError:
        return jsonify({"error": "Query parameter year must be integer."}), 400

    try:
        url = 'http://trends-engine-service:5001/get_topic_trend'  # Adjust the URL based on your setup
        params = {
            'topic': topic,
            'year': year,
        }
        print(f"out going request to: {url} with params: {params}")
        response = requests.get(url, params=params)
        
        # Extract only the trend_score from each topic stats
        topic_stats = response.json()
        trend_scores_only = [{'topic': ts['topic'], 'trend_score': ts['trend_score']} for ts in topic_stats]
        
        return jsonify(trend_scores_only), 200
    
    except Exception as e:
        return jsonify({"error": f"public: Failed to fetch topics: {e}"}), 500

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