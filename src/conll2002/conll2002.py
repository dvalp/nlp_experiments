import gzip
from collections import namedtuple
from typing import Union, Collection, Any, Dict

NamedEntity = namedtuple("NamedEntity", "entity, etype")
Token = namedtuple("Token", "text, pos, ner")
FILENAME = "/Users/davidvalpey/practice/nlp_experiments/data/conll2002/ned.testb.gz"


def parse_conll2002(max_items=10) -> Token:
    with gzip.open(FILENAME, 'rt', encoding="ISO-8859-1") as zf:
        next(zf)
        for idx, line in enumerate(zf):
            if not line.strip():
                yield Token(None, None, None)
            else:
                yield Token(*line.split())
            if max_items and (idx > max_items):
                break


def prep_sentences(max_items=10) -> dict:
    sentence = []
    entities = []
    entity = []
    etype = ""

    for token in parse_conll2002(max_items):
        if token.text:
            sentence.append(token.text)
            if token.ner[0] in "BI":
                if token.ner[0] == "B":
                    etype = token.ner.split("-")[-1]
                entity.append(token.text)
            else:
                if entity:
                    entities.append(NamedEntity(entity=" ".join(entity), etype=etype))
                    entity = []
        else:
            if entity:
                entities.append(NamedEntity(entity=" ".join(entity), etype=etype))
                entity = []
            yield {"sentence": " ".join(sentence), "entities": entities}
            sentence = []
            entities = []
    if sentence:
        yield {"sentence": " ".join(sentence), "entities": entities}


if __name__ == '__main__':
    print(list(prep_sentences(max_items=100)))
