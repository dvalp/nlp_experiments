from abc import ABC, abstractmethod
from pathlib import Path

from data_structures.russian_tweet_data import RussianTweetData

TWEET_DIR = "../data/russian-troll-tweets"
TWEET_FILE_EXTENSION = "csv"


class DatasetReader(ABC):
    def __init__(self, document_location: str, document_extension: str):
        self.document_location: str = document_location
        self.document_extension: str = document_extension

    def load_documents(self):
        for fp in Path(self.document_location).rglob(f"*.{TWEET_FILE_EXTENSION}"):
            self.convert_document(fp)

    @abstractmethod
    def convert_document(self, fp: Path):
        raise NotImplementedError


class RussianTweetReader(DatasetReader):
    def __init__(
            self,
            document_location: str = TWEET_DIR,
            document_extension: str = TWEET_FILE_EXTENSION
    ):
        super().__init__(document_location, document_extension)

    def convert_document(self, fp: Path):
        pass
