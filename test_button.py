import pygame
import sys
import pdb

from button import Button
from lable import Lable
from specialtimer import Timer

pygame.font.init()
pygame.init()

FPS = 30
DISPLAYSIZE = (500, 500)
print(pygame.time.get_ticks())
screen = pygame.display.set_mode(DISPLAYSIZE)
print(pygame.time.get_ticks())
pygame.display.set_caption(__file__)
clock = pygame.time.Clock()

button = Button(screen, (10, 10), None, '', (20, 10, 5), 'c')
button.set_text('Button')
button2 = Button(screen, (200, 10), None, '', (50, 150, 250), 'c')
button2.set_text('Button2')

# timer = [Timer(i*10) for i in range(1, 4)]
# for t in timer:
# 	t.start()

while True:
	clock.tick(FPS)
	pygame.display.set_caption(str(clock.get_fps()))
	for event in pygame.event.get():
		if event.type == pygame.QUIT \
		or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN\
			or event.type == pygame.MOUSEBUTTONUP\
			or event.type == pygame.MOUSEMOTION:
			ch_cur = button.collide(event)
			button2.collide(event, ch_cur)

		if event.type == Button.BUTTONEVENT:
			print('pressed')
			print(event.button_name)

	screen.fill((0, 0, 0))
	button.draw()
	button2.draw()

	pygame.display.flip()
