from collections import defaultdict


def get_anagrams(file_path="data/wordlist.txt"):
    anagrams = defaultdict(list)
    with open(file_path, "rt", newline="\n") as fp:
        for line in fp:
            anagrams["".join(sorted(line.strip()))].append(line.strip())
    return anagrams
