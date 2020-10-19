from pathlib import Path
from typing import NamedTuple
from zipfile import ZipFile

import requests

from dataset_readers.dataset_reader import DatasetReader


class AtticusIndividualClauseReader(DatasetReader):
    def __init__(
            self,
            document_location: str = "../data/atticus-contracts/Final Publication/individual_contract_clauses",
            document_extension: str = ".csv",
            atticus_zip = "aok_beta.zip"
    ):
        self.atticus_zip = atticus_zip
        super().__init__(document_location, document_extension)

    def convert_document(self, fp: Path) -> NamedTuple:
        pass

    def download_datafile(self):
        dl_path = "https://zenodo.org/record/4064880/files/aok_beta.zip?download=1"
        file_path = Path(self.document_location, self.atticus_zip)
        Path(self.document_location).mkdir(exist_ok=True, parents=True)

        with requests.get(dl_path, stream=True) as r:
            Path(file_path).write_bytes(r.content)

    def extract_datafile(self):
        file_path = Path(self.document_location, self.atticus_zip)
        if not file_path.exists():
            self.download_datafile()
        with ZipFile(file_path, mode='r') as z:
            z.extractall(path=self.document_location)