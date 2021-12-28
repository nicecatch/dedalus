

class Maze(object):
    """Main class. It holds a 2-dimensional Maze and relative parameters"""

    def __init__(self):
        self.generator = None  # ABCGenerator
        self.solver = None  # ABCSolver
        self.grid = None  # Grid
        self.printer = None  # ABCPrinter
        self.entrance = None  # Tuple
        self.finish = None  # Tuple
        self.path = None  # FollowedPaths

    def generate(self, height, width):
        self.grid = self.generator.generate(height, width)

    def solve(self):
        self.path = self.solver.solve(self.grid, self.entrance, self.finish)

    def __str__(self):
        return self.printer.do_print(self.grid, self.path)
