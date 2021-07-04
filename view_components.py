'''
Implementation of observer design pattern
'''

import pygame
from grid import *

pygame.font.init()
font = pygame.font.SysFont("comicsans", 50)


class SolveButton(pygame.Rect):

    def __init__(self, pos, dims, grid, surface):
        super().__init__(pos[0], pos[1], dims[0], dims[1])
        self.grid = grid
        self.surface = surface

    def render(self):
        pygame.draw.rect(self.surface, (0, 255, 0), self)
        text = font.render("Solve", 1, (0, 0, 0))
        self.surface.blit(text, (320, 730))

    def handle_click(self):
        self.grid.solve(0, 0)
        # self.grid.observer.draw()


class Cell(pygame.Rect):

    def __init__(self, coords, val, bold, grid, surface):
        super().__init__(coords[0] * 80, coords[1] * 80, 80, 80)
        if val == 0:
            self.text = ''
        else:
            self.text = str(val)

        font.set_bold(bold)
        font.set_bold(False)

        self.surface = surface
        self.grid = grid
        self.coords = coords
        self.bold = bold

    def render(self):
        # black if valid entry, red otherwise
        if self.text.isdigit() and self.grid.is_valid(self.coords, int(self.text)):
            color = (0, 0, 0)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(self.surface, (255, 255, 255), self)
        font.set_bold(self.bold)
        txt_surface = font.render(self.text, 1, color)
        font.set_bold(False)
        self.surface.blit(txt_surface,
                          (self.centerx - 20, self.centery - 20))

    def highlight(self):
        pygame.draw.line(self.surface, (255, 0, 0), (
            self.coords[0] * 80, self.coords[1] * 80), ((self.coords[0] + 1) * 80, (self.coords[1]) * 80), 7)
        pygame.draw.line(self.surface, (255, 0, 0), (
            self.coords[0] * 80, self.coords[1] * 80), ((self.coords[0]) * 80, (self.coords[1] + 1) * 80), 7)
        pygame.draw.line(self.surface, (255, 0, 0), (
            (self.coords[0] + 1) * 80, self.coords[1] * 80), ((self.coords[0] + 1) * 80, (self.coords[1] + 1) * 80), 7)
        pygame.draw.line(self.surface, (255, 0, 0), (
            self.coords[0] * 80, (self.coords[1] + 1) * 80), ((self.coords[0] + 1) * 80, (self.coords[1] + 1) * 80), 7)

    # observer -> grid
    def update_cell(self, val):
        self.grid.values[self.coords[0]][self.coords[1]] = val

    # grid -> observer
    def cell_changed(self):
        if self.grid.get(self.coords[0], self.coords[1]) == 0:
            self.text = ''
            self.bold = False
        else:
            self.text = str(self.grid.get(self.coords[0], self.coords[1]))

    def handle_click(self):
        self.highlight()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key != pygame.K_RETURN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                        self.render()
                    elif event.unicode.isdigit() and int(event.unicode) in range(1, 10):
                        print(event.unicode)
                        self.text = event.unicode
                        self.render()
                else:
                    if self.text.isdigit():  # sanity check
                        self.update_cell(int(self.text))
                    else:
                        self.text = ''
                    return


class GridView:
    def __init__(self, grid, surface):
        self.grid = grid
        self.grid_view = []
        # initializes board of rects with origin in top left
        for x in range(9):
            self.grid_view.append([])
            for y in range(9):
                self.grid_view[x].append(
                    Cell((x, y), self.grid.get(x, y), (x, y) in self.grid.hints,
                         grid, surface))
        self.solve_btn = SolveButton((0, 720), (720, 60), grid, surface)
        # parent component
        self.surface = surface

    def get_cell(self, coords):
        return self.grid_view[coords[0]][coords[1]]

    # call-back method, grid -> observer
    def cell_changed(self, coords):
        self.get_cell(coords).cell_changed()

    def draw(self):
        for x in range(9):
            if x % 3 == 0:
                width = 7
            else:
                width = 3
            pygame.draw.line(self.surface, (0, 0, 0),
                             (x * 80, 0), (x * 80, 720), width)
            for y in range(9):
                if y % 3 == 0:
                    width = 7
                else:
                    width = 3
                self.get_cell((x, y)).render()  # draw cell
                pygame.draw.line(self.surface, (0, 0, 0),
                                 (0, y * 80), (720, y * 80), width)
        self.solve_btn.render()

    def get_square_coords(self, pos):
        return (pos[0] // 80, pos[1] // 80)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.solve_btn.collidepoint(pygame.mouse.get_pos()):
                self.solve_btn.handle_click()
            else:
                cell_coords = self.get_square_coords(pygame.mouse.get_pos())
                self.get_cell(cell_coords).handle_click()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.draw()
