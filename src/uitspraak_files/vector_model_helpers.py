from itertools import chain
from typing import Iterator

from uitspraak_files.extract_from_xmls import parse_xmls
from vector_models.fasttext_model import create_training_sentences, train_model


def joined_texts() -> Iterator[str]:
    for doc in parse_xmls():
        yield ' '.join(chain(*doc["text"].values()))


def train_fasttext() -> None:
    training_sentences = create_training_sentences(joined_texts())
    train_model(training_sentences)


if __name__ == '__main__':
    train_fasttext()
