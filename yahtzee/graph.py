import networkx as nx

from dice import roll_results
from node import RollNode, DecisionNode
from score import rules


class Graph:
    def __init__(self, initial_state):
        self.G = nx.DiGraph()
        self._root_node = initial_state
        self._decision_nodes = []
        self._roll_nodes = []
        self._edges_opt = []
        self.ev_cache = Cache(self.calculate_ev)

    @property
    def graph(self):
        return self.G

    @property
    def decision_nodes(self):
        return self._decision_nodes

    @property
    def roll_nodes(self):
        return self._roll_nodes

    @property
    def optimal_edges(self):
        return self._edges_opt

    def expand_graph(self):
        frontier = [self._root_node]
        while frontier:
            current_node = frontier.pop()
            if not current_node.free:
                # no free categories to fill
                self.roll_nodes.append(current_node)
                continue
            neighbors = []
            if isinstance(current_node, RollNode):
                self.roll_nodes.append(current_node)
                neighbors = self.expand_rolls(current_node)
            elif isinstance(current_node, DecisionNode):
                self.decision_nodes.append(current_node)
                neighbors = self.expand_decisions(current_node)
            else:
                raise TypeError(f"{current_node.__class__.__name__} was unexpected!")
            if neighbors:
                frontier.extend(list(zip(*neighbors))[0])
                self.G.add_weighted_edges_from([(current_node, n, w) for (n, w) in neighbors])

    def calculate_evs(self):
        return self.calculate_ev(self._root_node)

    # ### TODO: Move stuff into states/nodes ###

    # find max ev / best decisions leading to max ev
    # 1) Expansion/Roll-Node: All edges are accumulated - EV(roll_node) = sum(EV(edges))
    def ev_roll(self, state: RollNode):
        ev = 0
        for (v, w) in self.G[state].items():
            # sum(p_child * ev_child)
            ev += w['weight'] * self.ev_cache.get_or_calculate(v)
        # save all edges to opt
        return ev

    # 2) Decisions-Nodes: One path is taken - EV(dec_node) = max(EV(edges))
    def ev_decision(self, state: DecisionNode):
        ev = 0
        opt = None
        for (v, w) in self.G[state].items():
            # max(edge_value_child + ev_child)
            ev_cur = w['weight'] + self.ev_cache.get_or_calculate(v)
            if ev_cur > ev:
                ev = ev_cur
                opt = [state, v]
        # save opt edge to opt
        self._edges_opt.append(opt)
        return ev

    def calculate_ev(self, state):
        if isinstance(state, DecisionNode):
            return self.ev_decision(state)
        elif isinstance(state, RollNode):
            return self.ev_roll(state)
        raise TypeError(f"{state.__class__.__name__} was unexpected!")

    def expand_decisions(self, node: DecisionNode):
        """

        :param node: DecisionNode
        :return: List(Tuple(ExpansionNode, Score))
        """
        # expand state for all possible decisions
        return [(RollNode(node.free - set(ff)), rules[ff](node.roll))
                for ff in node.free]

    # expand unrolled node
    def expand_rolls(self, node: RollNode):
        """

        :param node: ExpansionNode
        :return: List(Tuple(DecisionNode, probability))
        """
        return [(DecisionNode(node.free, r), p)
                for (r, p) in roll_results()]


# Caching calculated evs
class Cache:
    def __init__(self, value_fun):
        self.values = {}
        self.edges_opt = []
        self.value_fun = value_fun

    def get_or_calculate(self, state):
        v = self.values.get(state)
        if not v:
            v = self.value_fun(state)
            self.values[state] = v
        return v
