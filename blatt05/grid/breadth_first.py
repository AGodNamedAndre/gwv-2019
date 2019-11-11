#!/usr/bin/env python3
import time

from collections import deque
from .environment import Environment

CYCLE_CHECKING = 'cc'
MULTIPLE_PATH_PRUNING = 'mpp'


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
    frontier = deque([[s] for s in env.starts])
    explored = set()
    # while frontier not empty
    while frontier:
        # select and remove node from frontier
        path = frontier.popleft()
        node = path[0]
        # check if node is a goal state
        if env.check_goal(node):
            return path
        # update explored/closed set
        explored.add(node)
        # add neighbours to frontier
        neighbours = env.neighbours(node)
        # cycle checking - no neighbours that are on own path
        if mode == CYCLE_CHECKING:
            neighbours = [n for n in neighbours if n not in path]
        # multiple path pruning (already implies no cycles)
        if mode == MULTIPLE_PATH_PRUNING:
            neighbours = [n for n in neighbours if n not in explored]
        frontier.extend([[n] + path for n in neighbours])
    return None
