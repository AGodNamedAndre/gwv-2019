import networkx as nx

from dice import roll_results, roll_probabilities, keep_combinations
from node import RollNode, DecisionNode
from score import rules

NUM_DICE = 2
NUM_REROLLS = 2

class Graph:
    def __init__(self, initial_state):
        self.G = nx.DiGraph()
        self._root_node = initial_state
        self._decision_nodes = []
        self._roll_nodes = []
        self._edges_opt = set()
        self.ev_cache = Cache(self.calculate_node_ev)

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

    def build_graph(self):
        frontier = [self._root_node]
        while frontier:
            current_node = frontier.pop()
            successor_edges = current_node.generate_edges(self)
            if successor_edges:
                frontier.extend([v for (u, v, w) in successor_edges])
                self.G.add_weighted_edges_from(successor_edges)

    def calculate_evs(self):
        return self.calculate_node_ev(self._root_node)

    def calculate_node_ev(self, state):
        return state.ev(self)

    # find max ev / best decisions leading to max ev
    # 1) Expansion/Roll-Node: All edges are accumulated - EV(roll_node) = sum(EV(edges))
    def calculate_roll_node_ev(self, state: RollNode):
        if not self.G[state].items():
            return 1
        ev = 0
        for (v, w) in self.G[state].items():
            # sum(p_child * ev_child)
            ev += w['weight'] * self.ev_cache.get_or_calculate(v)
        # save all edges to opt
        return ev

    # 2) Decisions-Nodes: One path is taken - EV(dec_node) = max(EV(edges))
    def calculate_decision_node_ev(self, state: DecisionNode):
        ev = 0
        opt = None
        for (v, w) in self.G[state].items():
            # max(edge_value_child + ev_child)
            ev_cur = w['weight'] * self.ev_cache.get_or_calculate(v)
            if ev_cur > ev:
                ev = ev_cur
                opt = (state, v)
        # save opt edge to opt
        if opt:
            self._edges_opt.add(opt)
        return ev

    def generate_decision_edges(self, node: DecisionNode):
        """
        Erzeugt die ausgehenden Kanten aus der gegebenen DeciscionNode.

        :param node: DecisionNode
        :return: List(Tuple(node, ExpansionNode, Score))
        """
        # expand state for all possible decisions
        self._decision_nodes.append(node)
        edges = []
        if node.rerolls > 0:
            # case: we still can reroll 0..num_dice dices
            edges = [(node, RollNode(node.free, node.rerolls - 1, k), 1)
                     for k in keep_combinations(node.roll)]
            print(edges)
        else:
            edges = [(node, RollNode(node.free - set(ff), NUM_REROLLS), rules[ff](node.roll))
                     for ff in node.free]
        return edges

    def generate_roll_edges(self, node: RollNode):
        """
        Erzeugt die ausgehenden Kanten aus der gegebenen RollNode.

        :param node: ExpansionNode
        :return: List(Tuple(node, DecisionNode, probability))
        """
        self._roll_nodes.append(node)
        if not node.free:
            return []
        else:
            edges = [(node, DecisionNode(node.free, tuple(sorted(list(node.keeper + roll))), node.rerolls), prob)
                     for (roll, prob) in roll_probabilities(NUM_DICE - len(node.keeper))]
            return edges


# Caching calculated evs
class Cache:
    def __init__(self, value_fun):
        self.values = {}
        # self.edges_opt = []
        self.value_fun = value_fun

    def get_or_calculate(self, state):
        v = self.values.get(state)
        if not v:
            v = self.value_fun(state)
            self.values[state] = v
        return v
