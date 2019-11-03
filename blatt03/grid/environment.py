#!/usr/bin/env python3
from typing import List, Tuple, TypeVar

from blatt03.grid.file_reader import GridFileReader

import matplotlib.pyplot as plt
import numpy as np

T = TypeVar('T')


def mapchar(char: str) -> int:
    return {
        'x': 1,
        ' ': 0
    }.get(char, 0)


def transform(chars: List[List[str]]) -> np.array:
    # create numpy array with dimensions
    h: int = len(chars)
    w: int = max(len(s) for s in chars)
    mat = np.full([h, w], np.nan)
    # manual copy with ranges to support non rectangular inputs
    for i in range(len(chars)):
        np.copyto(mat[i, 0:len(chars[i])], [mapchar(c) for c in chars[i]])
    return mat


def positions(chars: List[List[T]], value: T) -> List[Tuple[int, int]]:
    # TODO less shit, more python (list comprehension, smart index func, ..)
    ps = list()
    for y in range(len(chars)):
        for x in range(len(chars[y])):
            if chars[y][x] == value:
                ps.append((x, y))
    return ps


class Environment:

    def __init__(self, reader: GridFileReader):
        chars: List[List[str]] = reader.read()
        self.starts = positions(chars, 's')
        self.goals = positions(chars, 'g')
        self.matrix = np.transpose(transform(chars))

    def get_starts(self) -> List[Tuple[int, int]]:
        return self.starts

    def is_goal(self, node: Tuple[int, int]) -> bool:
        return node in self.goals

    def walkable(self, node: Tuple[int, int]) -> bool:
        return self.matrix[node[0]][node[1]] == 0

    def neighbours(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        return list(filter(
            self.walkable,
            [(node[0] + 1, node[1]),  # rechts
             (node[0] - 1, node[1]),  # links
             (node[0], node[1] + 1),  # unten
             (node[0], node[1] - 1)]  # oben
        ))

    def draw(self, ax):
        ax.imshow(np.transpose(self.matrix), cmap=plt.cm.get_cmap('Greys'))
        ax.set_xticks(np.arange(-0.5, self.matrix.shape[0] + 0.5, 1))
        ax.set_yticks(np.arange(-0.5, self.matrix.shape[1] + 0.5, 1))

        for s in self.starts:
            ax.scatter(s[0], s[1], marker="*", color="green", s=400)
        for g in self.goals:
            ax.scatter(g[0], g[1], marker="*", color="brown", s=400)
