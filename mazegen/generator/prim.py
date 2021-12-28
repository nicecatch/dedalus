from .abcgrowingtree import ABCGrowingTree
import random


class Prim(ABCGrowingTree):
    def __init__(self):
        super(Prim, self).__init__()

    def _choose_index(self, elements):
        # Prim's algorithm: choose one random cell every iteration
        return random.randint(0, elements - 1)

