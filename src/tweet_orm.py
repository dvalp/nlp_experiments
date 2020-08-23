import json

from sqlalchemy import Boolean, Column, DateTime, Integer, Sequence, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from russian_tweets import flatten_tweets

with open("../db_config.json", "r") as f:
    config = json.load(f)

engine = create_engine(config["sqlite"]["connection_string"], echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class TweetDoc(Base):
    __tablename__ = 'russian_tweets'

    id = Column(Integer, Sequence('tweet_id_seq'), primary_key=True)
    external_author_id = Column(String(20))
    author = Column(String(20))
    content = Column(String(1000))
    region = Column(String(20))
    language = Column(String(20))
    publish_date = Column(DateTime)
    harvested_date = Column(DateTime)
    following = Column(Integer)
    followers = Column(Integer)
    updates = Column(Integer)
    post_type = Column(String(20))
    account_type = Column(String(20))
    retweet = Column(Boolean)
    account_category = Column(String(20))
    new_june_2018 = Column(Boolean)
    alt_external_id = Column(String(20))
    tweet_id = Column(String(20))
    article_url = Column(String(100))
    tco1_step1 = Column(String(300))
    tco2_step1 = Column(String(300))
    tco3_step1 = Column(String(300))

    def __repr__(self):
        return f"<TweetDoc(external_author_id='{self.external_author_id}', author='{self.author}', " \
               f"content='{self.content}', region='{self.region}', language='{self.language}', " \
               f"publish_date='{self.publish_date}', harvested_date='{self.harvested_date}', " \
               f"following='{self.following}', followers='{self.followers}', updates='{self.updates}', " \
               f"post_type='{self.post_type}', account_type='{self.account_type}', retweet='{self.retweet}', " \
               f"account_category='{self.account_category}', new_june_2018='{self.new_june_2018}', " \
               f"alt_external_id='{self.alt_external_id}', tweet_id='{self.tweet_id}', " \
               f"article_url='{self.article_url}', tco1_step1='{self.tco1_step1}', tco2_step1='{self.tco2_step1}', " \
               f"tco3_step1='{self.tco3_step1}')>"


def tweets_to_db():
    Base.metadata.create_all(engine)
    sess = Session()
    try:
        sess.add_all(TweetDoc(**tweet) for tweet in flatten_tweets())
        sess.commit()
    except Exception as e:
        sess.rollback()
        raise e
    finally:
        sess.close()
