from collections import Counter

from flair.data import Sentence
from flair.models import SequenceTagger
from transformers import pipeline

from conll2002.conll2002 import prep_sentences

hf_tagger = pipeline("ner", model="wietsedv/bert-base-dutch-cased-finetuned-conll2002-ner")
flair_tagger = SequenceTagger.load("flair/ner-dutch-large")


def add_ner_predictions():
    for sent in prep_sentences():
        sent["hf"] = hf_tagger(sent["sentence"])

        # careful, flair tagger replace the sentence in place.
        sentence = Sentence(sent["sentence"])
        flair_tagger.predict(sentence)
        sent["flair"] = sentence.get_spans()

        yield sent


def evaluate_flair():
    for sent in prep_sentences():
        sentence = Sentence(sent["sentence"])
        flair_tagger.predict(sentence)
        flair_names = Counter(f"{span.text} {span.tag}" for span in sentence.get_spans("ner"))
        valid_names = Counter(f"{span.entity} {span.etype}" for span in sent["entities"])
        print("Good names:", valid_names)
        print("Pred names:", flair_names)


if __name__ == '__main__':
    sents = list(add_ner_predictions())
    print(sents)
