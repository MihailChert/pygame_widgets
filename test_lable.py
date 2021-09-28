import pygame
import sys

from lable import Lable

pygame.font.init()
pygame.init()

FPS = 30
DISPLAYSIZE = (500, 500)
display = pygame.display.set_mode(DISPLAYSIZE)
pygame.display.set_caption(__file__)
clock = pygame.time.Clock()
lable = Lable(display, (100, 100), (None, 30, Lable.default_color),
	'', (100, 100, 100), 'r', rect_size=(100, 100))
lable.set_text('lksdn\nsmd')

while True:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT \
		or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			pygame.quit()
			sys.exit()

	display.fill((0, 0, 0))
	lable.draw()

	pygame.display.flip()
