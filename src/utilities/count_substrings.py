from itertools import combinations_with_replacement


def count_unique_substrings(text: str):
    return len({text[start:end+1] for start, end in combinations_with_replacement(range(len(text)), 2)}) + 1
