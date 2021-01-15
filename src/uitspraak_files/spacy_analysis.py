from string import ascii_letters
from typing import Collection, Generator

import nl_core_news_md
from spacy.tokens.doc import Doc

from uitspraak_files.extract_from_xmls import parse_xmls


def xml_docs() -> Generator[str, None, None]:
    docs = parse_xmls()
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
    nlp = nl_core_news_md.load()
    for text in texts:
        yield nlp(text)
