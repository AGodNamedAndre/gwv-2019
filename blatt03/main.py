#!/usr/bin/env python3


from blatt03.grid.file_reader import GridFileReader
from blatt03.grid.environment import Environment
from blatt03.grid.graph_search import GraphSearch

env = Environment(GridFileReader("../input/blatt3_environment.txt"))
search = GraphSearch(env, list())

# TODO init visualization
print(search.search())


