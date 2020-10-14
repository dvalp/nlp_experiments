"""
Document reader class for the Russian tweet collection from
https://fivethirtyeight.com/features/why-were-sharing-3-million-russian-troll-tweets/

Inherits from the ABC DatasetReader.
"""
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
        """
        Convert all rows from a given CSV file into internal data objects
        (in this case RussianTweetData).

        :param fp: Path to the CSV file to process
        :return:
        """
        with open(fp) as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)
            for row in csv_reader:
                fields = list(zip(headers, row))
                fields.append(("file_path", str(fp)))

                tweet_data = self.convert_data_types(dict(fields))

                yield RussianTweetData(**tweet_data)

    def convert_data_types(self, tweet_data: dict) -> dict:
        """
        Convert the string values that have been imported from the CSV into
        more useful data types.

        :param tweet_data: One row (tweet) from the CSV
        :return: Dict with converted fields
        """
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
        """
        The datetime strptime() function can only take one argument in the
        for converting data types. Here it is given default values for
        formatting the date.

        :param date_value: String containing a date matching the given format.
        :return: Transformed date value
        """
        return datetime.strptime(date_value, "%m/%d/%Y %H:%M")
