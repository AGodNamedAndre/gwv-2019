import networkx as nx

class Environment:
    def __init__(self, a, b, summe):
        self._a = a
        self._b = b
        self._summe = summe
        self._symbols = set(a+b+summe)
        # self._search_order = self.search_order()
        self._search_space = self.search_space()
        self._search_string = self.search_string()
        self._search_order = self.search_order()
        self._graph = self.make_graph()
        self._partial_sum_depth_dict = self.get_parital_sum_depth_dict()

        self._init_variables = self.init_variables()

    def init_variables(self):
        values = {'0': [0]}
        for s in self._symbols:
            values[s] = self._v_range
        values[self._a[0]] = self._v_range[1:] if len(self._a) > 0 else self._v_range
        values[self._b[0]] = self._v_range[1:] if len(self._b) > 0 else self._v_range
        values[self._summe[0]] = self._v_range[1:] if len(self._summe) > 0 else self._v_range

        return values

    def search_string(self):
        search_s = ''

        for i in range(max(len(self._a), len(self._b), len(self._summe))):
            search_s += self._a[i] if len(self._a[i]) > i else '0'
            search_s += self._b[i] if len(self._b[i]) > i else '0'
            search_s += self._summe[i] if len(self._summe[i]) > i else '0'

        return search_s

    def search_order(self):
        order = []
        is_set = set()

        for i in range(max(len(self._a), len(self._b), len(self._summe))):
            if not self._a[i] in order and not self._a[i] in is_set and len(self._a) > i:
                order.append(self._a[i])

            if not self._b[i] in order and not self._b[i] in is_set and len(self._b) > i:
                order.append(self._a[i])

            if not self._summe[i] in order and len(self._summe) > i:
                is_set.add(self._summe[i])

        return order

    def make_graph(self):
        graph = []
        for i in range(len(self._search_order)-1):
            a = self._search_order[i]
            b = self._search_order[i+1]
            for n_a in self._init_variables[a]:
                for n_b in self._init_variables[b]:
                    graph.append(('{}_{}'.format(a, n_a), '{}_{}'.format(b, n_b)))

        return nx.DiGraph(graph)

    def get_parital_sum_depth_dict(self):
        _set = set()
        _dict = {}

        for i in range(max(len(self._a), len(self._b), len(self._summe))):
            if len(self._a[i]) > i:
                _set.add(self._a[i])
            if len(self._a[i]) > i:
                _set.add(self._b[i])
            if len(self._a[i]) > i:
                _set.add(self._summe[i])

            _dict[str(i)] = len(_set)

        return _dict

    def get_parital_sum_depth(self, mapped):
        _dict = self._partial_sum_depth_dict
        for i in range(len(_dict.keys())):
            if len(_dict[str(i)]) > mapped:
                return i-1

    def partial_sum_constraint(self, mapping):
        depth = self.get_parital_sum_depth(len(mapping.keys()))

        a = self._a[-depth:]
        b = self._b[-depth:]
        summe = self._summe[-depth:]

        for symbol in mapping.keys():
            a.replace(symbol, str(mapping[symbol]))
            b.replace(symbol, str(mapping[symbol]))
            summe.replace(symbol, str(mapping[symbol]))

        return int(a) + int(b) == int(summe)

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
