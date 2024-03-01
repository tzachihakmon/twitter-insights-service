from dataclasses import dataclass , field
from datetime import datetime, timedelta
import requests
import os

exclude_phrases_str = os.getenv("exclude_phrases", "")
EXCLUDE_PHRASES = set(exclude_phrases_str.split(",")) if exclude_phrases_str != "" else {"twitter", "midnight", "10","two", "second", "night","friday", "morning", "first", "sunday", "thursday", "summer","saturday","monday", "1st", "today", "tonight", "one", "less than 24 hours", "tbt", "the day","1", "month of the year", "next week", "last day","one day", "this week","the week", "next year", "this year", "the year", "last night's" ,"last night", "all day","every day", "tomorrow", "yesterday","weekend", "the weekend", "this weekend","everyday" ,"last night","last week", "last year", "this day"}
TOPICS_REPOSITORY_SERVICE_NAME = os.getenv("topic_repository_service_name", "topic-repository-service")
TOPICS_REPOSITORY_SERVICE_PORT = os.getenv("topic_repository_servce_port", "5002")
share_score_factor = int(os.getenv("share_score_factor", "0.35"))
like_score_factor = int(os.getenv("like_score_factor", "0.05"))
frequency_score_factor = int(os.getenv("frequency_score_factor", "0.20"))
author_frequency_score = int(os.getenv("author_frequency_score", "0.40"))

@dataclass
class TopicStats:
    topic: str
    total_tweets: int = 0
    total_shares: int = 0
    total_likes: int = 0
    distinct_authors: set = field(default_factory=set)

    def add_tweet(self, author, likes, shares):
        self.total_tweets += 1
        self.total_shares += shares
        self.total_likes += likes
        self.distinct_authors.add(author)

@dataclass
class TopicScore:
    topic: str
    total_tweets: int = 0
    total_shares: int = 0
    total_likes: int = 0 
    distinct_authors: int = 0
    share_score: float = 0
    like_score: float = 0
    frequency_score: float= 0
    author_frequency_score: float= 0
    trend_score: float= 0

class TopicsTrendsEngine:
    def get_k_most_trend_topics(self, k, start_date, end_date):
        all_topics_stats = self._aggregate_topic_stats(start_date, end_date)
        # Calculate scores and sort
        most_shares = max(stats.total_shares for stats in all_topics_stats.values())
        most_likes = max(stats.total_likes for stats in all_topics_stats.values())
        most_frequent = max(stats.total_tweets for stats in all_topics_stats.values())
        most_distinct_authors = max(len(stats.distinct_authors) for stats in all_topics_stats.values())

        top_k_topics = []
        for stats in all_topics_stats.values():
            topic_score_object = self._create_topic_score_object(most_shares, most_likes, most_frequent, most_distinct_authors, stats)
            top_k_topics.append(topic_score_object)
        # Sort topics by trend score and return top k
        top_k_topics = sorted(top_k_topics, key=lambda x: x.trend_score, reverse=True)[:k]
        return top_k_topics

    def get_topic_trend_by_year(self, topic, year):
        topic_appearences_by_months = {i : TopicStats(topic = topic) for i in range (1,13)}
        topic_appearences = self.get_topic_appearances(topic, year)
        for appearence in topic_appearences:
            print(appearence)
            month = int(appearence['month'])
            topic_appearences_by_months[month].add_tweet(appearence['author'], appearence['likes'], appearence['shares'])
        
        most_shares = max(stats.total_shares for stats in topic_appearences_by_months.values())
        most_likes = max(stats.total_likes for stats in topic_appearences_by_months.values())
        most_frequent = max(stats.total_tweets for stats in topic_appearences_by_months.values())
        most_distinct_authors = max(len(stats.distinct_authors) for stats in topic_appearences_by_months.values())
        
        months_to_topic_score = {}
        for month in range(1,13):
            month_stats = topic_appearences_by_months[month]
            topic_score_object = self._create_topic_score_object(most_shares, most_likes, most_frequent, most_distinct_authors, month_stats)
            months_to_topic_score[month] = topic_score_object


        return months_to_topic_score

    def get_topic_appearances(self, topic, year):
        url = f'http://{TOPICS_REPOSITORY_SERVICE_NAME}:{TOPICS_REPOSITORY_SERVICE_PORT}/repotopics/get_single_topic_trend'  # Adjust the URL based on your setup
        params = {
            'year': year,
            'topic': topic,
        }
        print(f"out going request to: {url} with params: {params}")
        response = requests.get(url, params=params)
        if(response.status_code != 200):
            raise Exception("TrendsEngine: Failed to get topic year trend from repository.")
        
        raw_topic_appearences = response.json()
        return [{"topic": topic_stats[0], "month":topic_stats[1], "author": topic_stats[2], "likes": topic_stats[3],  "shares": topic_stats[4]} for topic_stats in raw_topic_appearences]

    
    def _aggregate_topic_stats(self, start_date, end_date):
        # Assuming start_date and end_date are datetime.date objects
        month_ranges = self._get_month_ranges(start_date, end_date)
        topic_stats = {}

        for start, end in month_ranges:
            print(f"Calling get_topics_by_month with: {start.year, start.month, start.day, end.day}")
            result = self._get_topics_by_month(start.year, start.month, start.day, end.day)
            for row in result:
                topic = row["topic"]
                if(topic not in EXCLUDE_PHRASES and (not topic.startswith("http")) and not topic.isdigit()):
                    if topic not in topic_stats:
                        print(f"inserting topic: {topic}")
                        topic_stats[topic] = TopicStats(topic=topic)
                    topic_stats[topic].add_tweet(row["author"], row["likes"], row["shares"])
        print(f"_aggregate_topic_stats:: returning topic stats: {len(topic_stats)}")
        return topic_stats

    def _get_topics_by_month(self, year, month, start_day, end_day):
        url = f'http://{TOPICS_REPOSITORY_SERVICE_NAME}:{TOPICS_REPOSITORY_SERVICE_PORT}/repotopics/get_topics_by_month'  # Adjust the URL based on your setup
        params = {
            'year': year,
            'month': month,
            'start_day': start_day,
            'end_day': end_day
        }
        print(f"out going request to: {url} with params: {params}")
        response = requests.get(url, params=params)
        if(response.status_code != 200):
            raise Exception("TrendsEngine: Failed to get topics by month from repository.")
        
        json = response.json()
        return [{"topic": topic_stats[0], "author": topic_stats[1], "likes": topic_stats[2],  "shares": topic_stats[3]} for topic_stats in json]

    @staticmethod
    def _get_month_ranges(start_date, end_date):
        current = start_date
        while current <= end_date:
            # Find the last day of the current month
            month_end = current.replace(day=1) + timedelta(days=32)
            month_end = month_end.replace(day=1) - timedelta(days=1)
            month_end = min(end_date, month_end)
            
            yield (current, month_end)
            current = month_end + timedelta(days=1)

    @staticmethod
    def _create_topic_score_object(most_shares, most_likes, most_frequent, most_distinct_authors, stats):
        topic_score_object = TopicScore(topic= stats.topic, total_tweets= stats.total_tweets, total_shares= stats.total_shares, total_likes= stats.total_likes, distinct_authors= len(stats.distinct_authors))
        topic_score_object.share_score = stats.total_shares / most_shares if most_shares else 0
        topic_score_object.like_score = stats.total_likes / most_likes if most_likes else 0
        topic_score_object.frequency_score = stats.total_tweets / most_frequent if most_frequent else 0
        topic_score_object.author_frequency_score = len(stats.distinct_authors) / most_distinct_authors if most_distinct_authors else 0
        topic_score_object.trend_score = (share_score_factor * topic_score_object.share_score) + (like_score_factor*topic_score_object.like_score) + (frequency_score_factor*topic_score_object.frequency_score) + (author_frequency_score*topic_score_object.author_frequency_score)
        return topic_score_object