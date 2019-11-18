#!/usr/bin/env python3
import itertools
from itertools import chain, combinations
from math import ceil
from typing import List, Dict

from blatt05.grid import a_star
from blatt05.grid.environment import GraphEnvironment
from blatt05.grid.node import Node


def manhattan_distance(a: Node, b: Node) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def manhattan_distance_to_nodes(node: Node, goals: List[Node]) -> int:
    return min([manhattan_distance(node, goal) for goal in goals])


# class PortalHeuristic():3

def powerset(iterable):  # TODO remove sets containing two directions of one portal
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, ceil(len(s) / 2) + 1))
    # return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


class ManhattanDistance:
    def __init__(self, goals):
        self._goals = goals

    def lower_bound(self, node: Node):
        return min([manhattan_distance(node, g) for g in self._goals])

    def lower_bound_path(self, node: Node):
        return min([(manhattan_distance(node, g), g) for g in self._goals])


class PortalHeuristic:
    # TODO BUG: Heuristik geht immer durch Portale
    def __init__(self, portals, goals):
        self._portals = portals
        self._goals = goals
        self._pset = list(powerset(list(portals.items()))) if len(portals.items()) > 0 else []
        self._heuristics = []
        self.make_heuristics()

    def manhattan_with_portals(self, path, goal):
        md = 0
        for i in range(len(path) - 1):
            md += manhattan_distance(path[i][1][0], path[i + 1][0])
        if path:
            return {'start': path[0][0], 'value': md + manhattan_distance(path[-1][1][0], goal)}
        else:
            return {'start': goal, 'value': 0}

    def make_heuristics(self):
        heuristics = []
        for subset in self._pset:
            for goal in self._goals:
                heuristics.append(self.manhattan_with_portals(subset, goal))
        if heuristics:
            self._heuristics = heuristics
        else:
            self._heuristics = [self.manhattan_with_portals([], g) for g in self._goals]

    def lower_bound(self, node):
        return min([manhattan_distance(node, mwp['start']) + mwp['value'] for mwp
                    in self._heuristics])

    def lower_bound_path(self, node):
        return min([(manhattan_distance(node, mwp['start']) + mwp['value'], mwp['start']) for mwp
                    in self._heuristics])

class PortalHeuristic2:
    def __init__(self, portals: Dict[Node, List[Node]], goals):
        # TODO portals: needs better structure - collection of edges?
        # build edges
        edges = dict()
        # buid portal 0-cost edges
        for src in portals.keys():
            for dest in portals.get(src):
                edges.update({(src, dest): 0})
        # build manhattan cost edges between nodes
        nodes = portals.keys() | goals
        for (n1, n2) in itertools.product(nodes, nodes):
            if n1 != n2 and not (n1, n2) in edges:
                edges.update({(n1, n2): manhattan_distance(n1, n2)})
        # find shortest paths to all nodes
        for n in nodes:
            # use real goals as starts, and node n as goals
            env = GraphEnvironment(nodes, edges, goals, [n])
            path, _ = a_star.find_path_rec(env, ManhattanDistance([n]))
            print("path: {}, cost: {}, full path: {}".format(path, path.total_estimate(), path.path))

    def lower_bound(self, node: Node):
        pass

    def lower_bound_path(self, node: Node):
        # Use this only for drawing the heuristic
        pass
