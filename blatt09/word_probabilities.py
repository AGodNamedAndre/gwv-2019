#!/usr/bin/env python3
from random import randrange
from typing import Dict, Set, TypeVar

T = TypeVar('T')

fn = 'res/short.txt'


def parse_file():
    # prev = {}  # preveiling form word
    # post = {}  # posterior from word
    bigrams = {}
    meta = {}

    with open(fn, 'r', encoding='utf-8') as f:

        text = ['<start>']
        for line in f:
            if not line.strip():
                text.append('<end>')
                text.append('<start>')
            else:
                text.append(line.strip())

        for i in range(1, len(text) - 1):
            prev = text[i - 1].strip()
            cur = text[i].strip()

            if (prev, cur) not in bigrams:
                bigrams[(prev, cur)] = 1
                if prev not in meta:
                    meta[prev] = set()
                    meta[prev].add((prev, cur))
                else:
                    meta[prev].add((prev, cur))
            else:
                bigrams[(prev, cur)] += 1

    return meta, bigrams


def draw_word(keys: Set[T], frequencies: Dict[T, int]) -> T:
    words = [(k, frequencies.get(k)) for k in keys]
    s = sum([w[1] for w in words])
    if s is 1:
        return words[0][0]
    r = randrange(1, s)
    sum_of_probs = 0
    for w in words:
        sum_of_probs += w[1]
        if sum_of_probs >= r:
            return w[0]


meta, bigrams = parse_file()

comment = ['<start>']

while comment[-1] != '<end>':
    b = draw_word(meta[comment[-1]], bigrams)
    comment.append(b[1])

print(comment)
