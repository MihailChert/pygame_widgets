import pygame
import sys

from lib import EventlessButton


def foo(button):
    print('event')


pygame.font.init()
pygame.init()

DISPLAY_SIZE = (500, 500)
FPS = 30

display = pygame.display.set_mode(DISPLAY_SIZE)
clock = pygame.time.Clock()
button = EventlessButton(display, (10, 10), None, 'some', (200, 200, 200), 'c', target=foo, borders=3)

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            button.check_press(event)

    display.fill(0)
    button.draw()
    pygame.display.flip()
