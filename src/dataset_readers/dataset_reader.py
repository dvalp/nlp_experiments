from abc import ABC, abstractmethod
from pathlib import Path
from typing import NamedTuple


class DatasetReader(ABC):
    def __init__(self, document_location: str, document_extension: str):
        self.document_location: str = document_location
        self.document_extension: str = document_extension

    def load_documents(self, file_extension: str) -> NamedTuple:
        for fp in Path(self.document_location).rglob(f"*.{file_extension}"):
            yield self.convert_document(fp)

    @abstractmethod
    def convert_document(self, fp: Path):
        raise NotImplementedError
