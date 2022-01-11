import pygame
import sys
import pdb

from button import Button
from eventlessbutton import EventlessButton
from label import Label
from specialtimer import Timer

pygame.font.init()
pygame.init()


def foo():
    print('pressed eventless')


FPS = 30
DISPLAYSIZE = (500, 500)
print(pygame.time.get_ticks())
screen = pygame.display.set_mode(DISPLAYSIZE)
print(pygame.time.get_ticks())
pygame.display.set_caption(__file__)
clock = pygame.time.Clock()

button = Button(screen, (10, 10), None, '', (20, 10, 5), 'c')
button.set_text('Button')
button2 = EventlessButton(screen, (200, 10), None, '', (50, 150, 250), 'c', target=foo)
button2.set_text('Button2')

# timer = [Timer(i*10) for i in range(1, 4)]
# for t in timer:
# 	t.start()

while True:
    clock.tick(FPS)
    pygame.display.set_caption(str(clock.get_fps()))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        if (event.type in
                (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION)):
            ch_cur = button.check_press(event)
            button2.check_press(event, ch_cur)

        if event.type == Button.BUTTONEVENT:
            print('pressed')
            print(event.button_name)

    screen.fill((0, 0, 0))
    button.draw()
    button2.draw()

    pygame.display.flip()
