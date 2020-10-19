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
from typing import NamedTuple


class DatasetReader(ABC):
    def __init__(self, document_location: str, document_extension: str):
        self.document_location: str = document_location
        self.document_extension: str = document_extension
        self.data_points = self.data_iterator()

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

    def data_iterator(self) -> NamedTuple:
        data_files = Path(self.document_location).glob(f"*.{self.document_extension}")
        for fpath in data_files:
            for record in self.convert_document(fpath):
                yield record

    def __enter__(self) -> DatasetReader:
        """
        Provide a context manager for the data processing, in cases where
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
        Because of the __next__() implementation, the class is already iterable.

        :return: A class that iterates through data points
        """
        return self

    def __next__(self) -> NamedTuple:
        """
        Allows the class to iterate through the individual data points loaded
        from the document set using a stored state for the class instance.

        :return: One data point from the document set
        """
        return next(self.data_points)
