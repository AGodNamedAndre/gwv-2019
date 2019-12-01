#!/usr/bin/env python3
from typing import Iterable

import networkx as nx
import matplotlib.pyplot as plt

words = ["add", "ado", "age", "ago", "aid", "ail", "aim", "air",
         "and", "any", "ape", "apt", "arc", "are", "ark", "arm",
         "art", "ash", "ask", "auk", "awe", "awl", "aye", "bad",
         "bag", "ban", "bat", "bee", "boa", "ear", "eel", "eft",
         "far", "fat", "fit", "lee", "oaf", "rat", "tar", "tie"]


class Variable:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain

    def __repr__(self):
        return f"{self.name}:{self.domain}"


class Constraint:
    # TODO variables ordered, same as constraint fun parameters -> for evaluation
    def __init__(self, name, constraint, variables):
        self.name = name
        self.constraint = constraint
        self.variables = variables

    def __repr__(self):
        return self.name

    @property
    def scope(self):
        return self.variables

    def is_satisfiable(self, value, others):
        # TODO
        return False

    def is_satisfied(self):
        # TODO
        return False


def gac(vs, cs: Iterable[Constraint]):
    # put all edges (v, c) on open list (TODO: set-like structure)
    to_do = {(v, c) for c in cs for v in c.scope}
    while to_do:
        # current tuple of (V, C)
        (v, c) = to_do.pop()
        # other Vs connected to C
        others = c.scope - {v}
        # find new domain for current v
        new_dom = {value for value in v.domain if c.is_satisfiable({v: value}, others)}
        print(new_dom)
        # if domain for v is changed
        if not v.domain == new_dom:
            # mark all other constraints that use v as dirty
            print(f"Old domain: {v}, new domain: {new_dom}")
            to_do.update([(v_other, c_other) for c_other in cs for v_other in c_other.scope
                          if c_other != c and v_other != v])
            v.domain = new_dom
            print(f"{c} and {others}")
    return {v for c in cs for v in c.variables}


x = Variable("X", {1, 2, 3})
y = Variable("Y", {1, 2, 3})

x_smaller_y = Constraint("X<Y", lambda lh, rh: lh < rh, {x, y})

G = nx.Graph()
G.add_edge(x, x_smaller_y)
G.add_edge(y, x_smaller_y)

print(gac({x, y}, {x_smaller_y}))

# labeldict = {}
# labeldict[x] = r'$X$'
# labeldict[y] = r'$Y$'
# labeldict[x_smaller_y] = r'$X<Y$'
#
# nx.draw(G, labels=labeldict, with_labels=True,
#         node_size=1000, font_size=12, node_shape='s', node_color='orange')
# plt.show()
