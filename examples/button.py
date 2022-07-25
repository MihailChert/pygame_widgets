import pygame
import sys

from lib import EventlessButton

from lib import Button
from lib.event import Event


def foo(button):
    print('event')


pygame.font.init()
pygame.init()

DISPLAY_SIZE = (500, 500)
FPS = 30

display = pygame.display.set_mode(DISPLAY_SIZE)
clock = pygame.time.Clock()
button = Button(display, (10, 10), None, 'some', (200, 200, 200), 'c', target=foo, border=3)

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            button.check_press(event)
        if event.type == Event.TYPE and event.event_type == Button.EVENT_TYPE:
            print('Event custom button id=', event.button_id)

    display.fill(0)
    button.draw(1)
    pygame.display.flip()
