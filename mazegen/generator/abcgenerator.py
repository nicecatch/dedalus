from abc import ABC, abstractmethod


class ABCGenerator(ABC):

    def __init__(self):
        self.grid = None
    
    @abstractmethod
    def generate(self, height, width):
        pass
