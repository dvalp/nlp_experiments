import itertools
from abc import ABC, abstractmethod
from pathlib import Path
from typing import NamedTuple


class DatasetReader(ABC):
    def __init__(self, document_location: str, document_extension: str):
        self.document_location: str = document_location
        self.document_extension: str = document_extension

    def load_documents(self, file_extension: str) -> NamedTuple:
        data_files = Path(self.document_location).rglob(f"*.{file_extension}")
        entries = itertools.chain(self.convert_document(fp) for fp in data_files)
        for entry in entries:
            yield entry

    @abstractmethod
    def convert_document(self, fp: Path):
        raise NotImplementedError
