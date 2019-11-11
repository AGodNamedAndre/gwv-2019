#!/usr/bin/env python3
class Node:
    """
    Node representation of x,y-coordinates
    TODO add comparison method for heuristics etc
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.x == other.x and self.y == other.y
        return False  # maybe go with 'NotImplemented'

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        # TODO base on f/g/h (cost, estimate or combination)
        pass

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return str((self.x, self.y))
