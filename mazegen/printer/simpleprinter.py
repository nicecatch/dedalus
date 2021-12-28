from mazegen.grid import Cell
from .abcprinter import ABCPrinter


class SimplePrinter(ABCPrinter):
    """Simple printing class. Shows ' ' for empty passage, '#' for closed wall"""

    def __init__(self):
        super(SimplePrinter, self).__init__()

    def _do_real_print(self):
        result = []
        # height = self.grid.height
        width = self.grid.width
        h = self.grid.H
        w = self.grid.W
        # Add superior border
        row_txt = ''
        for i in range(width*2+1):
            row_txt += '#'
        result.append(row_txt)

        # Fill grid
        row_txt = ''
        for i in range(h):
            row_txt = '#'
            for j in range(w):
                if self.grid.grid[i][j] == Cell.OPEN:
                    row_txt += ' '
                else:
                    row_txt += '#'
            row_txt += '#'
            result.append(row_txt)

        # Add last border
        row_txt = ''
        for i in range(width*2+1):
            row_txt += '#'
        result.append(row_txt)

        return '\n'.join(result)
