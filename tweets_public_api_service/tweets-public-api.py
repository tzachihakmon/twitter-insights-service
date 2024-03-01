from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/tweets', methods=['POST'])
def post_tweet():
    tweet = request.json.get('tweet', '')
    char_limit = int(os.getenv('TWEET_CHAR_LIMIT', 280))
    
    if len(tweet) > char_limit:
        return jsonify({"error": f"Tweet exceeds the maximum allowed length of {char_limit} characters."}), 400
    
    return jsonify({"message": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)