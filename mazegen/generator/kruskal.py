from .abcgenerator import ABCGenerator
from mazegen.grid import Grid, Cell, Directions
import random


class SetHolder(object):
    def __init__(self):
        self.parent_root = None

    def root(self):
        return self if self.parent_root is None else self.parent_root.root()

    def connected(self, other_set):
        return self.root() == other_set.root()
    
    def connect(self, other_set):
        other_set.root().parent_root = self


class Kruskal(ABCGenerator):
    # Reference: http://weblog.jamisbuck.org/2011/1/3/maze-generation-kruskal-s-algorithm
    def __init__(self):
        super(Kruskal, self).__init__()

    def generate(self, height, width):
        self.grid = Grid(height, width, Cell.OPEN)
        
        sets = [[SetHolder() for x in range(width)] for i in range(height)]

        # Create list of edges
        edges = []
        for i in range(0, self.grid.height, 1):
            for j in range(0, self.grid.width, 1):
                if i > 0:
                    edges.append([i, j, Directions.NORTH])
                if j > 0:
                    edges.append([i, j, Directions.WEST])
        
        # Randomize it
        random.shuffle(edges)

        while len(edges) > 0:
            edge = edges.pop(0)
            
            cell = (edge[0], edge[1])
            next_cell = Grid.get_next_cell(cell, edge[2])

            set1, set2 = sets[cell[0]][cell[1]], sets[next_cell[0]][next_cell[1]]
            if set1.connected(set2) is False:
                self.grid.set_passage(cell, next_cell, Cell.OPEN)
                set1.connect(set2)

        return self.grid
