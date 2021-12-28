from abc import ABC, abstractmethod


class ABCPrinter(ABC):

    def __init__(self, show_solution_path=False, show_attempted_paths=False):
        self.grid = None
        self.path = None
        self.show_attempted_paths = show_attempted_paths
        self.show_solution_path = show_solution_path

    def do_print(self, grid, path):
        if grid is None:
            return ''
        self.grid = grid
        self.path = path
        return self._do_real_print()
    
    @abstractmethod
    def _do_real_print(self):
        pass

