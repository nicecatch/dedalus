from .abcsolver import ABCSolver
from mazegen.grid import FollowedPaths, Grid, Directions
from abc import ABC, abstractmethod


class ABCRecursiveSolver(ABCSolver, ABC):
    def __init__(self):
        super(ABCRecursiveSolver, self).__init__()
        self.paths = FollowedPaths()
        self.attempt = 0

    @abstractmethod
    def _choose_next_cell(self, available_cells, current_direction=None):
        return []

    def solve(self, grid, entrance, finish):
        self.grid = grid
        self.entrance = entrance
        self.finish = finish

        self.attempt = 0
        self.paths = FollowedPaths()

        # Find solution
        self.proceed(entrance)

        self._optimize_paths()

        return self.paths

    def _get_new_attempt(self):
        self.attempt += 1
        return self.attempt

    def proceed(self, cell, previous=None):
        # Path we are following
        inner_path = list()
        inner_path.append(cell)
        available_cells = list()
        tentative = self._get_new_attempt()
        # Recursive until there is only one cell to visit
        while True:

            available_cells = self.grid.viable_cells(cell)
            # Remove cell we are coming from
            for x in available_cells:
                if previous == x.cell:
                    available_cells.remove(x)

            # If there is only one available cell we have to visit it
            if len(available_cells) == 1:
                previous = cell

                cell = available_cells.pop().cell
                inner_path.append(cell)

                if cell == self.finish:
                    self.paths.solution = inner_path
                    return True

            else:
                break

        # If no available direction it means we reached a dead end. Stop
        if len(available_cells) == 0:
            self.paths.attempted[tentative] = inner_path
            return False

        # We have more than one road to choose from.
        # If it is starting point fake first direction
        cd = Grid.get_relative_direction(previous, cell) if previous is not None else Directions.EAST
        for d in self._choose_next_cell(available_cells, current_direction=cd):

            if d.cell == self.finish:
                inner_path.append(d.cell)
                self.paths.solution = inner_path
                return True

            result = self.proceed(d.cell, cell)
            if result is True:
                # Exit found :)
                self.paths.solution = inner_path + self.paths.solution
                return result

        self.paths.attempted[tentative] += inner_path
        return False

    def _optimize_paths(self):
        sorted_keys = sorted(self.paths.attempted.keys())
        for i in range(len(sorted_keys)):
            self.paths.attempted[i+1] = self.paths.attempted[sorted_keys[i]]
            if i+1 != sorted_keys[i]:
                del self.paths.attempted[sorted_keys[i]]
