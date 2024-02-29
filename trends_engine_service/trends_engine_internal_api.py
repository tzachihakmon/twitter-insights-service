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

    k = int(k)
    start_date = datetime.strptime(start_date_str, "%Y%m%d").date()
    end_date = datetime.strptime(end_date_str, "%Y%m%d").date()

    # Call to the TopicsTrendsEngine with validated and converted parameters
    try:
        print(f"Calling get_k_most_trend_topics with k:{k} start:{start_date} end:{end_date}")
        top_k_topics = engine.get_k_most_trend_topics(k, start_date, end_date)
        print(f"got K trended topics: {top_k_topics}")
        top_k_topics_serializable = [vars(topic) for topic in top_k_topics]
        return jsonify(top_k_topics_serializable)
    except Exception as e:
        return jsonify({"error": f"internal: Failed to fetch topics: {e}"}), 500
    
@app.route('/get_topic_trend', methods=['GET'])
def get_topic_trend_year():
    # Extracting query parameters
    topic = request.args.get('topic')
    year = int(request.args.get('year'))

    # Call to the TopicsTrendsEngine with validated and converted parameters
    try:
        print(f"Calling to get topic: {topic} ternd over year: {year}")
        topic_stats = engine.get_topic_trend_by_year(topic, year)
        print(f"got month topic_stats of year: {year} for topic {topic}")
        #topic_stats_serializable = [vars(topic) for topic in topic_stats]
        return jsonify(topic_stats)
    except Exception as e:
        print(e)
        return jsonify({"error": f"internal: Failed to fetch topic stats for topc:{topic} in year: {year}: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)