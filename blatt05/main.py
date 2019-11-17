#!/usr/bin/env python3
from blatt05.grid import depth_first, breadth_first
from blatt05.grid.environment import Environment
from blatt05.grid.file_reader import char_lists_from_fn
from blatt05.grid.heuristics import ManhattanDistance

env = Environment(char_lists_from_fn("input/blatt3_environment.txt"))

# heuristic = PortalHeuristic(env.portals, env.goals)
heuristic = ManhattanDistance(env.goals)

# solution, frames = a_star.find_path_rec(env, heuristic)
solution, iterations, max_len = breadth_first.find_path(env)

print("Termination after: {} iterations/expansions".format(iterations))
print("Max frontier size in all runs: {} paths".format(max_len))
print(solution)
# print("***")
# print("length: " + str(len(solution)))

# Animation(env, frames, heuristic).draw()
