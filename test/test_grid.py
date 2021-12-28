import pytest
from mazegen.grid import Grid, Cell


class GridHolder(object):
    def __init__(self, grid, height, width, default_value):
        self.grid = grid
        self.height = height
        self.width = width
        self.default_value = default_value


@pytest.fixture(scope='module', params=[(10, 10), (10, 20), (20, 10)])
def dimensions(request):
    return request.param


@pytest.fixture(scope='module', params=[Cell.NOT_VISITED, Cell.OPEN])
def default_value(request):
    return request.param


@pytest.fixture(scope='module')
def create_grid(dimensions, default_value):

    height = dimensions[0]
    width = dimensions[1]
    grid = Grid(height, width, default_value)

    return GridHolder(grid, height, width, default_value)


class TestGrid:

    def test_grid_default_value(self, create_grid):
        for i in range(create_grid.height):
            for j in range(create_grid.width):
                assert create_grid.grid.get_value((i,j)) == create_grid.default_value
