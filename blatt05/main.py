#!/usr/bin/env python3
from blatt05.grid import a_star
from blatt05.grid.environment import Environment
from blatt05.grid.file_reader import char_lists_from_fn
from blatt05.grid.heuristics import PortalHeuristic2

env = Environment(char_lists_from_fn("input/blatt4_environment_b.txt"))

# heuristic = PortalHeuristic(env.portals, env.goals)
# heuristic = ManhattanDistance(env.goals)
heuristic = PortalHeuristic2(env.portals, env.goals)

solution, frames = a_star.find_path_rec(env, heuristic)
# solution, iterations, max_len = breadth_first.find_path(env)

print(solution)
# print("***")
# print("length: " + str(len(solution)))

# Animation(env, frames, heuristic).draw()
