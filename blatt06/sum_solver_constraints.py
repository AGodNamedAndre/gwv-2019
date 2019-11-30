from collections import deque
import numpy as np
from math import ceil


class Environment:
    def __init__(self, a, b, summe, v_range=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)):
        self._a = a
        self._b = b
        self._summe = summe
        self._symbols = set(a+b+summe)
        self._v_range = v_range
        # self._search_order = self.search_order()
        # self._search_space = self.search_space()
        self._search_string = self.search_string()

        self._init_variables = self.init_variables()

    def search_string(self):
        search_s = ''

        for i in range(max(len(self._a), len(self._b), len(self._summe))):
            search_s += self._a[-i] if len(self._a) > i else '0'
            search_s += self._b[-i] if len(self._b) > i else '0'
            search_s += self._summe[-i] if len(self._summe) > i else '0'

        return search_s

    def init_variables(self):
        values = {'0': [0]}
        for s in self._symbols:
            values[s] = self._v_range
        values[self._a[0]] = self._v_range[1:] if len(self._a) > 0 else self._v_range
        values[self._b[0]] = self._v_range[1:] if len(self._b) > 0 else self._v_range
        values[self._summe[0]] = self._v_range[1:] if len(self._summe) > 0 else self._v_range

        return values

    def get_neighbors(self, path):
        depth = path.get_depth() + 1
        symbol = self._search_string[depth]
        if symbol in path.get_symbols():
            return [{symbol: path.get_mapping()[symbol]}]

        if depth % 3 == 2:
            mapping = path.get_mapping()
            return [{symbol: mapping[self._search_string[depth-1]] + mapping[self._search_string[depth-2]]}]

        print(self._init_variables[symbol])
        return [{symbol: n} for n in self._init_variables[symbol]]

    def partial_sum_constraint(self, mapping, depth):
        depth = ceil(depth/3)
        a = self._a[-depth:]
        b = self._b[-depth:]
        summe = self._summe[-depth:]

        for symbol in mapping.keys():
            a.replace(symbol, str(mapping[symbol]))
            b.replace(symbol, str(mapping[symbol]))
            summe.replace(symbol, str(mapping[symbol]))

        return int(a) + int(b) == int(summe)

    def partial_sums_constraint(self, neighbors, mapping, depth, a0, a1):
        mapped_symbols = set(mapping.keys())
        constrain_matching_neighbors = []

        if a0 in mapped_symbols and a1 in mapped_symbols:
            for n in neighbors:
                tmp_mapping = mapping.copy()
                tmp_key = list(n.keys())[0]
                tmp_mapping[tmp_key] = n[tmp_key]

                if self.partial_sum_constraint(tmp_mapping, depth):
                    constrain_matching_neighbors.append(n)

        else:
            return neighbors

    def get_neighbors_matching_constraints(self, path):
        neighbors = self.get_neighbors(path)
        depth = path.get_depth() + 1
        shft = depth % 3

        s0 = self._search_string[depth-shft]
        s1 = self._search_string[depth-shft+1]
        s2 = self._search_string[depth-shft+2]

        if shft == 0:
            return self.partial_sums_constraint(neighbors, path.get_mapping(), depth, s1, s2)
        if shft == 1:
            return self.partial_sums_constraint(neighbors, path.get_mapping(), depth, s0, s2)

        return self.partial_sums_constraint(neighbors, path.get_mapping(), depth, s0, s1)

    def check_goal(self, path):
        if path.get_depth() % 3 != 2:
            return False

        try:
            variables_mapping = path.get_mapping()
            a = ''
            for s in self._a:
                a += str(variables_mapping[s])

            b = ''
            for s in self._b:
                b += str(variables_mapping[s])

            summe = ''
            for s in self._summe:
                summe += str(variables_mapping[s])

            return int(a) + int(b) == int(summe)
        except:
            return False


class Path:
    def __init__(self, mapping, depth=0):
        self._mapping = mapping
        self._depth = depth
        self._symbols = set(mapping.keys())

    def add(self, node):
        tmp_mapping = self._mapping.copy()
        key = list(node.keys())[0]
        tmp_mapping[key] = node[key]
        return Path(tmp_mapping, self._depth+1)

    def get_mapping(self):
        return self._mapping

    def get_depth(self):
        return self._depth

    def get_symbols(self):
        return self._symbols


def search(a, b, summe, v_range=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)):
    # initialize search with single element starting paths
    start_symb = a[-1]
    frontier = deque([Path({start_symb: v}) for v in v_range])
    env = Environment(a, b, summe)

    # while frontier not empty
    while frontier:
        # select and remove node from frontier
        path = frontier.popleft()
        # check if mapping is a goal
        if env.check_goal(path):
            return path
        # add neighbours to frontier
        neighbours = env.get_neighbors_matching_constraints(path)
        frontier.extendleft([path.add(n) for n in neighbours])

        print(path.get_mapping())
    return None

