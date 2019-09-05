from pathlib import Path

import numpy as np
import pandas as pd


def build_tweet_df() -> pd.DataFrame:
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

    df_rus = df_rus[df_rus['language'] == 'English'].dropna(subset=['content'])

    categorical_fields = ['region', 'language', 'post_type', 'account_type', 'account_category']
    df_rus[categorical_fields] = df_rus[categorical_fields].astype('category')

    return df_rus


