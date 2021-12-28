import numpy
from enum import IntEnum


class Cell(IntEnum):
    NOT_VISITED = -2
    WALL = -1
    OPEN = 0


class Directions(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


DX = {Directions.EAST: 1, Directions.WEST: -1, Directions.NORTH:  0, Directions.SOUTH: 0}
DY = {Directions.EAST: 0, Directions.WEST: 0, Directions.NORTH: -1, Directions.SOUTH: 1}

# OPPOSITE: useful?
OPPOSITE = {
    Directions.EAST: Directions.WEST,
    Directions.WEST: Directions.EAST,
    Directions.NORTH: Directions.SOUTH,
    Directions.SOUTH: Directions.NORTH
}


class AttemptedPaths(dict):
    def __missing__(self, key):
        return []


class FollowedPaths(object):
    def __init__(self, solution=None, attempted=None):
        self.solution = solution if solution is not None else list()
        self.attempted = attempted if attempted is not None else AttemptedPaths()


class CellDirection(object):

    def __init__(self, cell=None, direction=None):
        self.cell = cell
        self.direction = direction

    @staticmethod
    def get_cells(holders):
        for x in holders:
            yield x.cell


class Grid(object):
    def __init__(self, height, width, default_value=Cell.NOT_VISITED):
        self.height = height
        self.width = width
        self.H = height * 2 - 1
        self.W = width * 2 - 1

        self.grid = numpy.empty((self.H, self.W), dtype=numpy.dtype('i'))

        # Default: all fields not visited
        # Default connections: all walls
        for i in range(0, self.H, 1):
            for j in range(0, self.W, 1):
                if i % 2 != 0 or j % 2 != 0:
                    self.grid[i][j] = Cell.WALL
                if i % 2 == 0 and j % 2 == 0:
                    self.grid[i][j] = default_value

    def get_value(self, cell):
        coordinates = Grid._get_real_coordinates(cell)
        return self.grid[coordinates[0]][coordinates[1]]

    def set_value(self, cell, value):
        coordinates = Grid._get_real_coordinates(cell)
        self.grid[coordinates[0]][coordinates[1]] = value

    def is_open(self, cell_from, cell_to):
        if Grid._are_cells_adjacent(cell_from, cell_to):
            h, w = Grid._get_passage(cell_from, cell_to)
            return self.grid[h][w] == Cell.OPEN
        return False

    def set_passage(self, cell_from, cell_to, passage=Cell.OPEN):
        if Grid._are_cells_adjacent(cell_from, cell_to):
            pc = Grid._get_passage(cell_from, cell_to)
            self.grid[pc[0]][pc[1]] = passage

    def is_valid_cell(self, cell):
        return 0 <= cell[0] < self.height and 0 <= cell[1] < self.width

    def viable_cells(self, cell):
        """Returns reachable cells by a prefixed one and the corresponding directions"""
        cells = []
        for x in Directions:
            next_c = Grid.get_next_cell(cell, x)
            if self.is_valid_cell(next_c) and self.is_open(cell, next_c):
                cells.append(CellDirection(next_c, x))
        return cells

    @staticmethod
    def get_next_cell(cell, direction=Directions.EAST):
        return cell[0] + DY[direction], cell[1] + DX[direction]

    @staticmethod
    def get_relative_direction(previous, destination):
        if Grid._are_cells_adjacent(previous, destination):
            for direction in Directions:
                if destination == Grid.get_next_cell(previous, direction):
                    return direction

    @staticmethod
    def _get_real_coordinates(cell):
        return cell[0]*2, cell[1]*2

    @staticmethod
    def _are_cells_adjacent(cell_from, cell_to):
        return (cell_from[0] == cell_to[0] and abs(cell_from[1]-cell_to[1]) == 1) or \
               (cell_from[1] == cell_to[1] and abs(cell_from[0]-cell_to[0]) == 1)

    @staticmethod
    def _get_passage_coordinate(cell_from, cell_to):
        if cell_from == cell_to:
            return cell_from * 2
        elif cell_from < cell_to:
            return cell_from * 2 + 1
        else:
            return cell_to * 2 + 1

    @staticmethod
    def _get_passage(cell_from, cell_to):
        return Grid._get_passage_coordinate(cell_from[0], cell_to[0]), \
               Grid._get_passage_coordinate(cell_from[1], cell_to[1])


