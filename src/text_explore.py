from typing import Collection, Dict, List, Tuple

from flashtext import KeywordProcessor
from thefuzz.process import extractWithoutOrder
from sklearn.feature_extraction.text import CountVectorizer


def get_vocab_counts(texts: Collection, max_ngrams: int = 2) -> Dict[str, int]:
    """
    Use CountVectorizer to get counts of all possible ngrams up to a given size
    from the collections of texts. Each item in the collection represents an
    individual document.

    This does not preprocess the text in any way. The ngrams will be calculated
    across sentence boundaries (ie, last word of one sentence and first word of
    next sentence will be grouped together).

    :param texts: Collection of documents to process
    :param max_ngrams: Maximum size for ngrams (more than 3 gets too large)
    :return: Dictionary of terms mapped to their counts across all documents
    """
    vectorizer = CountVectorizer(ngram_range=(1, max_ngrams))
    features = vectorizer.fit_transform(texts)

    return dict(zip(vectorizer.get_feature_names(), features.sum(axis=0).tolist()[0]))


def get_fuzzy_matches(search_term: str, term_counts: Dict[str, int], cutoff_score: int) -> List[Tuple[str, int]]:
    """
    Return all terms that are similar to the search terms using the cutoff
    score as a threshold for the similarity.

    This expects a dictionary like the one returned from get_vocab_counts(),
    but can use any dictionary where the keys should be matched against the
    search terms.

    :param term_counts: Dictionary where the keys should be used to match the search term
    :param search_term: Term to use for comparing similarity of dictionary keys
    :param cutoff_score: Threshold for minimum similarity to possible match terms
    :return: All terms that meet the minimum similarity threshold
    """
    return sorted(extractWithoutOrder(search_term, term_counts.keys(), score_cutoff=cutoff_score), key=lambda i: i[1],
                  reverse=True)


def drop_ngrams_with_keyword(texts: Collection[str], term: str) -> Collection:
    keyword_processor = KeywordProcessor()
    keyword_processor.add_keyword(term)

    return texts
