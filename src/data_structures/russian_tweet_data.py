from datetime import datetime
from typing import NamedTuple


class RussianTweetData(NamedTuple):
    file_path: str
    external_author_id: str
    author: str
    content: str
    region: str
    language: str
    publish_date: datetime
    harvested_date: datetime
    following: int
    followers: int
    updates: int
    post_type: str
    account_type: str
    retweet: bool
    account_category: str
    new_june_2018: bool
    alt_external_id: str
    tweet_id: str
    article_url: str
    tco1_step1: str
    tco2_step1: str
    tco3_step1: str
    id: int = None

    def __eq__(self, other):
        ignore_fields = {"id"}
        return all((value == other.__dict__[key]) for key, value in self.__dict__.items()
                   if key not in ignore_fields)

    def __ne__(self, other):
        return not self.__eq__(other)
