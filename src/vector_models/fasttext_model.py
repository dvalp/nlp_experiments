from typing import Collection, Iterator

import numpy as np
from bs4 import BeautifulSoup
from elasticsearch.helpers import streaming_bulk
from gensim.models import FastText
from gensim.summarization.textcleaner import get_sentences
from gensim.utils import simple_preprocess
from tqdm import tqdm

from elastic.elasticsearch_connection import INDEX_NAME, ES_CONTEXT

MODEL_PATH = "vector_models/fast_text_vectors/fast_text.mod"


def train_model(sentences: Collection[str], save_path=MODEL_PATH):
    model = FastText(size=100)
    model.build_vocab(sentences=sentences)
    model.train(sentences=sentences, total_examples=model.corpus_count, epochs=50)
    model.save(save_path)
    return model


def load_model(load_path=MODEL_PATH):
    try:
        return FastText.load(load_path)
    except FileNotFoundError as e:
        print("The model does not exist at this location, try creating it or "
              "use another path.")
        raise e


def create_training_sentences(training_pages: Iterator[str]):
    for page in training_pages:
        for sentence in get_sentences(page):
            yield simple_preprocess(sentence)


def vectorize_text(page: str, ft_model: FastText):
    tokens = simple_preprocess(page)
    vector = np.zeros(100)

    if tokens:
        for token in tokens:
            vector += ft_model.wv[token]
        return vector / len(tokens)

    return vector


def generate_data(pages, ft_model):
    for page in pages:
        yield {
            "_index": INDEX_NAME,
            "_op_type": "index",
            "page_text": page,
            "page_vector": list(vectorize_text(page, ft_model))}


def strip_tags(html_pages: Collection[str]):
    for page in html_pages:
        yield BeautifulSoup(page, "lxml").text


def bulk_index(document_set, ft_model):
    progress = tqdm(unit="pages", total=len(document_set))
    successes = 0
    for ok, action in streaming_bulk(client=ES_CONTEXT, actions=generate_data(document_set, ft_model)):
        progress.update(1)
        successes += ok
    print(f"Indexed {successes}/{len(document_set)} documents")
