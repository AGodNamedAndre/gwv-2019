#!/usr/bin/env python3


from blatt04.grid.file_reader import GridFileReader
from blatt04.grid.environment import Environment
from blatt04.grid.graph_search import GraphSearch

env = Environment(GridFileReader("../input/blatt3_environment.txt"))
search = GraphSearch(env, list())

# TODO init visualization
print(search.search())
