"""
Abstract Base Class for reading document sets into an internal data model.

Designed to be used as an iterator so that individual records can be collected
and potentially batched together for processing.

Optionally to be used as a context manager in cases where setup/teardown are
required (if reading from a stream for example.
"""
from abc import ABC, abstractmethod
from contextlib import contextmanager
from pathlib import Path


class DatasetReader(ABC):
    def __init__(self, document_location: str, document_extension: str):
        self.document_location: str = document_location
        self.document_extension: str = document_extension

    @abstractmethod
    def convert_document(self, fp: Path):
        pass

    @contextmanager
    def document_set_reader(self):
        yield self.__iter__()

    def __iter__(self):
        data_files = Path(self.document_location).rglob(f"*.{self.document_extension}")
        for fpath in data_files:
            for record in self.convert_document(fpath):
                yield record
