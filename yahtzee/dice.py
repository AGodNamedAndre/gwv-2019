from fractions import Fraction
from itertools import chain, combinations


def roll_results():
    """

    :return: possible rolls and probabilities
    """
    return [(i, Fraction(1, 6)) for i in range(1, 7)]
    # return map(lambda x: (x, Fraction(1, 6)), range(1, 7))


counting_dict = dict()

DICE_SIDES = 6


def roll_probabilities(num_dice):
    global counting_dict
    if num_dice not in counting_dict.keys():
        counting_dict[num_dice] = create_counting_dict(_roll_dice(num_dice))
    return [tuple(el) for el in counting_dict[num_dice].items()]


# erzeuge alle würfelergebnisse
# alle werden gesortet und in eine conting map/dict gelegt
def create_all_rolls(num_dice):
    return [tuple(x) for x in _roll_dice(num_dice)]


def _roll_dice(num_dice):
    if num_dice == 0:
        return [[]]

    output = []
    for i in range(1, DICE_SIDES + 1):
        next_roll = _roll_dice(num_dice - 1)
        for j in range(len(next_roll)):
            next_roll[j] = [i] + next_roll[j]
        output += next_roll
    return output


def create_counting_dict(rolls):
    counter = {}
    fraction = Fraction(1, len(rolls))
    for roll in rolls:
        roll.sort()
        key = tuple(roll)
        if key in counter.keys():
            counter[key] += fraction
        else:
            counter[key] = fraction
    return counter


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


# def reroll_combinations
def keep_combinations(roll):
    return set(list(powerset(roll)))


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
