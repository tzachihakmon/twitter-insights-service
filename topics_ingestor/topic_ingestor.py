from dateutil.parser import parse
import spacy
import re
from TweetsRepositoryModule import TweetsRepository
from TopicRepositoryModule import Topic
from TopicRepositoryModule import TopicsRepository

nlp = spacy.load("en_core_web_sm")

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
    topic_repo = TopicsRepository()
    i = 0
    distinct_topics = set()
    inserted = 0
    for tweet in tweets_repo.get_tweets():
        topics = get_topics(tweet)
        topic_repo.insert_topics(topics)
        for topic in topics:
            distinct_topics.add(topic.topic)
        inserted += len(topics)
        if (i%1000==0):
            print(f"{i} tweets proceed. Number of distinct topics: {len(distinct_topics)}. Number of inserted topics: {inserted}")
        i+=1

def main():
    PopulateCassandraTopicsTables()

if __name__ == '__main__':
    main()