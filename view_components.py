'''
Implementation of observer design pattern
'''

import pygame
from grid import *

pygame.font.init()
font = pygame.font.SysFont("comicsans", 50)


class SolveButton(pygame.Rect):

    def __init__(self, pos, dims, grid):
        super().__init__(pos[0], pos[1], dims[0], dims[1])
        self.grid = grid

    def render(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self)
        text = font.render("Solve", 1, (0, 0, 0))
        surface.blit(text, (320, 730))

    def handle_click(self):
        self.grid.solve(0, 0)
        self.grid.observer.draw()


class GridView:
    def __init__(self, grid, surface):
        self.grid = grid
        self.grid_view = []
        # initializes board of rects with origin in top right
        for x in range(9):
            self.grid_view.append([])
            for y in range(9):
                self.grid_view[x].append(
                    pygame.Rect(x * 80, y * 80, 80, 80))
        self.solve_btn = SolveButton((0, 720), (720, 60), grid)
        # parent component
        self.surface = surface

    # draws board, adds lines
    def draw_grid(self):
        for row in range(9):
            if row % 3 == 0:
                h_width = 7
            else:
                h_width = 3
            pygame.draw.line(self.surface, (0, 0, 0),
                             (0, row * 80), (720, row * 80), h_width)
            for col in range(9):
                if col % 3 == 0:
                    v_width = 7
                else:
                    v_width = 3
                pygame.draw.rect(self.surface, (255, 255, 255),
                                 self.grid_view[col][row])
                pygame.draw.line(self.surface, (0, 0, 0),
                                 (col * 80, 0), (col * 80, 720), v_width)

    def draw(self):
        self.draw_grid()
        for col in self.grid:
            for val in col:
                if val != 0:
                    text = font.render(str(val), 1, (0, 0, 0))
                    self.surface.blit(text, (self.grid.index(
                        col) * 80 + 30, col.index(val) * 80 + 30))
        self.solve_btn.render(self.surface)

    def get_square_coords(self, pos):
        return (pos[0] // 80, pos[1] // 80)

    def highlight(self, coords):
        pygame.draw.line(self.surface, (255, 0, 0), (
            coords[0] * 80, coords[1] * 80), ((coords[0] + 1) * 80, (coords[1]) * 80), 7)
        pygame.draw.line(self.surface, (255, 0, 0), (
            coords[0] * 80, coords[1] * 80), ((coords[0]) * 80, (coords[1] + 1) * 80), 7)
        pygame.draw.line(self.surface, (255, 0, 0), (
            (coords[0] + 1) * 80, coords[1] * 80), ((coords[0] + 1) * 80, (coords[1] + 1) * 80), 7)
        pygame.draw.line(self.surface, (255, 0, 0), (
            coords[0] * 80, (coords[1] + 1) * 80), ((coords[0] + 1) * 80, (coords[1] + 1) * 80), 7)
