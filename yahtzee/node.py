# 1-player state = Freie-Felder, Score, ReRolls(?)
# 2-player state = (Freie Felder, Score), (Freie Felder, Score), Rerolls

# Initaler State ({FreieFelder},  Roll)
# Für quasi-Optimalität (der Entscheidungen) brauchen wir unseren aktuellen Score nicht

# TODO: unify interface

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
        return self.free.__hash__() << 1 + self.roll

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.free == other.free and self.roll == other.roll
