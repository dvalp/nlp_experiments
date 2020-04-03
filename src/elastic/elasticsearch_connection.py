import json

from elasticsearch import Elasticsearch

ES_CONTEXT = Elasticsearch([{'host': 'localhost', 'port': 9200}, ])
INDEX_NAME = "word_vector_index"


def create_word_vec_index():
    with open("elastic/elastic_mappings.json", "r") as f:
        mapping = json.load(f)["word_vectors"]

    ES_CONTEXT.indices.create(index=INDEX_NAME, body=mapping)
