import pygame
import sys
import grid

pygame.init()

size = width, height = 720, 780

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sudoku")

GRID = grid.Grid(screen)
GRID.observer.draw()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            GRID.observer.handle_event(event)
    pygame.display.update()
