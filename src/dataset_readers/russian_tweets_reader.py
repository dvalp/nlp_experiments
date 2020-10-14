import csv
from datetime import datetime
from pathlib import Path

from data_structures.russian_tweet_data import RussianTweetData
from dataset_readers.dataset_reader import DatasetReader


class RussianTweetReader(DatasetReader):
    def __init__(
            self,
            document_location: str = "../data/russian-troll-tweets",
            document_extension: str = "csv"
    ):
        super().__init__(document_location, document_extension)

    def convert_document(self, fp: Path) -> RussianTweetData:
        with open(fp) as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)
            for row in csv_reader:
                fields = list(zip(headers, row))
                fields.append(("file_path", str(fp)))

                tweet_data = self.convert_datatypes(dict(fields))

                yield RussianTweetData(**tweet_data)

    def convert_datatypes(self, tweet_data: dict):
        actions = (
            (int, {"following", "followers", "updates"}),
            (bool, {"retweet", "new_june_2018"}),
            (self.partial_strptime, {"publish_date", "harvested_date"})
        )

        for (action, fields) in actions:
            for field in fields:
                tweet_data[field] = action(tweet_data[field])

        return tweet_data

    @staticmethod
    def partial_strptime(date_value: str) -> datetime:
        return datetime.strptime(date_value, "%m/%d/%Y %H:%M")
