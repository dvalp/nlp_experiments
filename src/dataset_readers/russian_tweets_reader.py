from pathlib import Path

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
        pass
