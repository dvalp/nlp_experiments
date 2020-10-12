import itertools
from abc import ABC, abstractmethod
from pathlib import Path

from data_structures.russian_tweet_data import RussianTweetData


class DatasetReader(ABC):
    def __init__(self, document_location: str, document_extension: str):
        self.document_location: str = document_location
        self.document_extension: str = document_extension

    @abstractmethod
    def convert_document(self, fp: Path):
        pass

    def __iter__(self):
        return self

    def __next__(self) -> RussianTweetData:
        data_files = Path(self.document_location).rglob(f"*.{self.document_extension}")

        for entry in itertools.chain(self.convert_document(fp) for fp in data_files):
            yield entry
