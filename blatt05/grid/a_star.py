#!/usr/bin/env python3
import time
from functools import total_ordering
from queue import PriorityQueue
from typing import Set, List

from blatt05.grid.environment import Environment
from blatt05.grid.heuristics import manhattan_distance_to_nodes, PortalHeuristic, ManhattanDistance
from blatt05.grid.node import Node


@total_ordering
class Path:
    # TODO check out alternative data structures: recursive or algebraic data types
    def __init__(self, path, cost, estimate):
        self._path = path
        self._cost = cost
        self._estimate = estimate
        self._node = path[0]

    def with_head(self, node, cost, estimate):
        return Path([node] + self._path, self._cost + cost, estimate)

    @property
    def node(self):
        return self._node

    @property
    def path(self):
        return self._path

    def total_estimate(self):
        return self._cost + self._estimate

    def __eq__(self, other):
        return self == other

    def __lt__(self, other):
        # (A) go easy on comparison
        # return self.total_estimate() < other.total_estimate()
        # (B) prefer actual low cost of a path
        if self.total_estimate() < other.total_estimate():
            return True
        elif self.total_estimate() > other.total_estimate():
            return False
        else:
            return self._cost > other._cost

    def __repr__(self):
        return "(%s f=%s+%s)" % (self._node, self._cost, self._estimate)


def find_path_with_stats(env: Environment):
    start_time = time.time()
    solution = find_path(env)
    print("Took {} seconds.".format(time.time() - start_time))
    return solution


def find_path(env: Environment):
    """
    Find a path between start and end nodes in the given environment

    :param env: Environment to search for a path between start and end nodes
    :return: A solution path or None
    """
    # initialize search with single element starting paths

    frontier = PriorityQueue()
    for s in env.starts:
        frontier.put(Path([s], 0, manhattan_distance_to_nodes(s, env.goals)))
    explored = set()
    # while frontier not empty
    iteration = 0
    while not frontier.empty():
        iteration += 1
        # select and remove node from frontier
        path = frontier.get()
        node = path.node
        explored.add(node)
        # check if node is a goal state
        if env.check_goal(node):
            return path.path
        # (1) cycle checking (0-cost cycles can get ugly) - not needed due to path pruning
        # neighbours = [n for n in env.neighbours(node) if n not in path.path()]
        # (2) path pruning (because for a consistent heuristic, the first found path to a node is optimal)
        # otherwise: replace sub-paths to neighbours if they have a worse g(x)
        neighbours = [n for n in (env.neighbours(node)) if n not in explored]
        # add neighbours to frontier
        for n in neighbours:
            frontier.put(path.with_head(n, 1, manhattan_distance_to_nodes(n, env.goals)))
    return None


def find_path_rec(env: Environment, heuristic):
    # statistics
    iterations = 0
    frames = []

    # init
    # heuristic = PortalHeuristic(env.portals, env.goals)
    # heuristic = ManhattanDistance(env.goals)
    frontier = sorted([Path([s], 0, heuristic.lower_bound(s)) for s in env.starts])
    explored = set()
    max_len = 0

    while frontier and not env.check_goal(frontier[0].node):
        frontier, explored = find_next_step(env, heuristic.lower_bound, frontier, explored)

        # stats
        iterations += 1
        frames.append((frontier, explored))
        if len(frontier) > max_len:
            max_len = len(frontier)

    print("Termination after: {} iterations/expansions".format(iterations))
    print("Frontier size: {} paths".format(len(frontier)))
    print("Max frontier size in all runs: {} paths".format(max_len))

    if frontier:
        return frontier[0].path, frames
    else:
        return None, frames


def find_next_step(env: Environment, heuristic, frontier: List[Path], explored: Set[Node]):
    # select and remove node from frontier
    cur, *frontier = frontier
    # add current to closed
    explored = explored | {cur.node}
    # (0) multi path pruning: remove other paths to the current node (which have worse f-value)
    frontier = list(filter(lambda p: p.node != cur.node, frontier))
    # (1) cycle checking (0-cost cycles can get ugly) - not needed due to path pruning
    # neighbours = [n for n in env.neighbours(node) if n not in path.path()]
    # (2) path pruning (because for a consistent heuristic, the first found path to a node is optimal)
    # otherwise, for non-consisten heuristics: replace sub-paths to neighbours if they have a worse g(x)
    neighbours = [n for n in (env.neighbours(cur.node)) if n not in explored]
    # add neighbours to frontier
    frontier = sorted([cur.with_head(n, 1, heuristic(n)) for n in neighbours] + frontier)
    return frontier, explored
