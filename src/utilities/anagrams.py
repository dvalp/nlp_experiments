from collections import defaultdict
from typing import NamedTuple


class AnagramInfo(NamedTuple):
    longest_key: str
    largest_list_key: str
    anagrams: dict[str, list[str]]


def get_anagrams(file_path="data/wordlist.txt"):
    anagrams = defaultdict(list)
    longest_key = ""
    largest_list_key = ""

    with open(file_path, "rt", newline="\n") as fp:
        for line in fp:
            key = "".join(sorted(line.strip()))
            anagrams[key].append(line.strip())
            if len(key) > len(longest_key):
                longest_key = key
            if len(anagrams.get(key, [])) > len(anagrams.get(largest_list_key, [])):
                largest_list_key = key
    return AnagramInfo(anagrams=anagrams, longest_key=longest_key, largest_list_key=largest_list_key)
