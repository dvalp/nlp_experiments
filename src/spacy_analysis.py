from string import ascii_letters
from typing import Collection, Generator

import nl_core_news_sm
from spacy.tokens.doc import Doc

from src.rechtspraak_xml import read_xmls


def xml_docs() -> Generator[str, None, None]:
    docs = list(read_xmls("data/sample_dataset/xmls/"))
    letters = set(ascii_letters)

    for doc in docs:
        section_texts = []
        for section in doc['text'].values():
            for line in section:
                if len([character for character in line if character in letters]) > 3:
                    section_texts.append(line)
            section_texts.append("\n")
        yield ' '.join(section_texts).strip()


def create_spacy_objects(texts: Collection[str]) -> Generator[Doc, None, None]:
    nlp = nl_core_news_sm.load()
    for text in texts:
        yield nlp(text)
