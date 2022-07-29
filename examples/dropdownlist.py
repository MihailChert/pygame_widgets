import sys
import pygame
from lib import Label, MenuList, EventlessButton, Button, Event


pygame.font.init()
pygame.init()

DISPLAY_SIZE = (500, 500)
FPS = 30
clock = pygame.time.Clock()
display = pygame.display.set_mode(DISPLAY_SIZE)

label = Label(display, (100, 100), None, 'some', (100, 150, 30), 'c')
drop_list = MenuList(display, (10, 10))
button = EventlessButton(display, (0,0), None, 'some', (100, 150, 30), 'c')
drop_list.add(button)
button = EventlessButton(None, (0, 0), None, 'button', 200, 'r')
drop_list.add(button)

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == Event.TYPE:
            if event.event_type == MenuList.EVENT_TYPE:
                if event.selected_id == 0:
                    drop_list.remove(1)
                elif event.selected_id == 1:
                    drop_list.add(button)
                print('dropdown item', event.selected_id)
        if event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            drop_list.check_press(event)

    display.fill(0)
    drop_list.draw()
    pygame.display.flip()
