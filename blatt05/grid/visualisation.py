#!/usr/bin/env python3
import os

import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.axes import Axes


def draw_path(ax, path):
    arrows = []
    edges = list(zip(path, path[1:]))
    for edge in edges:
        if edge == edges[-1]:
            arrows.append(draw_arrow(ax, edge[0], edge[1], pointy_end=True))
        else:
            arrows.append(draw_arrow(ax, edge[0], edge[1]))
    return arrows


def draw_arrow(ax: Axes, src, dest, pointy_end=False):
    if pointy_end:
        return ax.annotate("", xy=(dest.x, dest.y), xytext=(src.x, src.y),
                           arrowprops=dict(arrowstyle='-|>', edgecolor='black', facecolor='black'))
    else:
        return ax.annotate("", xy=(dest.x, dest.y), xytext=(src.x, src.y), arrowprops=dict(arrowstyle='-'))


def draw_frontier(ax, frontier):
    patches = []
    head, *tail = frontier
    for f in tail:
        patches.append(ax.scatter(f.node.x, f.node.y, marker='o', edgecolors="blue", color='none', s=50))
    patches.append(ax.scatter(head.node.x, head.node.y, marker='o', edgecolors="red", color='none', s=50))
    return patches


def draw_explored(ax, explored):
    patches = []
    for e in explored:
        patches.append(ax.scatter(e.x, e.y, marker='o', edgecolors="green", color='none', s=20))
    return patches


def draw_heuristic(ax, node, heuristic):
    h, to = heuristic.lower_bound_path(node)
    print(to)
    return [ax.annotate('', xy=(to.x, to.y), xytext=(node.x, node.y),
                        arrowprops=dict(arrowstyle='-|>', edgecolor='red', facecolor='red', linestyle=':'))]


class Animation:
    def __init__(self, env, frames, heuristic):
        self.fig, self.ax = plt.subplots()
        self.env = env
        self.heuristic = heuristic
        self.frames = frames
        self.patches = []

    def init_background(self):  # only required for blitting to give a clean slate.
        print("initing background")
        self.env.draw(self.ax)

    def draw_frame(self, idx):
        print('timestep {0}'.format(idx))
        self.ax.set_xlabel("iteration {}".format(min(idx, len(self.frames) - 1)))

        for p in self.patches:
            p.remove()
        self.patches = []

        frontier, explored = self.frames[min(idx, len(self.frames) - 1)]
        print("frontier: " + str(frontier))
        print("explored: " + str(explored))

        self.patches += draw_explored(self.ax, explored)
        self.patches += draw_frontier(self.ax, frontier)
        self.patches += draw_path(self.ax, frontier[0].path[::-1])
        self.patches += draw_heuristic(self.ax, frontier[0].node, self.heuristic)
        return self.patches

    def draw(self):
        self.init_background()
        delay = 500
        pause_time = 3000
        num_frames = len(self.frames) + round(pause_time / delay)
        anim = animation.FuncAnimation(self.fig, self.draw_frame, frames=50, interval=delay)
        # anim = animation.FuncAnimation(self.fig, self.draw_frame, init_func=self.init_background,
        #                                        interval=200, blit=True, save_count=num_frames)
        anim.save('output/yolo.gif', dpi=200, writer='imagemagick')

        os.system('start output/yolo.gif')
