from flair.data import Sentence
from flair.models import SequenceTagger
from transformers import pipeline

from conll2002.conll2002 import prep_sentences


def add_ner_predictions():
    hf_tagger = pipeline("ner", model="wietsedv/bert-base-dutch-cased-finetuned-conll2002-ner")
    flair_tagger = SequenceTagger.load("flair/ner-dutch-large")

    for sent in prep_sentences():
        sent["hf"] = hf_tagger(sent["sentence"])

        # careful, flair tagger replace the sentence in place.
        sentence = Sentence(sent["sentence"])
        flair_tagger.predict(sentence)
        sent["flair"] = sentence.get_spans()

        yield sent


if __name__ == '__main__':
    sents = list(add_ner_predictions())
    print(sents)
