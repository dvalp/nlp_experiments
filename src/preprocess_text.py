from collections import deque
from typing import Iterable, List, Union

import ftfy
from unidecode import unidecode


def fix_text(text: str) -> str:
    return unidecode(ftfy.fix_text(text))


def create_ngrams(tokens: Union[str, Iterable[str]], min_len=1, max_len=3) -> List[List[str]]:
    """
    On small samples, this method performs the most efficiently.
    TODO: Test on larger samples and compare with other methods.

    If input tokens are in a string, split the string. Then use a sliding
    window to collect the n-grams. It can also handle creating a range of
    n-grams sizes, allowing you to collect multiple sizes at the same time.
    Currently this is done as one pass for each size, but could be adjusted
    to handle all sizes in the same pass through the tokens.

    :param tokens: The tokens or string to use for collecting n-grams
    :param min_len: Minimum n-gram size
    :param max_len: Maximum n-gram size
    :return: List containing all n-grams
    """
    if isinstance(tokens, str):
        tokens = tokens.split()

    grams = []

    for i in range(min_len, max_len + 1):
        for j in range(len(tokens) - i + 1):
            grams.append(tokens[j:j + i])

    return grams


def create_deque_ngrams(tokens, min_len=1, max_len=3):
    if isinstance(tokens, str):
        tokens = tokens.split()

    grams = []

    for i in range(min_len, max_len + 1):
        ngram = deque(tokens[:i], maxlen=i)
        grams.append(list(ngram))
        for item in tokens[i:]:
            ngram.append(item)
            grams.append(list(ngram))

    return grams


def create_gen_ngrams(tokens, min_len=1, max_len=3):
    if isinstance(tokens, str):
        tokens = tokens.split()

    grams = []

    for i in range(min_len, max_len + 1):
        grams.extend(tokens[j:j + i] for j in range(len(tokens) - i + 1))

    return grams


def ngrams(sequence, min_len=1, max_len=3):
    for n in range(min_len, max_len + 1):
        gram = deque(sequence[:n], n)
        for item in sequence[n:]:
            gram.append(item)
            yield tuple(gram)


def ngrams_zip(text, n=3):
    ngram_groups = zip(*[text[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngram_groups]
