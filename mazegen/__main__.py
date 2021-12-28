from mazegen.generator.abcgrowingtree import ABCGrowingTree
from mazegen.generator.kruskal import Kruskal
from mazegen.generator.prim import Prim
from mazegen.generator.recursivebacktracker import RecursiveBacktracker
from mazegen.maze import Maze
from mazegen.generator.eller import Eller
from mazegen.printer.simpleprinter import SimplePrinter
from mazegen.printer.smartprinter import SmartPrinter
from mazegen.solver.wallflower import WallFlower

maze = Maze()
maze.generator = RecursiveBacktracker()
maze.generate(10, 30)

maze.entrance = (0, 0)
maze.finish = (maze.grid.height - 1, maze.grid.width - 1)

# print('Simple')
# maze.printer = SimplePrinter()
# print(maze)

print('Smart')
maze.solver = WallFlower()
maze.solve()
maze.printer = SmartPrinter()
print(maze)
