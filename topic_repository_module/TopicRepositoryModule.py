import gevent
import gevent.monkey
gevent.monkey.patch_all()
from cassandra.io.geventreactor import GeventConnection
from cassandra.cluster import Cluster
import os
from dataclasses import dataclass

CASSANDRA_HOSTS =  [os.getenv('CASSANDRA_HOST', 'cassandra')] #  ["127.0.0.1"]  # Assuming 'cassandra' is the name of your Cassandra service in Kubernetes
KEYSPACE = "tweets_topics_1"
topic_trends_table = "topic_trends3"
topics_by_time_table = "topics_by_time4"

@dataclass
class Topic:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    topic: str
    author: str
    likes: int
    shares: int

def CreateKeySpaceIfNotExist(session):
        session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {KEYSPACE} 
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}};
        """)

def CreateTables(session):
    session.execute(f"""
    CREATE TABLE IF NOT EXISTS {KEYSPACE}.{topic_trends_table} (
    topic text,
    year int,
    month int,
    day int,
    hour int,
    minute int,
    author text,
    likes int,
    shares int,
    PRIMARY KEY ((topic), year, month, day, hour,author)
    );
    """)

    session.execute(f"""
    CREATE TABLE IF NOT EXISTS {KEYSPACE}.{topics_by_time_table}(
    topic text,
    year int,
    month int,
    day int,
    hour int,
    minute int,
    author text,
    likes int,
    shares int,
    PRIMARY KEY ((year, month), day, hour, minute, topic, likes, shares ,author)
    );
    """)  

def invoke_query(session, query):
    try:
        result = session.execute(query)
        df = result._current_rows
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        
class TopicsRepository:
    def __init__(self):
        self.cluster = Cluster(CASSANDRA_HOSTS)
        self.cluster.connection_class = GeventConnection
        cluster_session = self.cluster.connect()
        print(cluster_session)
        CreateKeySpaceIfNotExist(cluster_session)
        self.session = self.cluster.connect(KEYSPACE)
        CreateTables(self.session)

    def insert_topics(self, topics):
        for topic in topics:
            self.session.execute(
                f"""
                INSERT INTO {topic_trends_table} (topic, year, month, day, hour, minute, author, likes, shares)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (topic.topic, topic.year, topic.month, topic.day, topic.hour, topic.minute, topic.author, topic.likes, topic.shares)
            )

            self.session.execute(
                f"""
                INSERT INTO {topics_by_time_table} (topic, year, month, day, hour, minute, author, likes, shares)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (topic.topic, topic.year, topic.month, topic.day, topic.hour, topic.minute, topic.author, topic.likes, topic.shares)
            )

    def get_all_topics_appearences(self, topic_name, year, start_month, end_month):
        query = f"""SELECT
        topic, year, month, day, hour, minute, author, likes, shares
        FROM {topic_trends_table}
        WHERE topic = '{topic_name}' and year = {year} and month>={start_month} and month<= {end_month};"""

        return invoke_query(self.session, query)
    

    def get_topics_by_month(self, year, month, start_day, end_day):
        # Adjust the query to fetch required details for trend calculation
        query = f"""
        SELECT topic, author, likes, shares
        FROM {topics_by_time_table}
        WHERE year = {year} AND month = {month} AND day>={start_day} AND day <= {end_day}
        """

        print(f"About to invoke query:\n{query}")
        return invoke_query(self.session, query)

