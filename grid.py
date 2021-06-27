import random
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
        self.observer = GridView(self, surface)
        self.hints = []  # cannot change hint squares

    def get(self, x, y):
        return self.values[x][y]

    def in_row(self, y, value):
        row = []
        for col in self.values:
            row.append(col[y])
        try:
            row.index(value)
            return True
        except ValueError:
            return False

    def in_column(self, x, value):
        try:
            self.values[x].index(value)
            return True
        except ValueError:
            return False

    def in_subgrid(self, coords, value):
        subgrid = self.values[coords[0] // 3 * 3:coords[0] // 3 * 3 + 3]
        for col in subgrid:
            for val in col[coords[1] // 3 * 3: coords[1] // 3 * 3 + 3]:
                if val == value:
                    return True
        return False

    def is_valid(self, coords, value):
        return not (self.in_row(coords[1], value) or
                    self.in_column(coords[0], value) or
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
                self.values[x][y] = val
                if self.solve(x + 1, y):
                    return True

        self.values[x][y] = 0
        return False

    # creates sudoku puzzle with 17 hints (min num for unique solution)
    def populate(self):
        self.solve(0, 0)
        random.seed(a=random.randint(0, 100))  # create random seed
        for i in range(60):
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            while self.values[x][y] == 0:
                x = random.randint(0, 8)
                y = random.randint(0, 8)
            self.values[x][y] = 0
        self.observer.draw()

    def clear(self):
        self.hints = []
        for x in range(9):
            self.values[x] = [0] * 9

    def index(self, i):
        return self.values.index(i)

    def __iter__(self):
        return self.values.__iter__()
