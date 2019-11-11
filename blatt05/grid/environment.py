#!/usr/bin/env python3
import itertools
import matplotlib.pyplot as plt
import numpy as np

from typing import List, Tuple, TypeVar
from .node import Node

T = TypeVar('T')

WALKABLE = 0


def mapchar(char: str) -> int:
    return {
        'x': 1,
        ' ': 0
    }.get(char, 0)


def matrix_from(chars: List[List[str]]) -> np.array:
    """
    Safely create a numpy array from a list of lists of characters,
    filling up with 'nan' to achieve matrix properties of shape N x M.

    :param chars: Linewise representation of a grid environment
    :return: numpy array with shape (height x (max-length width))
    """
    # create numpy array with dimensions
    h: int = len(chars)
    w: int = max(len(s) for s in chars)
    mat = np.full([h, w], np.nan)
    # manual copy with ranges to support non rectangular inputs
    for i in range(len(chars)):
        np.copyto(mat[i, 0:len(chars[i])], [mapchar(c) for c in chars[i]])
    return mat


def positions(chars: List[List[T]], value: T) -> List[Node]:
    # TODO less shit, more python (list comprehension, smart index func, ..)
    ps = list()
    for y in range(len(chars)):
        for x in range(len(chars[y])):
            if chars[y][x] == value:
                ps.append(Node(x, y))
    return ps


class Environment:

    def __init__(self, chars: List[List[str]]):
        # determine nodes of interest
        self._starts = positions(chars, 's')
        self._goals = positions(chars, 'g')
        self._portals = self.build_portals(chars)
        # create matrix with only walkable information
        self.matrix = np.transpose(matrix_from(chars))

    def build_portals(self, chars):
        portals = dict()
        for c in range(1, 9):
            ps = positions(chars, str(c))
            if len(ps) == 1:
                continue  # no disappearing in portals
            for src in ps:
                portals.update({src: [dest for dest in ps if dest is not src]})
        return portals

    @property
    def starts(self) -> List[Node]:
        return self._starts

    def check_goal(self, node: Node) -> bool:
        return node in self._goals

    def walkable(self, node: Node) -> bool:
        return self.matrix[node.x, node.y] == WALKABLE

    def neighbours(self, node: Node) -> List[Node]:
        walkables = filter(
            self.walkable,
            [Node(node.x + 1, node.y),  # rechts
             Node(node.x - 1, node.y),  # links
             Node(node.x, node.y + 1),  # unten
             Node(node.x, node.y - 1)]  # oben
        )
        destinations = itertools.chain.from_iterable(map(self.use_portals, walkables))
        return set(destinations)

    def use_portals(self, node):
        return self._portals.get(node, [node])

    def draw(self, ax):
        ax.imshow(np.transpose(self.matrix), cmap=plt.cm.get_cmap('Greys'))
        ax.set_xticks(np.arange(-0.5, self.matrix.shape[0] + 0.5, 1))
        ax.set_yticks(np.arange(-0.5, self.matrix.shape[1] + 0.5, 1))

        for s in self.starts:
            ax.scatter(s[0], s[1], marker="*", color="green", s=400)
        for g in self._goals:
            ax.scatter(g[0], g[1], marker="*", color="brown", s=400)
