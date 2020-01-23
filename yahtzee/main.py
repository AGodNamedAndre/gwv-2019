import matplotlib
import matplotlib.pyplot as plt
import networkx as nx

from fractions import Fraction

# nxkwargs = {'with_labels': True, 'node_color': 'w', 'node_shape': 'o', 'edgecolors': 'black'}

# Unicodes and unicorns
to_dice = {
    1: '\u2680',
    2: '\u2681',
    3: '\u2682',
    4: '\u2683',
    5: '\u2684',
    6: '\u2685'
}


# 1-player state = Freie-Felder, Score, ReRolls(?)
# 2-player state = (Freie Felder, Score), (Freie Felder, Score), Rerolls

class ExpansionNode:
    def __init__(self, free):
        self.free = free

    def describe(self):
        join = ",".join(self.free)
        return f"{{{join}}}"

    def describe_simple(self):
        join = ",".join(self.free)
        return f"{join}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.describe()})"

    def __hash__(self):
        return self.free.__hash__()

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.free == other.free


class DecisionNode():
    def __init__(self, free, roll):
        self.free = free
        self.roll = roll

    def describe(self):
        join = ",".join(self.free)
        return f"{{{join}}},{self.roll}"

    def describe_simple(self):
        # return f"{to_dice[self.roll]}"
        return f"{self.roll}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.describe()})"

    def __hash__(self):
        return self.free.__hash__() << 2 + self.roll

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.free == other.free and self.roll == other.roll


def roll_results():
    """

    :return: possible rolls and probabilities
    """
    return [(i, Fraction(1, 6)) for i in range(1, 7)]
    # return map(lambda x: (x, Fraction(1, 6)), range(1, 7))


# Warmup-Game 1) 2-Field (Double, Square) - Single Player

# Rules for scoreboard fields
rules = {
    'D': lambda x: 2 * x,
    'S': lambda x: x ** 2
}

# Initaler State ({FreieFelder},  Roll)
# Für quasi-Optimalität (der Entscheidungen) brauchen wir unseren aktuellen Score nicht
init_state = ExpansionNode(frozenset({'D', 'S'}))


# Find optimum decision for state: { free fields }


def expand_decisions(node: DecisionNode):
    """

    :param node: DecisionNode
    :return: List(Tuple(ExpansionNode, Score))
    """
    # expand state for all possible decisions
    return [(ExpansionNode(node.free - set(ff)), rules[ff](node.roll))
            for ff in node.free]


# expand unrolled node
def expand_rolls(node: ExpansionNode):
    """

    :param node: ExpansionNode
    :return: List(Tuple(DecisionNode, probability))
    """
    return [(DecisionNode(node.free, r), p)
            for (r, p) in roll_results()]


G = nx.DiGraph()

# refactor/clean-up -> function/package this
decision_nodes = []
roll_nodes = []
frontier = [init_state]
while frontier:
    head = frontier.pop()
    neighbors = []
    if isinstance(head, ExpansionNode) and head.free:
        roll_nodes.append(head)
        neighbors = expand_rolls(head)
    elif isinstance(head, DecisionNode) and head.free:
        decision_nodes.append(head)
        neighbors = expand_decisions(head)
    elif not head.free:
        roll_nodes.append(head)
        continue
    else:
        raise TypeError(f"{head.__class__.__name__} was unexpected!")
    if neighbors:
        frontier.extend(list(zip(*neighbors))[0])
        G.add_weighted_edges_from([(head, n, w) for (n, w) in neighbors])


# find max ev / best decisions leading to max ev
# 1) Expansion/Roll-Node: All edges are accumulated - EV(exp_node) = sum(EV(edges))
# 2) Decisions-Nodes: One path is taken - EV(dec_node) = max(EV(edges))
def maximize_ev(state: ExpansionNode):
    for (child, prob) in G[state].items():
        # sum child ev * prob
        print((child, prob))


maximize_ev(init_state)

G.graph['graph'] = {'rankdir': 'LR'}
pos = nx.nx_agraph.graphviz_layout(G, prog='dot')

# TODO draw different kind of nodes in other shapes (states = o, decisions = square, unexpanded = <|)
nx.draw_networkx_nodes(G, pos, decision_nodes, node_shape='s', node_color='w', edgecolors='black')
nx.draw_networkx_nodes(G, pos, roll_nodes, node_shape='o', node_color='w', edgecolors='black', node_size=400)
node_labels = dict([(n, f"{n.describe_simple()}") for n in G.nodes])
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)

nx.draw_networkx_edges(G, pos, G.edges)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, rotate=False, font_size=6, label_pos=0.7)

plt.axis('off')
plt.show()
