from dataclasses import dataclass , field
from datetime import datetime, timedelta
import sys
sys.path.append('C:/src/flask-app/topic_repository_module')
from TopicRepositoryModule import TopicsRepository
EXCLUDE_PHRASES = {"less than 24 hours", "tbt", "the day","1", "month of the year", "next week", "last day","one day", "this week","the week", "next year", "this year", "the year", "last night's" ,"last night", "all day","every day", "tomorrow", "yesterday", "the weekend", "this weekend","everyday" ,"last night","last week", "last year", "this day"}

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
    def __init__(self):
        self.topic_repository = TopicsRepository()

    def get_k_most_trend_topics(self, k, start_date, end_date):
        all_topics_stats = self._aggregate_topic_stats(start_date, end_date)
        # Calculate scores and sort
        most_shares = max(stats.total_shares for stats in all_topics_stats.values())
        most_likes = max(stats.total_likes for stats in all_topics_stats.values())
        most_frequent = max(stats.total_tweets for stats in all_topics_stats.values())
        most_distinct_authors = max(len(stats.distinct_authors) for stats in all_topics_stats.values())

        top_k_topics = []
        for stats in all_topics_stats.values():
            topic_score_object = TopicScore(topic= stats.topic, total_tweets= stats.total_tweets, total_shares= stats.total_shares, total_likes= stats.total_likes, distinct_authors= len(stats.distinct_authors))
            topic_score_object.share_score = stats.total_shares / most_shares if most_shares else 0
            topic_score_object.like_score = stats.total_likes / most_likes if most_likes else 0
            topic_score_object.frequency_score = stats.total_tweets / most_frequent if most_frequent else 0
            topic_score_object.author_frequency_score = len(stats.distinct_authors) / most_distinct_authors if most_distinct_authors else 0
            topic_score_object.trend_score = (0.35 * topic_score_object.share_score) + (0.05*topic_score_object.like_score) + (0.20*topic_score_object.frequency_score) + (0.40*topic_score_object.author_frequency_score)
            top_k_topics.append(topic_score_object)
        # Sort topics by trend score and return top k
        top_k_topics = sorted(top_k_topics, key=lambda x: x.trend_score, reverse=True)[:k]
        for topic in top_k_topics:
            print(topic)
        return top_k_topics

    def _aggregate_topic_stats(self, start_date, end_date):
        # Assuming start_date and end_date are datetime.date objects
        month_ranges = self._get_month_ranges(start_date, end_date)
        topic_stats = {}

        for start, end in month_ranges:
            print(f"Calling get_topics_by_month with: {start.year, start.month, start.day, end.day}")
            result = self.topic_repository.get_topics_by_month(start.year,start.month, start.day, end.day)
            for row in result:
                if(row.topic not in EXCLUDE_PHRASES):
                    if row.topic not in topic_stats:
                        print(f"inserting topic: {row.topic}")
                        topic_stats[row.topic] = TopicStats(topic=row.topic)
                    topic_stats[row.topic].add_tweet(row.author, row.likes, row.shares)

        return topic_stats

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