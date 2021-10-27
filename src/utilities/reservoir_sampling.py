"""
Sample of reservoir sampling methods
"""
from typing import Iterator


def simple_reservoir(sequence: Iterator, reservoir_size: int):
    reservoir = list()
    sequence = iter(sequence)
    while len(reservoir) < reservoir_size:
        reservoir.append(next(sequence))
