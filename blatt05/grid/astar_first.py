#!/usr/bin/env python3
import time
from functools import total_ordering
from queue import PriorityQueue
from typing import Set, List

from blatt05.grid.environment import Environment
from blatt05.grid.node import Node


def manhattan_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def heuristic(node, goals):  # use manhattan distance from now to goal
    return min([manhattan_distance(node, goal) for goal in goals])


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

    def node(self):
        return self._node

    def path(self):
        return self._path

    def total_estimate(self):
        return self._cost + self._estimate

    def __eq__(self, other):
        return self.total_estimate() == other.total_estimate()

    def __lt__(self, other):
        # (A) go easy on comparison:
        return self.total_estimate() < other.total_estimate()
        # (B) prefer actual low cost of a path
        # Probably doesn't help in the general case (only a fraction of paths should have equal f-value)
        # if self.total_estimate() < other.total_estimate():
        #     return True
        # elif self.total_estimate() > other.total_estimate():
        #     return False
        # else:
        #     return self._cost > other._cost

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
        frontier.put(Path([s], 0, heuristic(s, env.goals)))
    explored = set()
    # while frontier not empty
    iteration = 0
    while not frontier.empty():
        iteration += 1
        # select and remove node from frontier
        path = frontier.get()
        node = path.node()
        explored.add(node)
        # check if node is a goal state
        if env.check_goal(node):
            print("Iterations: " + str(iteration))
            print("Length of s: " + str(len(path.path())))
            return path.path()
        # (1) cycle checking (0-cost cycles can get ugly) - not needed due to path pruning
        # neighbours = [n for n in env.neighbours(node) if n not in path.path()]
        # (2) path pruning (because for a consistent heuristic, the first found path to a node is optimal)
        # otherwise: replace sub-paths to neighbours if they have a worse g(x)
        neighbours = [n for n in (env.neighbours(node)) if n not in explored]
        # add neighbours to frontier
        for n in neighbours:
            frontier.put(path.with_head(n, 1, heuristic(n, env.goals)))
    return None


def find_path_rec(env: Environment):
    frontier = [Path([s], 0, heuristic(s, env.goals)) for s in env.starts]
    explored = set()
    i = 0
    while frontier and not env.check_goal(frontier[0].node()):
        frontier, explored = find_next_step(env, heuristic, frontier, explored)
        i += 1
    print("After {} iterations: ".format(i))
    print(frontier)
    print(explored)
    if frontier:
        return frontier[0].path()
    else:
        return None


def find_next_step(env: Environment, heuristic, frontier: List[Path], explored: Set[Node]):
    # select and remove node from frontier
    path, *frontier = frontier
    # add current to closed
    explored = explored | {(path.node())}
    # (1) cycle checking (0-cost cycles can get ugly) - not needed due to path pruning
    # neighbours = [n for n in env.neighbours(node) if n not in path.path()]
    # (2) path pruning (because for a consistent heuristic, the first found path to a node is optimal)
    # otherwise: replace sub-paths to neighbours if they have a worse g(x)
    neighbours = [n for n in (env.neighbours(path.node())) if n not in explored]
    # add neighbours to frontier
    frontier = sorted([path.with_head(n, 1, heuristic(n, env.goals)) for n in neighbours] + frontier)
    return frontier, explored
