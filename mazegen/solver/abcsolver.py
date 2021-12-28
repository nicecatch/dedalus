from abc import ABC, abstractmethod


class ABCSolver(ABC):
    def __init__(self):
        self.grid = None
        self.entrance = None
        self.finish = None

    @abstractmethod
    def solve(self, grid, entrance, finish):
        pass
