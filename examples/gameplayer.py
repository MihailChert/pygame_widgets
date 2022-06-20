import pygame
import sys
from lib.abstractgame import AbstractGame
from ffpyplayer.player import MediaPlayer
from ffpyplayer.pic import SWScale


class GamePlayer(AbstractGame):

    def __init__(self, video_path, size, fps=0, is_font=False, is_music=False, is_resizable=False,
                 is_full_screen=False, flags=0):
        super().__init__(size, fps, is_font, is_music, is_resizable, is_full_screen, flags)
        self.path = video_path
        ff_opt = {'sync': 'video', 'paused': True}
        self.player = MediaPlayer(self.path, ff_opts=ff_opt)
        while self.player.get_metadata()['src_vid_size'] == (0, 0):
            pygame.time.wait(100)
        self._metadata = self.player.get_metadata()
        self.sws = SWScale(self._metadata['src_vid_size'][0], self._metadata['src_vid_size'][1], 'rgb24',
                           self.window.get_size()[0], self.window.get_size()[1], 'rgb24')

    def before_quit(self):
        self.player.close_player()

    def window_event(self):
        return

    def mouse_event(self, events):
        return

    def key_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.before_quit()
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_SPACE:
                    self.player.toggle_pause()

    def custom_event(self, events):
        return

    def draw(self):
        self.clock.tick()
        frame, value = self.player.get_frame()
        if 'eof' == value:
            self.player.set_pause(True)
        elif frame is None:
            pygame.time.wait(100)
        else:
            pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.time.wait(int(value * 1000))
            img = self.sws.scale(frame[0])
            img = pygame.image.frombuffer(img.to_bytearray()[0], img.get_size(), 'RGB')
            self.window.blit(img, (0, 0))
            pygame.display.flip()


# if __name__ == '__main__':
player = GamePlayer('/home/mihail/Видео/freak kithen - freak of the week.mp4', (600, 500), is_font=True)
# pdb.set_trace()
player.run()
