from mazegen.grid import Grid, Directions, AttemptedPaths
from .abcprinter import ABCPrinter
from enum import Enum


MINIMUM_WIDTH = 3


class Borders(str, Enum):
    CROSS = '+',
    WALL_VERTICAL = '|',
    WALL_HORIZONTAL = '-',
    FREE_VERTICAL = ' ',
    FREE_HORIZONTAL = ' ',


class CellFiller(str, Enum):
    EMPTY_CELL = ' ',
    PATH_CELL = 'X',
    PATH_ATTEMPTED = '.'


class SmartPrinter(ABCPrinter):
    """Smarter printer class than SimplePrinter. Shows real number of cell per row"""
    
    def __init__(self, show_solution_path=False, show_attempted_paths=False):
        super(SmartPrinter, self).__init__(show_solution_path, show_attempted_paths)

    @staticmethod
    def _position_to_represent(max_number):
        positions = 1
        while max_number/10 > 1:
            positions += 1
            max_number //= 10
        return positions

    @staticmethod
    def _get_cell_representation(character: str, number, filler=''):
        padding = (number - len(filler)) // 2
        right_filler = (number - len(filler)) % 2
        return character[:] * padding + filler + character[:] * (right_filler + padding)

    def _do_real_print(self):
        result = []
        height = self.grid.height
        width = self.grid.width

        # Latest element in keys is the highest number we have to represent
        max_positions_occupied = 0

        # Little refactor for better attempt search
        temp_dict = AttemptedPaths()
        for attempt in self.path.attempted.keys():
            for cell in self.path.attempted[attempt]:
                if not temp_dict[cell[0]]:
                    temp_dict[cell[0]] = []
                temp_dict[cell[0]].append((cell[0], cell[1], attempt))
            max_positions_occupied = attempt

        max_positions_occupied = SmartPrinter._position_to_represent(max_positions_occupied)
        max_positions_occupied = max_positions_occupied if max_positions_occupied > MINIMUM_WIDTH else MINIMUM_WIDTH

        horizontal_wall = SmartPrinter._get_cell_representation(Borders.WALL_HORIZONTAL, max_positions_occupied)
        horizontal_free = SmartPrinter._get_cell_representation(Borders.FREE_HORIZONTAL, max_positions_occupied)
        path_cell = SmartPrinter._get_cell_representation(CellFiller.EMPTY_CELL, max_positions_occupied, CellFiller.PATH_CELL)
        empty_cell = SmartPrinter._get_cell_representation(CellFiller.EMPTY_CELL, max_positions_occupied)

        # Add superior border
        row_txt = ''
        for i in range(width):
            row_txt += Borders.CROSS + horizontal_wall

        row_txt += Borders.CROSS
        result.append(row_txt)

        # From now on every cell paints his lower and right border 
        # So no special inferior border handling
        for r in range(height):
            row_txt = Borders.WALL_VERTICAL
            inf_txt = Borders.CROSS
            for c in range(width):
                cc = (r, c)
                found = False
                number = None
                # row_txt += ' '
                if self.path is not None and (self.show_solution_path or self.show_attempted_paths):
                    if self.show_solution_path and cc in self.path.solution:
                        row_txt += path_cell
                    elif self.show_attempted_paths:
                        for cell in temp_dict[cc[0]]:
                            if (cell[0],cell[1]) == cc:
                                row_txt += SmartPrinter._get_cell_representation\
                                (CellFiller.EMPTY_CELL, max_positions_occupied, str(cell[2]))
                                break
                        else:
                            row_txt += empty_cell
                    else:
                        row_txt += empty_cell
                else:
                    row_txt += empty_cell

                # If not last column check if passage is open. 
                # Last column has always a wall
                if c != width - 1:
                    east_cell = Grid.get_next_cell(cc)
                    if self.grid.is_open(cc, east_cell):
                        row_txt += Borders.FREE_VERTICAL
                    else:
                        row_txt += Borders.WALL_VERTICAL
                else:
                    row_txt += Borders.WALL_VERTICAL

                # If not last row check if passage is open. 
                # Last row has always a walls
                if r != height - 1:
                    south_cell = Grid.get_next_cell(cc, Directions.SOUTH)
                    if self.grid.is_open(cc, south_cell):
                        inf_txt += horizontal_free
                    else:
                        inf_txt += horizontal_wall
                else:
                    inf_txt += horizontal_wall

                inf_txt += Borders.CROSS

            result.append(row_txt)
            result.append(inf_txt)

        return '\n'.join(result)
