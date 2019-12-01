#!/usr/bin/env python3
from typing import Iterable, Any, Set, Dict, Callable

import networkx as nx

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
    def __init__(self, name, predicate: Callable[[Dict[str, Any]], bool], variables):
        self.name = name
        self.predicate = predicate
        self.variables = variables

    def __repr__(self):
        return self.name

    @property
    def scope(self):
        return self.variables

    def is_satisfiable(self, fixed, others):
        assignment = fixed
        domains = {o.name: o.domain for o in others}
        return self._rec_is_satisfiable(assignment, domains)

    # TODO @TailRecursion or something to protect the stack
    def _rec_is_satisfiable(self, assignment, domains: Dict[str, Set[Any]]):
        # all domains set to value
        if not domains:
            return self.is_satisfied(assignment)
        # otherwise fixate values recursive
        cur, *tail = domains
        print(domains)
        print(cur)
        print(tail)
        for v in cur[1]:
            assignment_with_v = assignment + {cur[0]: v}
            if self._rec_is_satisfiable(assignment_with_v, tail):
                return True
        return False

    def is_satisfied(self, assignment):
        return self.predicate(assignment)


def gac(vs, cs: Iterable[Constraint]):
    # put all edges (v, c) on open list/set
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


x = Variable('X', {1, 2, 3})
y = Variable('Y', {1, 2, 3})

# TODO lieber lokale Benamung der Variablen, e.g. {'X': x, 'Y': y} ?
x_smaller_y = Constraint("X<Y", lambda assignment: assignment['X'] < assignment['Y'], {x, y})

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
