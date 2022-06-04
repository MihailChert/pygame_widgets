from ffpyplayer.player import MediaPlayer
from ffpyplayer.pic import SWScale
import pygame
import sys
# from lib.abstractgame import AbstractGame

video_path = '/home/mihail/Видео/freak kithen - freak of the week.mp4'

pygame.mixer.init()
pygame.init()
display = pygame.display.set_mode((600, 500))
clock = pygame.time.Clock()

ff_opt = {'sync': 'video'}
player = MediaPlayer(video_path, ff_opts=ff_opt)

while player.get_metadata()['src_vid_size'] == (0, 0):
    pygame.time.wait(100)

frame_size = player.get_metadata()['src_vid_size']
sws = SWScale(frame_size[0], frame_size[1], 'rgb24', 600, 500, 'rgb24')
print(player.get_metadata())
player.set_pause(True)

while True:
    clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            player.close_player()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.toggle_pause()
    frame, val = player.get_frame()
    if 'eof' == val:
        break
    elif frame is None:
        continue
    else:
        pygame.time.wait(int(val * 1000))
        pygame.display.set_caption(str(clock.get_fps()))
        img = frame[0]
        img = sws.scale(img)
        img = pygame.image.frombuffer(img.to_bytearray()[0], img.get_size(), 'RGB')
        display.blit(img, (0, 0))
        pygame.display.flip()

player.close_player()