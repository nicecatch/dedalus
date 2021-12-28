from abc import ABC, abstractmethod
from .abcgenerator import ABCGenerator
from mazegen.grid import Grid, Cell, Directions
import random


class ABCGrowingTree(ABCGenerator, ABC):

    def __init__(self):
        super(ABCGrowingTree, self).__init__()

    @abstractmethod
    def _choose_index(self, elements):
        return 0

    def generate(self, height, width):
        self.grid = Grid(height, width)

        # Select random coordinate,visit it and initialize pool
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        pool = [(y, x)]
        self.grid.set_value(pool[0], Cell.OPEN)
        # Create Directions array (needed to be shuffled)
        directions = [k for k in Directions]

        while len(pool) > 0:
            # Choose a cell from the pool
            chosen_index = self._choose_index(len(pool))
            cell = pool[chosen_index]

            # For every randomized direction build a road until no other roads are available
            for direction in random.sample(directions, len(directions)):

                # Get next cell and verify is valid
                next_cell = Grid.get_next_cell(cell, direction)

                # If it is valid, visit it, open wall and add cell to the pool
                if self.grid.is_valid_cell(next_cell) and self.grid.get_value(next_cell) == Cell.NOT_VISITED:
                    self.grid.set_value(next_cell, Cell.OPEN)
                    self.grid.set_passage(cell, next_cell)
                    pool.append(next_cell)

                    # Actual cell had a valid neighbour. Reset index and interrupt break so we can choose another index
                    chosen_index = None
                    break

            if chosen_index is not None:
                # If chosen_index is still valid it means it has no more valuable neighbour. Remove it
                pool.pop(chosen_index)

        return self.grid
