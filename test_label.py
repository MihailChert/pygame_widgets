import pygame
import sys
from label import Label

pygame.font.init()
pygame.init()

DISPLAY_SIZE = (500, 500)
FPS = 30

display = pygame.display.set_mode(DISPLAY_SIZE)
clock = pygame.time.Clock()
label = Label(display, (10, 10), None, 'some', (100, 100, 100), 'c')
label.client_rect.width = 200
while True:
    display.fill(0)
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    label.draw()
    pygame.display.flip()
