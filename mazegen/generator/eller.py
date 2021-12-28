from .abcgenerator import ABCGenerator
from mazegen.grid import Grid, Cell, Directions
import random


class Eller(ABCGenerator):

    def __init__(self, xbias=0.5, ybias=0.5):
        super(Eller, self).__init__()
        self.xbias = xbias
        self.ybias = ybias
        self._current_set = 0

    def _get_new_set(self):
        self._current_set += 1
        return self._current_set

    def _merge_different_sets(self, current_row, final_set, from_set):
        """Move all cells in a given set to another set"""

        # Since older rows are no more important, ignore them
        for j in range(0, self.grid.width, 1):
            cell = (current_row, j)
            if self.grid.get_value(cell) == from_set:
                self.grid.set_value(cell, final_set)
    
    def _standardize_grid(self):
        for i in range(0, self.grid.height, 1):
            for j in range(0, self.grid.width, 1):
                self.grid.set_value((i, j), Cell.OPEN)

        return self.grid

    def generate(self, height, width):

        self.grid = Grid(height, width)

        for i in range(0, self.grid.height, 1):
            
            for j in range(0, self.grid.width, 1):
                cc = (i, j)
                # If no set assign one
                if self.grid.get_value(cc) == Cell.NOT_VISITED:
                    self.grid.set_value(cc, self._get_new_set())

                # If not last row
                # If not last column
                # If bias
                # If not same set
                # => join
                if i < self.grid.height - 1 and j < self.grid.width - 1 and random.random() < self.xbias:

                    next_cell = Grid.get_next_cell(cc, Directions.EAST)

                    if self.grid.get_value(next_cell) == Cell.NOT_VISITED:
                        self.grid.set_value(next_cell, self._get_new_set())

                    if self.grid.get_value(cc) != self.grid.get_value(next_cell):
                        self.grid.set_passage(cc, next_cell)
                        self._merge_different_sets(i, self.grid.get_value(cc), self.grid.get_value(next_cell))

            # Vertical join if not last row
            if i != (self.grid.height - 1):
                # First join at least one cell per set
                sets = {}
                columns_not_joined = []
                for j in range(0, self.grid.width, 1):
                    temp = self.grid.get_value((i, j))
                    if temp not in sets:
                        sets[temp] = [j]
                    else:
                        sets[temp] += [j]
                for s in sets:
                    j = random.choice(sets[s])

                    # If only one element within the set I will ignore him for sure (already joined vertically)
                    if len(sets[s]) > 1:
                        columns_not_joined += [x for x in sets[s] if x != j]

                    cell = (i, j)
                    next_cell = Grid.get_next_cell(cell, Directions.SOUTH)
                    self.grid.set_passage(cell, next_cell)
                    self.grid.set_value(next_cell, s)

                # Random join others cells
                # Bias must be adjusted in order to avoid to create too many vertical joins
                # (Every set has already one)
                for j in columns_not_joined:
                    if random.random() < self.ybias * len(columns_not_joined) / self.grid.width:
                        cell = (i, j)
                        s = self.grid.get_value(cell)
                        south = Grid.get_next_cell(cell, Directions.SOUTH)
                        if self.grid.get_value(south) == Cell.NOT_VISITED:
                            self.grid.set_passage(cell, south)
                            self.grid.set_value(south, s)
            else:
                # If last row join adjacent cells from different sets
                for j in range(self.grid.width - 1, 0, -1):
                    
                    cell = (i, j)
                    if self.grid.get_value(cell) == Cell.NOT_VISITED:
                        self.grid.set_value(cell, self._get_new_set())

                    next_cell = Grid.get_next_cell(cell, Directions.WEST)
                    if self.grid.get_value(next_cell) == Cell.NOT_VISITED:
                        self.grid.set_value(next_cell, self._get_new_set())

                    if self.grid.get_value(cell) != self.grid.get_value(next_cell):
                        self.grid.set_passage(cell, next_cell)
                        self._merge_different_sets(i, self.grid.get_value(cell), self.grid.get_value(next_cell))

        # Return a standardized grid
        return self._standardize_grid()
