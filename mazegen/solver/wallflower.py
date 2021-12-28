from .abcrecursivesolver import ABCRecursiveSolver
from mazegen.grid import Directions

WallFlowerDirections = [Directions.EAST, Directions.NORTH, Directions.WEST, Directions.SOUTH]
Shifts = {
    Directions.SOUTH: 2,
    Directions.EAST: 3,
    Directions.NORTH: 0,
    Directions.WEST: 1
}


class WallFlower(ABCRecursiveSolver):

    def __init__(self):
        super(WallFlower, self).__init__()

    def _choose_next_cell(self, available_cells, current_direction=None):
        """WallFlower always tries to turn right when possible"""
        ordered_directions = []
        if current_direction is None:
            ordered_directions = WallFlowerDirections
        else:
            ordered_directions = \
                WallFlowerDirections[Shifts[current_direction]:] + WallFlowerDirections[:Shifts[current_direction]]
        return sorted(available_cells, key=lambda x: ordered_directions.index(x.direction))
