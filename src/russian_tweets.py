from pathlib import Path

import pandas as pd


def build_tweet_df() -> pd.DataFrame:
    df_rus = pd.concat((pd.read_csv(csv) for csv in Path('../data/russian-troll-tweets').rglob('*.csv')),
                       ignore_index=True)
    df_rus = df_rus[df_rus['language'] == 'English'].dropna(subset=['content'])
    categorical_fields = ['author', 'region', 'post_type', 'account_type', 'account_category']
    df_rus[categorical_fields] = df_rus[categorical_fields].astype('category')

    return df_rus
