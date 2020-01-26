# 1-player state = Freie-Felder, (optional: Roll, ggf. Reroll#)
# 2-player state = (Freie Felder, Score), (Freie Felder, Score), Rerolls/Roll

# Initaler State ({FreieFelder},  Roll)
# Für quasi-Optimalität (der Entscheidungen) brauchen wir unseren aktuellen Score nicht


class RollNode:
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

    def generate_edges(self, g):
        return g.generate_roll_edges(self)

    def ev(self, g):
        return g.calculate_roll_node_ev(self)


class DecisionNode:
    def __init__(self, free, roll):
        self.free = free
        self.roll = roll

    def describe(self):
        join = ",".join(self.free)
        return f"{{{join}}},{self.roll}"

    def describe_simple(self):
        return f"{self.roll}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.describe()})"

    def __hash__(self):
        return self.free.__hash__() << 1 + self.roll

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.free == other.free and self.roll == other.roll

    def generate_edges(self, g):
        return g.generate_decision_edges(self)

    def ev(self, g):
        return g.calculate_decision_node_ev(self)
