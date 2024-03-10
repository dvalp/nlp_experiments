from typing import Iterable
import pickle
from pathlib import Path
from nltk.tokenize.punkt import PunktTrainer, PunktSentenceTokenizer, PunktParameters

from src.data_structures.atticus_project_data import AtticusFullContracts
from src.dataset_readers.atticus_contract_reader import read_pdfs

TOKENIZER_DIR = Path("/Users/dtv/practice/nlp_experiments/models/tokenizers")


def train_sentence_tokenizer(doc_reader: Iterable[AtticusFullContracts] = read_pdfs(), save_params: bool = True) -> PunktParameters:
    punkt_trainer = PunktTrainer()
    for doc in doc_reader:
        punkt_trainer.train(doc.text)

    tokenizer_params = punkt_trainer.get_params()
    if save_params:
        pickle.dump(tokenizer_params, TOKENIZER_DIR.open(mode="wb"))

    return tokenizer_params


def get_sententence_tokenizer(tokenizer_params: PunktParameters) -> PunktSentenceTokenizer:
    return PunktSentenceTokenizer(tokenizer_params)


