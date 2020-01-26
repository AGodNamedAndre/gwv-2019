import matplotlib.pyplot as plt
import networkx as nx

from graph import Graph
from node import DecisionNode, RollNode

# [x] DONE Warmup-Game MicroYahtzee (2-Fields: Double, Square, 1 Player)
# [x] ---- extend to: + Rerolls
# [ ] ---- extend to: + 2 Players (mit utility-3 am besten)
# [x] ---- extend to: + More Dice (Combinatorics)

# Mögliche Utility-Funktionen
# 1. max ev?
# 2. win probability
# 3. (Sehr) gute Approximation:
#       maximieren der Wahrscheinlichkeit, dass:
#       hero_score > *Exepected* opp_score

# Find optimum decision for state: { free fields }
init_state = RollNode(frozenset({'D', 'S'}), 1)

yahtzee_graph = Graph(init_state)
G = yahtzee_graph.graph

yahtzee_graph.build_graph()
yahtzee_graph.calculate_evs()

plt.figure(figsize=(18, 18))

G.graph['graph'] = {'rankdir': 'LR'}
pos = nx.nx_agraph.graphviz_layout(G, prog='dot')

nx.draw_networkx_nodes(G, pos, yahtzee_graph.decision_nodes, node_shape='s', node_color='w', edgecolors='black')
nx.draw_networkx_nodes(G, pos, yahtzee_graph.roll_nodes, node_shape='o', node_color='w', edgecolors='black',
                       node_size=400)
node_labels = dict([(n, f"\n\n\n{n.describe_simple()}") for n in G.nodes])
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)

node_ev = dict([(n, f"{yahtzee_graph.ev_cache.get_or_calculate(n)}") for n in G.nodes])
nx.draw_networkx_labels(G, pos, labels=node_ev, font_size=10, font_color='red')

nx.draw_networkx_edges(G, pos, G.edges)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, rotate=False, font_size=6, label_pos=0.7)

nx.draw_networkx_edges(G, pos, yahtzee_graph.optimal_edges, edge_color='red')

# plt.axis('off')
# plt.show()

# plt.savefig("plot.png", dpi=300)
