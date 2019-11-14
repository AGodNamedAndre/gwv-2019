#!/usr/bin/env python3
import time
from functools import total_ordering
from queue import PriorityQueue

from blatt05.grid.environment import Environment


def manhattan_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def heuristic(node, goals):  # use manhattan distance from now to goal
    return min([manhattan_distance(node, goal) for goal in goals])

    # def total_estimate(self, path):
    #   return self.costs(path) + self.heuristic(path[0])


@total_ordering
class Path:
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
        return self.total_estimate() < other.total_estimate()
        # prefer actual low cost of a path
        # if self.total_estimate() < other.total_estimate():
        #     return True
        # elif self.total_estimate() > other.total_estimate():
        #     return False
        # else:
        #     return self._cost > other._cost

    def __repr__(self):
        return "(%s f=%s+%s)" % (self._node, self._cost, self._estimate)


# class PriorityQueue:
#     def __init__(self, inp):
#         heapq.heapify(inp)
#         self._queue = inp
#
#     def popleft(self):
#         return heapq.heappop(self._queue)
#
#     def extend(self, inp):
#         for n in inp:
#             heapq.heappush(self._queue, n)
#
#     def is_empty(self):
#         return len(self._queue) == 0
#
#     def __repr__(self):
#         return str(list(self._queue))
#

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
        # cycle checking (0-cost cycles can get ugly)
        neighbours = [n for n in env.neighbours(node) if n not in path.path()]
        # TODO can we do path pruning or will this hurt optimality?
        # neighbours = [n for n in neighbours if n not in explored]
        # add neighbours to frontier
        for n in neighbours:
            frontier.put(path.with_head(n, 1, heuristic(n, env.goals)))
    return None
