import pygame
import sys

from lable import Lable
from specialtimer import Timer
from modules import SizeRange

pygame.font.init()
pygame.init()

FPS = 30
DISPLAYSIZE = (500, 500)
display = pygame.display.set_mode(DISPLAYSIZE)
pygame.display.set_caption(__file__)
clock = pygame.time.Clock()
s_range = SizeRange(None, 60, None, None)
colors = (150,20,0)
lable = Lable(display, (100, 100), (None, 30, Lable.default_color),
	'', (100, 100, 100), 'c', border_colors=colors, border=40)
lable.set_text('lksdn\nsmd')
lable.font.color[1] = 0
event = pygame.event.Event(Timer.TIMEREVENT)
timer = Timer(40*10)
timer.start()

while True:
	clock.tick()

	pygame.display.set_caption(str(clock.get_fps()))
	for event in pygame.event.get():
		if event.type == pygame.QUIT \
		or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			pygame.quit()
			sys.exit()
		if event.type == Timer.TIMEREVENT:
			display.fill(0)
			lable.draw()

	pygame.display.flip()
