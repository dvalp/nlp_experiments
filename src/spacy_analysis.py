from string import ascii_letters
from typing import Collection, Generator

import spacy
from spacy.tokens.doc import Doc

from src.rechtspraak_xml import read_xmls


def xml_docs():
    docs = list(read_xmls("nlp_experiments/data/sample_dataset/xmls/"))
    letters = set(ascii_letters)
    page_texts = []
    for doc in docs:
        section_texts = []
        for section in doc['text'].values():
            for line in section:
                if len([character for character in line if character in letters]) > 3:
                    section_texts.append(line)
            section_texts.append("\n")
        page_texts.append(' '.join(section_texts).strip())

    return page_texts


def create_spacy_objects(texts: Collection[str]) -> Generator[Doc]:
    nlp = spacy.load("nl_core_news_sm")
    for text in texts:
        yield nlp(text)
