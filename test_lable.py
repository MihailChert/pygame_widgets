import pygame
import sys
import pdb

from label import Label
from specialtimer import Timer
from modules import SizeRange, Margin

pygame.font.init()
pygame.init()

FPS = 30
DISPLAYSIZE = (500, 500)
display = pygame.display.set_mode(DISPLAYSIZE)
pygame.display.set_caption(__file__)
clock = pygame.time.Clock()
s_range = SizeRange(None, 60, None, None)
colors = (150,20,0)
labels = []
for i in range(10):
	label = Label(display, (50, 50), (None, 17, Label.default_color),
		'', (100, 100, 100), 'c', border_colors=colors, margin=Margin(5))
	label.set_text(label.name)
	labels.append(label)

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
			for i in labels:
				move = i.calculate_collide(labels)
			display.fill(0)
			for l in labels:
				l.draw()

	pygame.display.flip()
