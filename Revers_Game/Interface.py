from header import *
from controls import Label


class Interface:
    def __init__(self, size, img_dict, options):
        self.size = size
        self.img_dict = img_dict
        self.step = img_dict[Img.block_b].get_rect().h
        self.FIELD_START_WIDTH = int(options[Opt.width]/5 +
                                     (options[Opt.width]/5*4 -
                                      self.step*size)/2)
        self.FIELD_START_HEIGHT = int(options[Opt.height]/10)
        self.animation = []
        self.up_information = None
        self.down_information = None

    def set_information(self, points, person, players):
        up_information = "Black :" + str(points[-1]) + "; White : " +\
                         str(points[1]) + "."
        self.up_information = Label(up_information,
                                    int(self.FIELD_START_WIDTH/10),
                                    (self.FIELD_START_WIDTH,
                                     self.FIELD_START_HEIGHT/5))
        down_information = ""
        if players[-1] != Player.man or players[1] != Player.man:
            down_information = "You " + \
                               ("black. " if players[-1] == Player.man else
                                "white. ")
        down_information += "Turn " + \
                            ("black. " if person == -1 else
                             "white. ")
        self.down_information = Label(down_information,
                                      int(self.FIELD_START_WIDTH/10),
                                      (self.FIELD_START_WIDTH,
                                       self.FIELD_START_HEIGHT/5*45))

    def draw(self, display, field, path={}):
        iRow = iColumn = 0
        for row in field:
            for column in row:
                block_name = Img.block_w if (iColumn + iRow % 2) % 2 == 0 else\
                    Img.block_b
                display.blit(self.img_dict[block_name],
                             (self.FIELD_START_WIDTH+iColumn*self.step,
                              self.FIELD_START_HEIGHT+iRow*self.step))
                if column in (-1, 1, 2):
                    if column == 1:
                        block_name = Img.point_w
                    elif column == -1:
                        block_name = Img.point_b
                    elif column == 2:
                        block_name = Img.black_hall
                    display.blit(self.img_dict[block_name],
                                 (self.FIELD_START_WIDTH+iColumn*self.step,
                                  self.FIELD_START_HEIGHT+iRow*self.step))
                iColumn += 1
            iColumn = 0
            iRow += 1

        for (keyX, keyY) in path:
            display.blit(self.img_dict[Img.point],
                         (self.FIELD_START_WIDTH+keyY*self.step,
                          self.FIELD_START_HEIGHT+keyX*self.step))

        self.up_information.draw(display)
        self.down_information.draw(display)

    def event(self):
        mouse = pygame.mouse.get_pos()
        mouse = (mouse[0] - self.FIELD_START_WIDTH,
                 mouse[1] - self.FIELD_START_HEIGHT)
        if mouse_in(mouse, (0, 0), (self.step * self.size,
                                    self.step * self.size)):
            return mouse[1]//self.step, mouse[0]//self.step
        else:
            return -1, -1
