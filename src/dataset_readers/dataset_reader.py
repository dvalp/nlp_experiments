"""
Abstract Base Class for reading document sets into an internal data model.

Designed to be used as an iterator so that individual records can be collected
and potentially batched together for processing.

Optionally to be used as a context manager in cases where setup/teardown are
required (if reading from a stream for example).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import NamedTuple, Optional


class DatasetReader(ABC):
    def __init__(self, document_location: str, document_extension: str, date_format: Optional[str] = None):
        self.document_location: str = document_location
        self.document_extension: str = document_extension
        self.date_format: str = date_format
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
        data_files = Path(self.document_location).rglob(f"*.{self.document_extension}")
        for fpath in data_files:
            for record in self.convert_document(fpath):
                yield record

    def partial_strptime(self, date_value: str) -> datetime:
        """
        The datetime strptime() function can only take one argument in the
        for converting data types. Here it is given default values for
        formatting the date.

        :param date_value: String containing a date matching the given format.
        :return: Transformed date value
        """
        return datetime.strptime(date_value, self.date_format)

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
        yield from self.data_points
