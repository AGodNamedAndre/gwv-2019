#!/usr/bin/env python3
import itertools
from typing import List, TypeVar, Set, Dict, Tuple

import matplotlib.font_manager as mfm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from blatt05.grid.node import Node

T = TypeVar('T')

WALKABLE = 0


def map_char(char: str) -> int:
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
        np.copyto(mat[i, 0:len(chars[i])], [map_char(c) for c in chars[i]])
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
        self._portals, self._numbered_portals = self.build_portals(chars)
        # create matrix with only walkable information
        self.matrix = np.transpose(matrix_from(chars))

    def build_portals(self, chars):
        portals = dict()
        mapped = dict()
        for c in range(1, 9):
            ps = positions(chars, str(c))
            mapped.update({c: ps})
            if len(ps) == 1:
                continue  # no disappearing in portals
            for src in ps:
                portals.update({src: [dest for dest in ps if dest is not src]})
        return portals, mapped

    @property
    def starts(self) -> List[Node]:
        return self._starts

    @property
    def goals(self):
        return self._goals

    @property
    def portals(self):
        return self._portals

    def check_goal(self, node: Node) -> bool:
        return node in self._goals

    def walkable(self, node: Node) -> bool:
        return self.matrix[node.x, node.y] == WALKABLE

    def neighbours(self, node: Node) -> Set[Node]:
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

    def draw(self, ax: Axes):
        ax.imshow(np.transpose(self.matrix), cmap=plt.cm.get_cmap('Greys'))
        ax.set_xlim(-0.5, self.matrix.shape[0] - 0.5)
        ax.set_ylim(-0.5, self.matrix.shape[1] - 0.5)
        ax.set_xticks(np.arange(0, self.matrix.shape[0], 1))
        ax.set_yticks(np.arange(0, self.matrix.shape[1], 1))
        ax.set_xticks(np.arange(0.5, self.matrix.shape[0] + 0.5, 1), minor=True)
        ax.set_yticks(np.arange(0.5, self.matrix.shape[1] + 0.5, 1), minor=True)
        ax.grid(which='minor', alpha=0.5)

        prop = mfm.FontProperties(fname='res/pp.ttf')
        for s in self.starts:
            ax.text(s.x, s.y, u"\u24C8", fontproperties=prop, fontsize=14,
                    horizontalalignment='center', verticalalignment='center')
            # ax.scatter(s.x, s.y, marker="$\\alpha$", color="green", s=200)
        for g in self._goals:
            ax.text(g.x, g.y, u"\u24BC", fontproperties=prop, fontsize=14,
                    horizontalalignment='center', verticalalignment='center')

        icons = {1: u"\u2460", 2: u"\u2461", 3: u"\u2462", 4: u"\u2463", 5: u"\u2464", 6: u"\u2465"}
        for c, ps in self._numbered_portals.items():
            for p in ps:
                ax.text(p.x, p.y, icons.get(c), fontproperties=prop, fontsize=14,
                        horizontalalignment='center', verticalalignment='center')

class GraphEnvironment:
    def __init__(self, nodes, edges: Dict[Tuple[Node, Node], int], starts, goals):
        self._edges = edges
        self.starts = starts
        self.goals = goals

    def neighbours(self, node):
        neighbours = []
        for edge, cost in self._edges.items():
            if edge[0] == node:
                neighbours.append((edge[1], cost))
        return neighbours

    def check_goal(self, node):
        return node in self.goals
