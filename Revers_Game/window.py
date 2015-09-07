from pygame.locals import *
from resmanager import ResManager
from header import *


class Window:
    """Class create pygame window"""
    def __init__(self,
                 color=(255, 255, 255),
                 fps=60,
                 scene=None,
                 manager=ResManager()):
        pygame.init()

        self.fps = fps
        self.__manager = manager
        self.scene = scene

        self.set_display(manager.options[Opt.width],
                         manager.options[Opt.height])

        self.__display.fill(color)
        pygame.display.flip()

    def set_display(self, width, height):
        if self.__manager.options[Opt.full_screen]:
            self.__display = pygame.display.set_mode((width, height),
                                                     DOUBLEBUF |
                                                     FULLSCREEN |
                                                     HWSURFACE)
        else:
            self.__display = pygame.display.set_mode((width, height),
                                                     DOUBLEBUF)

    def set_caption(self, title=None, icon=None):
        if title is None:
            pygame.display.set_caption("game")
        else:
            pygame.display.set_caption(title)

        if icon is not None:
            pygame.display.set_icon(self.__manager.get_image(icon))

    def loop(self):
        while self.scene is not None:
            clock = pygame.time.Clock()
            dt = 0

            self.scene.start(self.__display, self.__manager)

            while not self.scene.is_end():
                self.scene.loop(dt)

                pygame.display.flip()

                dt = clock.tick(self.fps)

            self.scene = self.scene.next()
