#!/usr/bin/env python3


from blatt04.grid.environment import Environment
from blatt04.grid.file_reader import char_lists_from_fn
from blatt04.grid.graph_search import GraphSearch

env = Environment(char_lists_from_fn("input/blatt4_environment_b.txt"))
search = GraphSearch(env, list())

# TODO init visualization
print("Solution: " + str(search.search()))
