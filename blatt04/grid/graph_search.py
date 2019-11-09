#!/usr/bin/env python3
from typing import Tuple, MutableSequence, Set, List, Any

from blatt04.grid.environment import Environment

import matplotlib.pyplot as plt


# TODO move to visualization pkg
def draw_path(ax, path):
    for vert in zip(path, path[1:]):
        draw_arrow(ax, vert[0], vert[1])


# TODO move to visualization pkg
def draw_arrow(ax, src, dest):
    ax.arrow(src[0], src[1], dest[0] - src[0], dest[1] - src[1], width=0.01, length_includes_head=True,
             head_width=0.1, head_length=0.1, color='blue')


class GraphSearch:
    """
    Init search algorithm with components
    """

    def __init__(self, env: Environment, frontier: List[Any]):
        self.drawing: bool = True
        self.environment: Environment = env
        self.explored: Set[Tuple[int, int]] = set()
        self.frontier: List[Tuple[Tuple[int, int], List[Tuple[int, int]]]] = frontier

        # Initialize frontier with Tuple(start, initial-path)
        # might get more complex e.g. Tuple((x,y), cost/g(p), path)
        for s in self.environment.starts:
            self.frontier.append((s, [s]))

    """
    :returns Union[None, Some(Solution)]
    
    Implementation based on: Generic graph search algorithm [Russel,Norvig: AIMA 3rd ed., 2010]
    1) (condition) the frontier is empty -> return failure
    2) choose a leaf node and remove it from the frontier
        implementation: use a datatype for frontier that embeds the choosing algorithm (e.g. Stack, Queue, ..)
    3) (condition) the node contains a goal state -> return solution
    4) add the node to the explored set
    5) expand the chosen node, adding the resulting nodes to the frontier 
        (condition): only if not in the frontier or explored set
    """

    def search(self):
        for i in range(100):
            # (1) frontier is empty -> return failure
            if not self.frontier:
                return None
            # (2) choose a leaf node and remove it from the frontier
            node, path = self.frontier.pop()
            # (3) node contains a goal state -> return solution
            if self.environment.is_goal(node):
                return path
            # (4) add the node to the explored set
            self.explored.add(node)
            # (5a) expand the chosen node (and filter out nodes already on frontier/visited)
            neighbours = [n for n in self.environment.neighbours(node)
                          if n not in [el[0] for el in self.frontier]
                          and n not in self.explored]
            # (5b) adding the resulting nodes to the frontier
            for n in neighbours:
                p = list(path)
                p.append(n)
                self.frontier.append((n, p))
            # (*) draw the current state of our search
            if self.drawing:
                self.draw()

    def draw(self):
        # TODO move this to somewhere#init_visualization
        fig = plt.figure(figsize=(13, 13 * self.environment.matrix.shape[1] / self.environment.matrix.shape[0]))
        plt.gca().invert_yaxis()
        # ..
        ax = fig.gca()

        # draw the environment itself
        self.environment.draw(ax)

        # draw the path on top of the frontier
        draw_path(ax, self.frontier[-1][1])

        # draw other nodes on frontier
        for f in self.frontier[0:-1]:
            ax.scatter(f[0][0], f[0][1], marker="x", color="green", s=500)

        # draw the explored nodes
        for e in self.explored:
            ax.scatter(e[0], e[1], marker="o", color="yellow", s=600)

        # display the plot to the user
        plt.grid(linestyle='dashed')
        plt.show()

        # TODO close correctly at some point in time and learn matplotlib
        plt.close()
