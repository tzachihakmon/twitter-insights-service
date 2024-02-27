import csv
from typing import Iterator
from dateutil.parser import parse
from dataclasses import dataclass


@dataclass
class Tweet:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    content: str
    author: str
    likes: int
    shares: int

class TweetsRepository:
    def __init__(self):
        self.source = 'tweets.csv'

    def get_tweets(self) -> Iterator[Tweet]:
        """Yield Tweet objects from the source."""
        with open(self.source, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dt = parse(row['date_time'])
                yield Tweet(
                    year=dt.year,
                    month=dt.month,
                    day=dt.day,
                    hour=dt.hour,
                    minute=dt.minute,
                    content=row['content'],
                    author=row['author'],
                    likes=int(row['number_of_likes']),
                    shares=int(row['number_of_shares'])
                )