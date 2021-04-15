from flair.data import Sentence
from flair.models import SequenceTagger
from transformers import pipeline

from conll2002.conll2002 import prep_sentences

if __name__ == '__main__':
    nlp = pipeline("ner")
    tagger = SequenceTagger.load("flair/ner-dutch-large")

    for sent in prep_sentences():
        sentence = Sentence(sent["sentencee"])
        tagger.predict(sentence)
        sent["flair"] = sentence.get_spans()
