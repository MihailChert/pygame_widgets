import pygame
import sys

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

lable = Lable(screen, (100, 100), None, '', (200, 100, 5), 'r')
button = Button(screen, (10, 10), None, '', (20, 10, 5), 'c')
button.set_text('Button')
print(Button.ID)
print(Lable.ID)

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

		if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
			button.collide(event)
			print(event)

		if event.type == Button.BUTTONEVENT:
			print('pressed')
			print(event.button_name)

	screen.fill((0, 0, 0))
	button.draw()

	pygame.display.flip()
