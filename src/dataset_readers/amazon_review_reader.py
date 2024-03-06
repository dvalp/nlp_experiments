from pathlib import Path
from typing import NamedTuple

import json_lines

from src.dataset_readers.dataset_reader import DatasetReader


class AmazonReviewReader(DatasetReader):
    def convert_document(self, fp: Path) -> NamedTuple:
        with json_lines.open(fp) as f:
            for item in f:
                yield item
