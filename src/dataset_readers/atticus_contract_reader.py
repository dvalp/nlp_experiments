import csv
from pathlib import Path
from typing import NamedTuple
from zipfile import ZipFile

import requests

from data_structures.atticus_project_data import label_mappings, AtticusIndividualClause
from dataset_readers.dataset_reader import DatasetReader


class AtticusIndividualClauseReader(DatasetReader):
    def __init__(
            self,
            document_location: str = "../../data/atticus-contracts/Final Publication/individual_contract_clauses",
            document_extension: str = "csv",
            atticus_zip: str = "aok_beta.zip"
    ):
        self.atticus_zip = atticus_zip
        super().__init__(document_location, document_extension)

    def convert_document(self, fp: Path) -> NamedTuple:
        with open(fp) as csv_file:
            csv_reader = csv.reader(csv_file)
            _ = next(csv_reader)
            for row in csv_reader:
                fields = list(zip(headers, row))
                fields.append(("file_path", str(fp)))

                record = self.convert_data_types(dict(fields))

                yield AtticusIndividualClause(**record)

    def convert_data_types(self, record: dict):
        actions = (
            (int, {}),
            (bool, {("better_terms non_compete exclusivity customer_solicitation employee_solicitation "
                     "non_disparagement convenience_termination first_rights change_control anti_assignment "
                     "profit_sharing price_restriction minimum_commitment volume_restriction ip_assignment joint_ip "
                     "license_grant non_transferable_license affiliate_licensor affiliate_licensee unlimited_usage "
                     "perpetual_license code_escrow post_termination audit_rights uncapped_liability capped_liability "
                     "liquidated_damages warranty_duration insurance outside_claims third_party").split()}),
            (self.partial_strptime, {})
        )

        for (action, fields) in actions:
            for field in fields:
                record[field] = action(record[field])

        return record

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


if __name__ == '__main__':
    c = AtticusIndividualClauseReader()
    print(next(c))
