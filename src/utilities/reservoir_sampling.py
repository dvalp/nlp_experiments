"""
Sample of reservoir sampling methods
"""
from random import randint
from typing import Iterator


def simple_reservoir(sequence: Iterator, reservoir_size: int):
    """
    Naive version simple visits every number and generates a random indeex at
    each step.

    More efficient methods are possible. Modification may be necessary to read
    from actual streams.

    :param sequence: The sequence to be sampled
    :param reservoir_size: Number of items to sample
    :return: The random sample collected from the stream
    """
    reservoir = list()
    sequence = iter(sequence)
    while len(reservoir) < reservoir_size:
        reservoir.append(next(sequence))

    for idx, value in enumerate(sequence, start=reservoir_size):
        rand_int = randint(0, idx)
        if rand_int < reservoir_size:
            reservoir[rand_int] = value

    return reservoir
