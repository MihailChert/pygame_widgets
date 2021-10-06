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
lable = Lable(display, (100, 100), (None, 30, Lable.default_color),
	'', (100, 100, 100), 'c')
lable.set_text('lksdn\nsmd')
lable.font.color[1] = 0
event = pygame.event.Event(Timer.TIMEREVENT)
timer = [Timer(i*10) for i in range(1, 4)]
for t in timer:
	t.start()

while True:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT \
		or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			pygame.quit()
			sys.exit()
		if event.type == Timer.TIMEREVENT:
			lable.font.color[event.timer_id] += 1
			# print(lable.font.color)
			if lable.font.color[event.timer_id] > 255:
				lable.font.color[event.timer_id] = 0



	display.fill((0, 0, 0))
	lable.draw()

	pygame.display.flip()
