#### Example:  
  
        from mazegen.maze import Maze  
        from mazegen.generator.Eller import Eller  
        from mazegen.printer.SimplePrinter import SimplePrinter  
        from mazegen.printer.SmartPrinter import SmartPrinter  
  
        maze = Maze()  
        maze.generator = Eller()  
        maze.generate(5,12)  
         
        maze.entrance = (0, 0)
        maze.finish = (maze.grid.height - 1, maze.grid.width - 1)
        
        print('Simple')  
        maze.printer = SimplePrinter()  
        print(maze)  
  
        print('Smart')  
        maze.printer =  SmartPrinter()  
        print(maze)  
  
#### Sample Output:  
        Simple  
		#########################  
		#             # #   # # #  
		# ### # ####### ### # # #  
		# #   # # # #       #   #  
		# # # ### # # ### ### ###  
		# # # #   # # #   # #   #  
		# ####### # # # ### ### #  
		# # # #     # # #   # # #  
		# # # # ##### # ### # # #  
		#             #         #  
		#########################  
		Smart  
	+---+---+---+---+---+---+---+---+---+---+---+---+
        | O   O     |           |                   |   |
        +---+   +   +   +---+---+---+   +---+   +   +   +
        |     O |   |   | O   O   O |   |       |       |
        +---+   +---+   +   +   +   +---+---+   +---+   +
        |   | O   O   O | O |   | O   O |           |   |
        +   +---+---+   +   +---+---+   +---+   +---+---+
        |           | O   O     |     O | O   O   O |   |
        +   +   +---+---+   +---+---+   +   +---+   +   +
        |   |                   |     O   O |     O   O |
        +---+---+---+---+---+---+---+---+---+---+---+---+  
