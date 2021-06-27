import pygame
import sys
import grid

pygame.init()

size = width, height = 720, 780

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sudoku")

GRID = grid.Grid(screen)
GRID.populate()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if x < 720 and y < 720:
                GRID.observer.highlight(
                    GRID.observer.get_square_coords(pygame.mouse.get_pos()))
            else:
                GRID.observer.solve_btn.handle_click()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            GRID.observer.draw()
    pygame.display.update()
