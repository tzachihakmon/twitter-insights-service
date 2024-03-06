from dateutil.parser import parse
import spacy
import re
from TweetsRepositoryModule import TweetsRepository
import requests
from TopicRepositoryModule import Topic
import os

nlp = spacy.load("en_core_web_sm")
TOPICS_REPOSITORY_SERVICE_NAME = os.getenv("topic_repository_service_name", "topic-repository-service")
TOPICS_REPOSITORY_SERVICE_PORT = os.getenv("topic_repository_servce_port", "5002")

def extract_topics_from_tweet(content):
    doc = nlp(content)
    topics_from_spacy_list = [ent.text.lower() for ent in doc.ents if  len(ent.text.strip()) > 1]
    topics_from_spacy_list = [topic[1:] if topic.startswith(('@', '#')) else topic for topic in topics_from_spacy_list]
    
    hashtag_regex = r'#(\w+)'
    mention_regex = r'@(\w+)'
    hashtags = re.findall(hashtag_regex, content)
    mentions = re.findall(mention_regex, content)

    for entity in hashtags + mentions:
        entity = entity.lower()
        if entity not in topics_from_spacy_list:
            topics_from_spacy_list.append(entity)

    return topics_from_spacy_list


def get_topics(tweet):
    # Extract date and time components
    topics_string = extract_topics_from_tweet(tweet.content)
    topics_objects = []
    for topic_string in topics_string:
        topics_objects.append(Topic(
            year = tweet.year,
            month = tweet.month,
            day = tweet.day,
            hour = tweet.hour,
            minute = tweet.minute,
            topic = topic_string,
            author = tweet.author,
            likes = int(tweet.likes),
            shares = int(tweet.shares)
        ))
    return topics_objects

def PopulateCassandraTopicsTables():
    tweets_repo = TweetsRepository()
    i = 0
    distinct_topics = set()
    inserted = 0
    for tweet in tweets_repo.get_tweets():
        topics = get_topics(tweet)
        insert_topics(topics)
        for topic in topics:
            distinct_topics.add(topic.topic)
        inserted += len(topics)
        if (i%1000==0):
            print(f"{i} tweets proceed. Number of distinct topics: {len(distinct_topics)}. Number of inserted topics: {inserted}")
        i+=1

def insert_topics(topics):
    try:
        if(len(topics) != 0):
            url = f'http://{TOPICS_REPOSITORY_SERVICE_NAME}:{TOPICS_REPOSITORY_SERVICE_PORT}/repotopics/insert_topics'  # Adjust the URL based on your setup
            topics_dicts = [t.__dict__ for t in topics]
            requests.post(url, json=topics_dicts)
    except Exception as ex:
        print(f"Failed to publish topics to repo. Topics: {topics}, topics dict:{topics_dicts} ex: {ex}")

def main():
    PopulateCassandraTopicsTables()

if __name__ == '__main__':
    main()