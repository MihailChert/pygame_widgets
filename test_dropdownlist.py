import sys
import pygame
from label import Label
from dropdownlist import DropDownList
from eventlessbutton import EventlessButton

pygame.font.init()
pygame.init()

DISPLAY_SIZE = (500, 500)
FPS = 30
clock = pygame.time.Clock()
display = pygame.display.set_mode(DISPLAY_SIZE)

label = Label(display, (100, 100), None, 'some', (100, 150, 30), 'c')
drop_list = DropDownList(display, (10, 10), 40)
button = EventlessButton(display, (0,0), None, 'some', (100, 150, 30), 'c')
# drop_list.add_item(button)

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    display.fill(0)
    # drop_list.draw()
    button.draw()
    label.draw()
    pygame.display.flip()
