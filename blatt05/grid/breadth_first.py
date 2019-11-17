#!/usr/bin/env python3
import time

from collections import deque
from blatt05.grid.environment import Environment


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
    max_len = 0
    iterations = 0
    while frontier:
        if len(frontier) > max_len:
            max_len = len(frontier)
        iterations += 1
        # select and remove node from frontier
        path = frontier.popleft()
        node = path[0]
        # check if node is a goal state
        if env.check_goal(node):
            return path, iterations, max_len
        # update explored/closed set
        explored.add(node)
        # cycle checking - no neighbours that are on own path
        neighbours = [n for n in (env.neighbours(node)) if n not in explored]
        # add neighbours to frontier
        frontier.extend([[n] + path for n in neighbours])
    return None
