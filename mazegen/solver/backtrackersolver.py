from .abcrecursivesolver import ABCRecursiveSolver
import random


class BacktrackerSolver(ABCRecursiveSolver):

    def __init__(self):
        super(BacktrackerSolver, self).__init__()

    def _choose_next_cell(self, available_cells, current_direction=None):
        """Recursive backtracker randomizes the possible directions when it gets to choose one
        Current cell will not affect decision"""
        for x in random.sample(available_cells, len(available_cells)):
            yield x

