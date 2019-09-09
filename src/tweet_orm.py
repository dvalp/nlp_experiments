from sqlalchemy import Boolean, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TweetDoc(Base):
    __tablename__ = 'russian_tweets'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    external_author_id = Column(String)
    author = Column(String)
    content = Column(String)
    region = Column(String)
    language = Column(String)
    publish_date = Column(String)
    harvested_date = Column(String)
    following = Column(Integer)
    followers = Column(Integer)
    updates = Column(Integer)
    post_type = Column(String)
    account_type = Column(String)
    retweet = Column(Boolean)
    account_category = Column(String)
    new_june_2018 = Column(Boolean)
    alt_external_id = Column(String)
    tweet_id = Column(String)
    article_url = Column(String)
    tco1_step1 = Column(String)
    tco2_step1 = Column(String)
    tco3_step1 = Column(String)

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
