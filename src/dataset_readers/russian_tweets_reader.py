import itertools
from datetime import datetime
from pathlib import Path
import csv

from data_structures.russian_tweet_data import RussianTweetData
from dataset_readers.dataset_reader import DatasetReader

TWEET_DIR = "../data/russian-troll-tweets"
TWEET_FILE_EXTENSION = "csv"


class RussianTweetReader(DatasetReader):
    def __init__(
            self,
            document_location: str = TWEET_DIR,
            document_extension: str = TWEET_FILE_EXTENSION
    ):
        super().__init__(document_location, document_extension)

    def convert_document(self, fp: Path) -> RussianTweetData:
        with open(fp) as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)
            for row in csv_reader:
                fields = list(zip(headers, row))
                fields.append(("file_path", str(fp)))

                tweet_data = dict(fields)

                for date_field in {"publish_date", "harvested_date"}:
                    tweet_data[date_field] = datetime.strptime(tweet_data[date_field], "%m/%d/%Y %H:%M")

                for int_field in {"following", "followers", "updates"}:
                    tweet_data[int_field] = int(tweet_data[int_field])

                for bool_field in {"retweet", "new_june_2018"}:
                    tweet_data[bool_field] = bool(tweet_data[bool_field])

                yield RussianTweetData(**tweet_data)
