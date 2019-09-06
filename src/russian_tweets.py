import json
from pathlib import Path

import numpy as np
import pandas as pd


def build_tweet_df(filter_language: int = 'English', convert_dates=True) -> pd.DataFrame:
    """
    Create a DataFrame from directory of Russian troll tweets.

    Defaults to filtering only for documents labeled as English language, but
    many other languages are present in the original data. Not all language
    fields are completely correct - I've noticed some that appear to be English
    but are marked as unknown languages.

    Setting column types stops Pandas from guessing; guessing causes problems
    when combining some of the data sets. Converting to categoricals and dates
    makes the data more useful in some contexts.

    Datetime fields are not storable in JSON, set convert_dates to False if
    you intend to make JSON files from this dataset using the function
    make_json_samples() below.

    :param filter_language: Language to filter on
    :param convert_dates: Convert dates to datetime
    :return: DataFrame of twitter posts with metadata
    """
    col_types = {'external_author_id': str,
                 'author':             str,
                 'content':            str,
                 'region':             str,
                 'language':           str,
                 'publish_date':       str,
                 'harvested_date':     str,
                 'following':          np.int32,
                 'followers':          np.int32,
                 'updates':            np.int32,
                 'post_type':          str,
                 'account_type':       str,
                 'retweet':            bool,
                 'account_category':   str,
                 'new_june_2018':      bool,
                 'alt_external_id':    str,
                 'tweet_id':           str,
                 'article_url':        str,
                 'tco1_step1':         str,
                 'tco2_step1':         str,
                 'tco3_step1':         str}

    df_rus = pd.concat(
        (pd.read_csv(csv, header=0, dtype=col_types) for csv in Path('../data/russian-troll-tweets').rglob('*.csv')),
        ignore_index=True)

    df_rus = df_rus[df_rus['language'] == filter_language].dropna(subset=['content'])

    if convert_dates:
        df_rus['publish_date'] = pd.to_datetime(df_rus['publish_date'], infer_datetime_format=True)
        df_rus['harvested_date'] = pd.to_datetime(df_rus['harvested_date'], infer_datetime_format=True)

    categorical_fields = ['region', 'language', 'post_type', 'account_type', 'account_category']
    df_rus[categorical_fields] = df_rus[categorical_fields].astype('category')

    return df_rus


def make_json_samples(df: pd.DataFrame, sample_size=20) -> None:
    """
    Make a small set of JSON files from the tweet collection. This is only
    necessary for creating some sample documents for testing some code to
    read json files into a database.

    Note that the URLs are artificially moved into a sub group for testing
    the code with nested JSON.

    :param df: Tweet DataFrame created by build_tweet_df() (above)
    :param sample_size: Number of items to return
    """
    docs = df.sample(n=sample_size).to_dict(orient='records')

    for doc in docs:
        doc['urls'] = {}
        for field in ['article_url', 'tco1_step1', 'tco2_step1', 'tco3_step1']:
            doc['urls'][field] = doc[field]
            del doc[field]

        with open(Path('../data/json_tweets/', doc['tweet_id']), 'w') as fp:
            json.dump(doc, fp)
