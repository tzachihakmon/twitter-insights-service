from flask import Flask, request, jsonify
from datetime import datetime
from TrendsEngineModule import TopicsTrendsEngine

app = Flask(__name__)
engine = TopicsTrendsEngine()

@app.route('/get_k_topics_by_date', methods=['GET'])
def get_k_topics_by_date():
    # Extracting query parameters
    k = request.args.get('k')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    # Basic input validation
    if not k or not start_date_str or not end_date_str:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        k = int(k)
        # Validating and converting date strings to date objects
        start_date = datetime.strptime(start_date_str, "%Y%m%d").date()
        end_date = datetime.strptime(end_date_str, "%Y%m%d").date()

        if start_date > end_date:
            raise ValueError("start_date cannot be after end_date")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Call to the TopicsTrendsEngine with validated and converted parameters
    try:
        print(f"Calling get_k_most_trend_topics with k:{k} start:{start_date} end:{end_date}")
        top_k_topics = engine.get_k_most_trend_topics(k, start_date, end_date)
        print(f"got K trended topics: {top_k_topics}")
        top_k_topics_serializable = [vars(topic) for topic in top_k_topics]
        return jsonify(top_k_topics_serializable)
    except Exception as e:
        return jsonify({"error": f"internal: Failed to fetch topics: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)