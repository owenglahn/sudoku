import random
import copy
from view_components import *


def create_randoms():
    random.seed(a=random.randint(0, 100))
    randoms = []
    for i in range(9):
        val = random.randint(1, 9)
        while val in randoms:
            val = random.randint(1, 9)
        randoms.append(val)
    return randoms


class Grid:
    def __init__(self, surface):
        self.values = []  # 9x9 empty board
        for x in range(9):
            self.values.append([0] * 9)
        self.hints = [(x, y) for x in range(9)
                      for y in range(9)]  # cannot change hint squares
        self.observer = GridView(self, surface)
        self.populate()

    def get(self, x, y):
        return self.values[x][y]

    def set_value(self, x, y, val):
        self.values[x][y] = val
        self.observer.cell_changed((x, y))

    def in_row(self, coords, value):
        row = []
        for col in self.values:
            row.append(col[coords[1]])
        del row[coords[0]]
        return value in row

    def in_column(self, coords, value):
        col = copy.deepcopy(self.values[coords[0]])
        del col[coords[1]]
        return value in col

    def in_subgrid(self, coords, value):
        subgrid = copy.deepcopy(
            self.values[coords[0] // 3 * 3:coords[0] // 3 * 3 + 3])
        subgrid[coords[0] % 3][coords[1]] = 0
        for col in subgrid:
            if value in col[coords[1] // 3 * 3: coords[1] // 3 * 3 + 3]:
                return True
        return False

    def is_valid(self, coords, value):
        return not (self.in_row(coords, value) or
                    self.in_column(coords, value) or
                    self.in_subgrid(coords, value))

    def solve(self, x, y):
        if x == 9:
            return self.solve(0, y + 1)
        if y == 9:
            return True
        if self.values[x][y] != 0:
            return self.solve(x + 1, y)
        for val in create_randoms():
            if self.is_valid((x, y), val):
                self.set_value(x, y, val)
                if self.solve(x + 1, y):
                    return True

        self.set_value(x, y, 0)
        return False

    def populate(self):
        self.solve(0, 0)  # solve empty board
        random.seed(a=random.randint(0, 100))  # create random seed
        # remove solved cells at random to create puzzle
        for i in range(60):
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            while self.values[x][y] == 0:
                x = random.randint(0, 8)
                y = random.randint(0, 8)
            self.values[x][y] = 0
            self.observer.cell_changed((x, y))
            # for debugging
            try:
                self.hints.remove((x, y))
            except ValueError:
                print((x, y))

        self.observer.draw()

    def clear(self):
        self.hints = []
        for x in range(9):
            self.values[x] = [0] * 9

    def index(self, i):
        return self.values.index(i)

    def __iter__(self):
        return self.values.__iter__()
