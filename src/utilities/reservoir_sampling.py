"""
Sample of reservoir sampling methods taken from
https://en.wikipedia.org/wiki/Reservoir_sampling
"""
from math import exp, floor, log
from random import randint, random
from typing import Iterator


def simple_reservoir(sequence: Iterator, reservoir_size: int):
    """
    Naive version simply visits every number and generates a random indeex at
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


def optimized_reeservoir(sequence: Iterator, reservoir_size: int):
    """
    Optimized version visits every number but only stops at the next number
    calculated randomly, using a decreasing weight. Thus at each round the next
    number is farther away, but at a random interval.

    Modification may be necessary to read from actual streams.

    :param sequence: The sequence to be sampled
    :param reservoir_size: Number of items to sample
    :return: The random sample collected from the stream
    """
    reservoir = list()
    sequence = iter(sequence)
    while len(reservoir) < reservoir_size:
        reservoir.append(next(sequence))

    next_value = 0
    weight = exp(log(random()) / reservoir_size)
    while next_value < reservoir_size:
        next_value = next_value + floor(log(random()) / log(1 - weight)) + 1

    for idx, value in enumerate(sequence, start=reservoir_size):
        if idx == next_value:
            reservoir[randint(0, reservoir_size - 1)] = value
            next_value = next_value + floor(log(random()) / log(1 - weight)) + 1
            weight *= exp(log(random()) / reservoir_size)

    return reservoir
