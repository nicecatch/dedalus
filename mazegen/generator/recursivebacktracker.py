from .abcgrowingtree import ABCGrowingTree


class RecursiveBacktracker(ABCGrowingTree):
    def __init__(self):
        super(RecursiveBacktracker, self).__init__()

    def _choose_index(self, elements):
        # Recursive Backtracker's algorithm: choose always last cell
        return elements - 1

