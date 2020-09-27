from abc import ABC, abstractmethod
from pathlib import Path

from dataset_readers.russian_tweets_reader import TWEET_FILE_EXTENSION


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
