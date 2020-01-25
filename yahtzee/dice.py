from fractions import Fraction


def roll_results():
    """

    :return: possible rolls and probabilities
    """
    return [(i, Fraction(1, 6)) for i in range(1, 7)]
    # return map(lambda x: (x, Fraction(1, 6)), range(1, 7))


class Roll():
    def __init__(self, dices):
        self.dices = dices

    def describe(self):
        return f"{self.dices}"

    def __repr__(self):
        return self.describe()

    def __hash__(self):
        return self.dices.__hash__()

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.dices == other.dices
