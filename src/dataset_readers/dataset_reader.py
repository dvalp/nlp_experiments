"""
Abstract Base Class for reading document sets into an internal data model.

Designed to be used as an iterator so that individual records can be collected
and potentially batched together for processing.

Optionally to be used as a context manager in cases where setup/teardown are
required (if reading from a stream for example.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import NamedTuple, Iterable


class DatasetReader(ABC):
    def __init__(self, document_location: str, document_extension: str):
        self.document_location: str = document_location
        self.document_extension: str = document_extension

    @abstractmethod
    def convert_document(self, fp: Path) -> NamedTuple:
        """
        Required method for converting the raw data into internal data
        representations. To be defined in the child class for a particular
        kind of data.

        :param fp: Location of a file to be processed.
        :return: A NamedTuple for the data
        """
        pass

    def __enter__(self) -> Iterable:
        """
        Provide a context manager for the data processing, in case where it
        teardown operations are desired (ie, when processing a stream).

        :return: The iterable for this class
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Required for the closing process of the context manager. Currently a
        no-op process because closing of the files is handled in pathlib.Path

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return: z
        """
        pass

    def __iter__(self) -> DatasetReader:
        """
        Load files containing data points read each record from the file,
        sending it to be processed.

        :return: A record transformed into the internal data representation
        """
        return self

    def __next__(self) -> NamedTuple:
        data_files = Path(self.document_location).rglob(f"*.{self.document_extension}")
        for fpath in data_files:
            for record in self.convert_document(fpath):
                return record
