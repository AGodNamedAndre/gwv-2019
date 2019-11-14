#!/usr/bin/env python3
from queue import PriorityQueue

import numpy

from blatt05.grid import breadth_first, depth_first, astar_first
from blatt05.grid.environment import Environment
from blatt05.grid.file_reader import char_lists_from_fn

# TODO init visualization
env = Environment(char_lists_from_fn("input/blatt3_environment.txt"))
print(astar_first.find_path_with_stats(env))
