# 1-player state = Freie-Felder, (optional: Roll, ggf. Reroll#)
# 2-player state = (Freie Felder, Score), (Freie Felder, Score), Rerolls/Roll

# Initaler State ({FreieFelder},  Roll)
# Für quasi-Optimalität (der Entscheidungen) brauchen wir unseren aktuellen Score nicht


class RollNode:
    def __init__(self, free, rerolls, roll=tuple()):
        self.free = free
        self.rerolls = rerolls
        self.keeper = roll

    def describe(self):
        join = ",".join(self.free)
        return f"{{{join}}},{self.rerolls},{self.keeper}"

    def describe_simple(self):
        join = ",".join(self.free)
        return f"{join},{self.rerolls},{self.keeper}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.describe()})"

    def __hash__(self):
        return self.free.__hash__() * self.rerolls + self.keeper.__hash__()

    def __eq__(self, other):
        return self.__class__ == other.__class__ \
               and self.free == other.free and self.rerolls == other.rerolls and self.keeper == other.keeper

    def generate_edges(self, g):
        return g.generate_roll_edges(self)

    def ev(self, g):
        return g.calculate_roll_node_ev(self)


class DecisionNode:
    def __init__(self, free, roll, rerolls):
        self.free = free
        self.roll = roll
        self.rerolls = rerolls

    def describe(self):
        join = ",".join(self.free)
        return f"{{{join}}},{self.roll},{self.rerolls}"

    def describe_simple(self):
        return f"{self.roll},{self.rerolls}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.describe()})"

    def __hash__(self):
        # TODO be nicer to hash
        return self.free.__hash__() * self.rerolls + self.roll.__hash__()

    def __eq__(self, other):
        return self.__class__ == other.__class__ \
               and self.free == other.free and self.roll == other.roll and self.rerolls == other.rerolls

    def generate_edges(self, g):
        return g.generate_decision_edges(self)

    def ev(self, g):
        return g.calculate_decision_node_ev(self)
