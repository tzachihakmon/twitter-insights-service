from flask import Flask, request, jsonify
from datetime import datetime
from flask import Flask, request, jsonify
from TopicRepositoryModule import TopicsRepository, Topic 

app = Flask(__name__)
repo = TopicsRepository()

@app.route('/repotopics/insert_topics', methods=['POST'])
def insert_topics():
    topics_data = request.json
    topics = [Topic(**data) for data in topics_data]
    repo.insert_topics(topics)
    return jsonify({"message": "Topics inserted successfully"}), 200

@app.route('/repotopics/get_topics_by_month', methods=['GET'])
def get_topics_by_month():
    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    start_day = int(request.args.get('start_day'))
    end_day = int(request.args.get('end_day'))
    data = repo.get_topics_by_month(year, month, start_day, end_day)
    return jsonify(data), 200
    # Example JSON response:
    # [{"topic": "example", "author": "author_name", "likes": 100, "shares": 50}]

@app.route('/repotopics/get_single_topic_trend', methods=['GET'])
def get_single_topic_trend():
    year = int(request.args.get('year'))
    topic = request.args.get('topic')
    data = repo.get_single_topic_trend(year, topic)
    return jsonify(data), 200
    # Example JSON response:
    # [{"topic": "example", "month": 1, "author": "author_name", "likes": 100, "shares": 50}]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)