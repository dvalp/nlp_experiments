import argparse

from russian_tweets import build_tweet_df, make_json_samples
from tweet_orm import tweets_to_db


def create_json_samples(args):
    df = build_tweet_df()
    make_json_samples(df, sample_size=args.sample_size)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Process text files for NLP")
    parser.add_argument('--foo', action='store_true', help='foo help')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_db = subparsers.add_parser("store-tweets", help="Process tweets into a database for later use")
    parser_db.set_defaults(func=tweets_to_db)

    parser_json = subparsers.add_parser("json-sample", help="Create sample JSON from tweets to work with")
    parser_json.add_argument("-s", "--sample-size", type=int, default=20, help="Number of JSON samples to create")
    parser_json.set_defaults(func=create_json_samples)

    args = parser.parse_args()
    args.func(args)
