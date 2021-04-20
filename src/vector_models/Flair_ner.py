from collections import Counter

import spacy
from flair.data import Sentence
from flair.models import SequenceTagger
from transformers import pipeline

from conll2002.conll2002 import prep_sentences

hf_tagger = pipeline("ner", model="wietsedv/bert-base-dutch-cased-finetuned-conll2002-ner")
flair_tagger = SequenceTagger.load("flair/ner-dutch-large")
spacy_tagger = spacy.load("nl_core_news_lg")


def add_ner_predictions():
    for sent in prep_sentences():
        sent["hf"] = hf_tagger(sent["sentence"])

        # careful, flair tagger replace the sentence in place.
        sentence = Sentence(sent["sentence"])
        flair_tagger.predict(sentence)
        sent["flair"] = sentence.get_spans()

        yield sent


def compare_predictions():
    for sent in prep_sentences():
        sentence = Sentence(sent["sentence"])
        flair_tagger.predict(sentence)
        spacy_sent = spacy_tagger(sent["sentence"])
        flair_names = Counter(f"{span.text} {span.tag}" for span in sentence.get_spans("ner"))
        valid_names = Counter(f"{span.entity} {span.etype}" for span in sent["entities"])
        hf_names = Counter(f"{span['word']} {span['entity'][2:].upper()}" for span in hf_tagger(sent["sentence"]))
        spacy_names = Counter(f"{ent.text} {ent.label_}" for ent in spacy_sent.ents)
        print("Good names:", valid_names)
        print("Pred names:", flair_names)
        print("HF names   :", hf_names)
        print("Spacy names:", spacy_names)


if __name__ == '__main__':
    sents = list(add_ner_predictions())
    print(sents)
