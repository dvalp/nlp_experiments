import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from pandas.io.json import json_normalize

# TODO: Load from config file instead
JSON_DIR = Path('../../data/json_tweets/')
TWEET_DIR = Path('../../data/russian-troll-tweets')


def build_tweet_df(filter_language: str = 'English', convert_dates: bool = True) -> pd.DataFrame:
    """
    Create a DataFrame from directory of Russian troll tweets.

    Defaults to filtering only for documents labeled as English language, but
    many other languages are present in the original data. Not all language
    fields are completely correct - I've noticed some that appear to be English
    but are marked as unknown languages.

    Setting column types stops Pandas from guessing; guessing causes problems
    when combining some data sets. Converting to categorical and date makes
    the data more useful in some contexts.

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
        (pd.read_csv(csv, header=0, dtype=col_types) for csv in TWEET_DIR.rglob('*.csv')),
        ignore_index=True)

    df_rus = df_rus[df_rus['language'] == filter_language].dropna(subset=['content'])

    if convert_dates:
        df_rus['publish_date'] = pd.to_datetime(df_rus['publish_date'], infer_datetime_format=True)
        df_rus['harvested_date'] = pd.to_datetime(df_rus['harvested_date'], infer_datetime_format=True)

    categorical_fields = ['region', 'language', 'post_type', 'account_type', 'account_category']
    df_rus[categorical_fields] = df_rus[categorical_fields].astype('category')

    return df_rus


def make_json_samples(df: pd.DataFrame, sample_size: int = 20) -> None:
    """
    Make a small set of JSON files from the tweet collection. This is only
    necessary for creating some sample documents for testing some code to
    read json files into a database.

    Note that the URLs are artificially moved into a subgroup for testing
    the code with nested JSON.

    Warning: Some tweet IDs are duplicated, it is possible that conflicts
    will occur. This is just for creating some sample files, so no big
    problem, but this is definitely not production ready.

    :param df: Tweet DataFrame created by build_tweet_df() (above)
    :param sample_size: Number of items to return
    """
    convert_fields = ['publish_date', 'harvested_date', 'region', 'language', 'post_type', 'account_type',
                      'account_category']
    df[convert_fields] = df[convert_fields].astype(str)

    docs = df.sample(n=sample_size).fillna("nan").to_dict(orient='records')

    for doc in docs:
        doc['urls'] = {}
        for field in ['article_url', 'tco1_step1', 'tco2_step1', 'tco3_step1']:
            doc['urls'][field] = doc[field]
            del doc[field]

        with open(Path(JSON_DIR, f"{doc['tweet_id']}.json"), 'w') as fp:
            json.dump(doc, fp)


def load_json_data() -> dict:
    """
    Load a directory of JSON files through a generator for reading into a
    DataFrame.

    :return: Each file as a dictionary
    """
    for file_name in JSON_DIR.rglob('*.json'):
        with open(file_name, 'r') as fp:
            yield json.load(fp)


def flatten_tweets() -> dict:
    """
    Reformat (flatten) JSON as necessary to fit in DB table.

    :return: Dictionary of data for one document.
    """
    for doc in load_json_data():
        doc.update(doc['urls'])
        del doc['urls']
        doc['publish_date'] = datetime.strptime(doc['publish_date'], '%Y-%m-%d %H:%M:%S')
        doc['harvested_date'] = datetime.strptime(doc['harvested_date'], '%Y-%m-%d %H:%M:%S')

        for key, value in doc.items():
            if value == "nan":
                doc[key] = None

        yield doc


def build_tweet_df_from_json():
    """
    Use json_normalize() to create a DataFrame from dictionary objects.

    :return: DataFrame from JSON objects
    """
    return json_normalize(load_json_data(), sep='_')


def move_json_to_sql_db(dir_path: Path) -> None:
    json_docs = []
    for file_name in Path(dir_path).rglob('*.json'):
        with open(file_name, 'r') as fp:
            json_docs.append(json.load(fp))
