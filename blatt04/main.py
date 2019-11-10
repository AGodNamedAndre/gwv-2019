#!/usr/bin/env python3
from blatt04.grid import breadth_first, depth_first
from blatt04.grid.environment import Environment
from blatt04.grid.file_reader import char_lists_from_fn
from blatt04.grid.graph_search import GraphSearch

# TODO init visualization
env = Environment(char_lists_from_fn("input/blatt4_environment_b.txt"))
print("*** Breadth First Search ***")
print("Solution cycle checking:")
print(breadth_first.find_path_with_stats(env, breadth_first.CYCLE_CHECKING))
print("Solution multiple path pruning:")
print(breadth_first.find_path_with_stats(env, breadth_first.MULTIPLE_PATH_PRUNING))

# not needed for our impl, as mpp includes cc
# print("Solution multiple path pruning:")
# print("Solution with both MPP/CC: " + str(breadth_first.find_path_with_stats(env, breadth_first.CYCLE_CHECKING)))

print("*** Depth First Search ***")
print("Solution cycle checking:")
print(depth_first.find_path_with_stats(env, depth_first.CYCLE_CHECKING))
print("Solution multiple path pruning:")
print(depth_first.find_path_with_stats(env, depth_first.MULTIPLE_PATH_PRUNING))
