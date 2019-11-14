#!/usr/bin/env python3
import heapq
import time
from functools import total_ordering

from blatt05.grid.environment import Environment

CYCLE_CHECKING = 'cc'
MULTIPLE_PATH_PRUNING = 'mpp'


@total_ordering
class Path:
    def __init__(self, path, env):
        self._env = env
        self._path = path
        self._total_estimate = env.total_estimate(path)
        self._node = path[0]

    #    def __cmp__(self, obj):
    #       if obj == None:
    #          return -1
    #     if not isinstance(obj, someClass):
    #        return -1

    def update_costs(self):
        self._total_estimate = self._env.total_estimate(self._path)

    def add_node(self, node):
        return Path([node] + self._path, self._env)

    def node(self):
        return self._node

    def path(self):
        return self._path

    def __eq__(self, other):
        return self._total_estimate == other._total_estimate

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self._total_estimate < other._total_estimate

    def __repr__(self):
        return "%s" % str(self._total_estimate)


class PriorityQueue:
    def __init__(self, inp):
        heapq.heapify(inp)
        self._queue = inp

    def popleft(self):
        return self._queue.pop(0)

    def extend(self, inp):
        [heapq.heappush(self._queue, n) for n in inp]

    def is_empty(self):
        return len(self._queue) == 0


def find_path_with_stats(env: Environment, mode=None):
    start_time = time.time()
    solution = find_path(env, mode)
    print("Took {} seconds.".format(time.time() - start_time))
    return solution


def find_path(env: Environment, mode=None):
    """
    Find a path between start and end nodes in the given environment

    :param mode: One of MPP, CC or None
    :param env: Environment to search for a path between start and end nodes
    :return: A solution path or None
    """
    # initialize search with single element starting paths

    frontier = PriorityQueue([Path([s], env) for s in env.starts()])
    explored = set()
    # while frontier not empty
    while not frontier.is_empty():
        # select and remove node from frontier
        path = frontier.popleft()
        node = path.node()
        # check if node is a goal state
        if env.check_goal(node):
            return path.path()
        # update explored/closed set
        explored.add(node)
        # add neighbours to frontier
        neighbours = env.neighbours(node)
        # cycle checking - no neighbours that are on own path
        if mode == CYCLE_CHECKING:
            neighbours = [n for n in neighbours if n not in path.path()]
        # multiple path pruning (already implies no cycles)
        if mode == MULTIPLE_PATH_PRUNING:
            neighbours = [n for n in neighbours if n not in explored]
        frontier.extend([path.add_node(n) for n in neighbours])
    return None
