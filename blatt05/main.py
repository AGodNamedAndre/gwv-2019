#!/usr/bin/env python3

from blatt05.grid import astar_first
from blatt05.grid.environment import Environment
from blatt05.grid.file_reader import char_lists_from_fn
from blatt05.grid.heuristics import PortalHeuristic
from blatt05.grid.visualisation import Animation

env = Environment(char_lists_from_fn("input/blatt4_environment_b.txt"))

heuristic = PortalHeuristic(env.portals, env.goals)
# heuristic = ManhattanDistance(env.goals)

solution, frames = astar_first.find_path_rec(env, heuristic)
print(solution)
# print("***")
# print("length: " + str(len(solution)))

Animation(env, frames, heuristic).draw()
