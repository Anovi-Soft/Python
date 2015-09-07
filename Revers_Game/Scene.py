from controls import *
from game import *
from random import randint
from online import *
from threading import Thread
from header import get_music
import subprocess
import sys


class SceneLogo (Scene):
    """scene with my logo"""
    def __init__(self, time=5000, *argv):
        Scene.__init__(self, *argv)
        self.run = 0
        self.time = time
        self.revers = 0

    def _start(self):
        self.manager.load_images()
        if self.manager.message != "end":
            tmp = None
            try:
                tmp = get_music("loading.ogg")
            except Exception:
                print("Music file for loading not find")
            self.thread = Thread(target=self.manager.load_music)
            self.thread.setDaemon(True)
            self.thread.start()
            if tmp is not None:
                self.music_stream = tmp.play(loops=1)
                self.music_stream.set_volume(0.3)
        else:
            self.music_stream = None
        self.back = self.img_dict[Img.load_background]
        self.pos = (0, 0)

    def _event(self, event):
        if (pygame.KEYDOWN in event or pygame.MOUSEBUTTONUP in event or
            self.run > self.time)\
                and self.manager.message == "end" and not self.is_end():
                if self.music_stream is not None:
                    self.music_stream.stop()
                self.the_end()
                self.music_thread = Thread(target=play_music)
                self.music_thread.setDaemon(True)
                self.music_thread.start()

    def _update(self, dt):
        self.run += dt
        if self.run//200 > self.revers:
            self.back, self.pos = self.rot_center(
                image=self.img_dict[Img.load_background],
                angle=-11*self.revers)
            self.revers += 1

    def _draw(self, dt):
        pos0 = self.pos[0]-self.manager.options[Opt.width]/4
        pos1 = self.pos[1]-self.manager.options[Opt.height]
        pos = pos0, pos1
        self.display.blit(self.back, pos)
        tmp0 = self.img_dict[Img.logo].get_rect().w//2
        tmp1 = self.display.get_rect().w//2 - tmp0
        tmp2 = self.display.get_rect().h//2 - tmp0
        self.display.blit(self.img_dict[Img.logo],
                          (tmp1, tmp2))
        tmp0 = self.img_dict[Img.loading_end].get_rect().w/2
        tmp1 = self.display.get_rect().w/2 - tmp0
        tmp2 = self.img_dict[Img.loading_end].get_rect().h/2
        tmp3 = self.display.get_rect().h/2 + tmp2
        if self.manager.message == "end" and self.music_stream is not None:
            self.display.blit(self.img_dict[Img.loading_end],
                              (tmp1, tmp3))

    def rot_center(self, image, pos=(0, 0), angle = 0):
        rot_im = pygame.transform.rotate(image, angle)

        ow, oh = image.get_size()
        rw, rh = rot_im.get_size()
        scale_x, scale_y = float(rw) / ow, float(rh) / oh
        dx = round((ow / 2.0) * scale_x - (ow / 2.0))
        dy = round((oh / 2.0) * scale_y - (oh / 2.0))
        new_pos = pos[0] - dx, pos[1] - dy

        return rot_im, new_pos


class MainScene (MenuScene):
    """Main scene"""
    def __init__(self, *argv):
        MenuScene.__init__(self, *argv)
        self.controls = []
        self.elem = ME.main
        self.menu = None
        self.server = None
        self.thread = None
        self.game_type = {GM.opponent: Player.pc, GM.type: Revers, GM.size: 10}
        self.menu_items = {ME.main: (("Online Game", self.button_online),
                                     ("New Game", self.button_game),
                                     ("Load Game", self.button_load),
                                     ("Options", self.button_options),
                                     ("About", self.button_about),
                                     ("Records", self.button_record),
                                     ("Exit", self.button_exit)),
                           ME.options: (("Back", self.button_back),
                                        ("Style", self.button_style),
                                        ("Window", self.button_window)),
                           ME.online: (("Back", self.button_back),
                                       ("Client", self.button_client),
                                       ("Host", self.button_host)),
                           ME.message: (("OK", self.button_back),)}

    def _start(self, controls=[]):
        self.controls = controls
        width = self.img_dict[Img.left_substrate].get_rect().w
        self.menu = self.create_menu(cord=(10, 10),
                                     elements=self.menu_items[self.elem],
                                     width=width)

    def _draw(self, dt):
        self.display.blit(self.img_dict[Img.background], (0, 0))
        self.display.blit(self.img_dict[Img.left_substrate], (0, 0))
        if self.controls:
            self.display.blit(self.img_dict[Img.right_substrate],
                              (self.img_dict[Img.left_substrate].get_rect().w,
                               0))
            for control in self.controls:
                control.draw(self.display)
        self.menu.draw(self.display)

    def _event(self, event):
        self.event(event)
        for control in self.controls:
            control.event(event)

    def button_back(self):
        self.manager.music_dict[MUS.step].play()
        self.elem = ME.main
        self._start([])
        self.manager.load_options()
        self.game_type = {GM.opponent: Player.pc, GM.type: Revers, GM.size: 10}
        self.thread = None
        if self.server is not None:
            self.server.close()
            self.server = None

    def button_exit(self):
        self.manager.music_dict[MUS.step].play()
        self.set_next_scene(SceneLogo(2000))
        self.the_end()

    def button_online(self):
        self.manager.music_dict[MUS.step].play()
        self.elem = ME.online
        self._start([])

    def button_options(self):
        self.manager.music_dict[MUS.step].play()
        self.elem = ME.options
        self._start([])

    def button_style(self):
        self.manager.music_dict[MUS.step].play()
        self.manager.load_options()
        style_one = Label('Select type of style:',
                          self.manager.options[Opt.height]//15,
                          (self.manager.options[Opt.width]//4.5,
                           int(self.manager.options[Opt.height]*0.05)))

        style_two = RadioButtons((self.manager.options[Opt.width]//4.5,
                                  int(self.manager.options[Opt.height] *
                                      0.05+style_one.size())),
                                 self.select_point,
                                 (self.manager.options[Opt.point_b],
                                  self.manager.options[Opt.point_w],
                                  self.manager.options[Opt.point],
                                  self.manager.options[Opt.black_hall]),
                                 True,
                                 self.img_dict[Img.radio_select],
                                 self.img_dict[Img.radio_no_select])
        style_two.add_menu_item(self.img_dict[Img.deselect_stock_point],
                                self.img_dict[Img.select_stock_point],
                                ("point_black.png", "point_white.png",
                                 "point.png", "black_hall.png"))
        style_two.add_menu_item(self.img_dict[Img.deselect_politics_point],
                                self.img_dict[Img.select_politics_point],
                                ("usa.png", "russian.png",
                                 "ukraine.png", "german.png"))

        self._start([style_one, style_two])

    def button_window(self):
        self.manager.music_dict[MUS.step].play()
        self.manager.load_options()
        x = self.manager.options[Opt.width]//4.5
        y = int(self.manager.options[Opt.height]*0.05)
        label1 = Label('Select resolution:',
                       self.manager.options[Opt.height]//15,
                       (x, y))
        y += label1.size()

        rb1 = RadioButtons((x, y),
                           self.select_resolution,
                           (self.manager.options[Opt.width],
                            self.manager.options[Opt.height]),
                           True,
                           self.img_dict[Img.radio_select],
                           self.img_dict[Img.radio_no_select])
        font = pygame.font.SysFont("Monospace",
                                   self.manager.options[Opt.height]//20,
                                   bold=False, italic=False)
        b_font = pygame.font.SysFont("Monospace",
                                     self.manager.options[Opt.height]//20,
                                     bold=True, italic=False)
        rb1.add_menu_item(font.render("640x360", True, (255, 255, 255)),
                          b_font.render("640x360", True, (255, 255, 255)),
                          (640, 360))
        rb1.add_menu_item(font.render("1280x720", True, (255, 255, 255)),
                          b_font.render("1280x720", True, (255, 255, 255)),
                          (1280, 720))
        rb1.add_menu_item(font.render("1600x900", True, (255, 255, 255)),
                          b_font.render("1600x900", True, (255, 255, 255)),
                          (1600, 900))
        rb1.add_menu_item(font.render("1920x1080", True, (255, 255, 255)),
                          b_font.render("1920x1080", True, (255, 255, 255)),
                          (1920, 1080))

        y += self.img_dict[Img.radio_select].get_rect().h
        y += b_font.render("0", True, (255, 255, 255)).get_rect().h+30

        label2 = Label('Select windowed or fullscreen',
                       self.manager.options[Opt.height]//15,
                       (x, y))

        y += label2.size()

        rb2 = RadioButtons((x, y),
                           self.select_full_screen,
                           self.manager.options[Opt.full_screen],
                           True,
                           self.img_dict[Img.radio_select],
                           self.img_dict[Img.radio_no_select])
        rb2.add_menu_item(font.render("Windowed", True, (255, 255, 255)),
                          b_font.render("Windowed",
                                        True, (255, 255, 255)),
                          False)
        rb2.add_menu_item(font.render("FullScreen", True, (255, 255, 255)),
                          b_font.render("FullScreen",
                                        True, (255, 255, 255)),
                          True)

        y += self.img_dict[Img.radio_select].get_rect().h
        y += b_font.render("0", True, (255, 255, 255)).get_rect().h+30

        label3 = Label('Reboot for the take effect',
                       self.manager.options[Opt.height]//15,
                       (x, y))
        y += label3.size()

        b1 = Button("Restart", self.manager.options[Opt.height]//15,
                    (x, y), self.button_restart)

        self._start([label1, label2, label3, rb1, rb2, b1])

    def button_game(self):
        self.manager.music_dict[MUS.step].play()
        x = self.manager.options[Opt.width]//4.5
        y = int(self.manager.options[Opt.height]*0.05)
        label1 = Label('Select opponent:',
                       self.manager.options[Opt.height]//15,
                       (x, y))

        y += label1.size()

        font = pygame.font.SysFont("Monospace",
                                   self.manager.options[Opt.height]//20,
                                   bold=False, italic=False)
        b_font = pygame.font.SysFont("Monospace",
                                     self.manager.options[Opt.height]//20,
                                     bold=True, italic=False)
        rb1 = RadioButtons((x, y),
                           self.select_opponent,
                           self.game_type[GM.opponent],
                           True,
                           self.img_dict[Img.radio_select],
                           self.img_dict[Img.radio_no_select])

        rb1.add_menu_item(font.render("Player vs PC.", True,
                                      (255, 255, 255)),
                          b_font.render("Player vs PC.", True,
                                        (255, 255, 255)),
                          Player.pc)
        rb1.add_menu_item(font.render("Player vs Player.", True,
                                      (255, 255, 255)),
                          b_font.render("Player vs Player.", True,
                                        (255, 255, 255)),
                          Player.man)

        y += self.img_dict[Img.radio_select].get_rect().h
        y += b_font.render("0", True, (255, 255, 255)).get_rect().h+30

        label2 = Label('Select game type:',
                       int(self.manager.options[Opt.height]/15),
                       (x, y))
        y += label2.size()

        rb2 = RadioButtons((x, y),
                           self.select_type,
                           self.game_type[GM.type],
                           True,
                           self.img_dict[Img.radio_select],
                           self.img_dict[Img.radio_no_select])
        rb2.add_menu_item(font.render("Original revers.", True,
                                      (255, 255, 255)),
                          b_font.render("Original revers.", True,
                                        (255, 255, 255)),
                          Revers)
        rb2.add_menu_item(font.render("Revers with blackhall.", True,
                                      (255, 255, 255)),
                          b_font.render("Revers with blackhall.", True,
                                        (255, 255, 255)),
                          ReversWithBlackHall)

        y += self.img_dict[Img.radio_select].get_rect().h
        y += b_font.render("0", True, (255, 255, 255)).get_rect().h+30

        label3 = Label('Select size:',
                       int(self.manager.options[Opt.height]/15),
                       (x, y))
        y += label3.size()

        b1 = Button("Start", int(self.manager.options[Opt.height]/15),
                    (x, y+label3.size()), self.button_create_game)

        ti = TextInput(int(self.manager.options[Opt.height]/15),
                       (x, y),
                       self. manager.img_dict[Img.right_substrate],
                       2,
                       is_in_4_to_20,
                       "size ok",
                       "4 <= size <= 20",
                       b1,
                       "10")

        self._start([label1, label2, label3, rb1, rb2, ti])

    def button_load(self):
        self.manager.music_dict[MUS.step].play()
        try:
            dump = self.manager.load_game()
            if dump is None:
                return

            self.game_type[GM.opponent] = Player.pc\
                if dump[GM.opponent] == "pc" else Player.man
            self.game_type[GM.rnd] = dump[GM.rnd]
            self.game_type[GM.size] = dump[GM.size]
            self.game_type[GM.type] == Revers \
                if dump[GM.type] == "Revers" else ReversWithBlackHall
            game = self.game_type[GM.type](self.game_type[GM.size],
                                           self.manager,
                                           Player.man,
                                           self.game_type[GM.opponent],
                                           self.game_type[GM.rnd])
            game.start()
            game.field = dump[GM.field]
            game.person = dump[GM.person]
            game.valid_path = game.get_valid_path()
            game.points = {-1: 0, 1: 0}
            for row in game.field:
                    for column in row:
                        if column == 1 or column == -1:
                            game.points[column] += 1
            game.interface.set_information(game.points,
                                           game.person,
                                           game.players)

            self.set_next_scene(GameScene(game, self.game_type))
            self.the_end()
        except:
            self.create_message("Loading error")

    def button_record(self):
        if self.manager.records is None:
            self.create_message("Error in open file of records")
            return
        self.manager.music_dict[MUS.step].play()
        x = int(self.manager.options[Opt.width]/4.5)
        y = int(self.manager.options[Opt.height]*0.05)
        label1 = Label('TABLE OF RECORDS',
                       int(self.manager.options[Opt.height]/15),
                       (x, y))
        y += label1.size()
        records_lst = []
        for i in range(4, 21):
            value = self.manager.records[i][0]
            records_lst.append(("size " + str(i) + ": " + value[0] + " - " +
                                ("" if value[1] == 0 else str(value[1])),
                                self.open_record,
                                i))
        list = self.create_menu(cord=(x, y),
                                elements=records_lst,
                                width=2000,
                                font_size=self.manager.options[Opt.height]//22)
        self._start([label1, list])

    def open_record(self, i):
        self.manager.music_dict[MUS.step].play()
        x = int(self.manager.options[Opt.width]/4.5)
        y = int(self.manager.options[Opt.height]*0.05)
        label1 = Label('RECORDS IN SIZE:' + str(i),
                       int(self.manager.options[Opt.height]/15),
                       (x, y))
        y += label1.size()
        records_lst = []
        j = 0
        for i in self.manager.records[i]:
            records_lst.append((str(j) + ": " +
                                i[0] + " - " +
                                ("" if i[1] == 0 else str(i[1])),
                                None))
            j += 1
        list = self.create_menu(cord=(x, y),
                                elements=records_lst,
                                width=2000,
                                font_size=self.manager.options[Opt.height]//22)
        self._start([label1, list])

    def button_about(self):
        self.manager.music_dict[MUS.step].play()
        x = int(self.manager.options[Opt.width]/4.5)
        y = int(self.manager.options[Opt.height]*0.05)
        label1 = Label('''Revers Game

This app has written by Andrey Novikov

You can choose one of two rules for the game
First: The original rules
Second: The original rules with a black hole

You can play:
With the computer
With your friend on the network
Wiht your friend on this computer

You can choose the size of the playing field
Enjoy the game''',
                       int(self.manager.options[Opt.height]/22),
                       (x, y))

        self._start([label1])

    def button_client(self):
        self.manager.music_dict[MUS.step].play()
        x = int(self.manager.options[Opt.width]/4.5)
        y = int(self.manager.options[Opt.height]*0.05)
        label1 = Label('Please input id:',
                       int(self.manager.options[Opt.height]/15),
                       (x, y))
        y += label1.size()

        b1 = Button("Connect", int(self.manager.options[Opt.height]/15),
                    (x, y+label1.size()), self.button_connect)

        text_input = TextInput(int(self.manager.options[Opt.height]/15),
                               (x, y),
                               self.img_dict[Img.right_substrate],
                               15,
                               is_it_ip,
                               "it is ip",
                               "it is not ip",
                               b1,
                               "127.0.0.1")

        self._start([label1, text_input])

    def button_host(self):
        self.manager.music_dict[MUS.step].play()
        x = int(self.manager.options[Opt.width]/4.5)
        y = int(self.manager.options[Opt.height]*0.05)
        font = pygame.font.SysFont("Monospace",
                                   int(self.manager.options[Opt.height]/20),
                                   bold=False, italic=False)
        b_font = pygame.font.SysFont("Monospace",
                                     int(self.manager.options[Opt.height]/20),
                                     bold=True, italic=False)

        label2 = Label('Select game type:',
                       int(self.manager.options[Opt.height]/15),
                       (x, y))
        y += label2.size()

        rb2 = RadioButtons((x, y),
                           self.select_type,
                           self.game_type[GM.type],
                           True,
                           self.img_dict[Img.radio_select],
                           self.img_dict[Img.radio_no_select])
        rb2.add_menu_item(font.render("Original revers.",
                                      True, (255, 255, 255)),
                          b_font.render("Original revers.",
                                        True, (255, 255, 255)),
                          Revers)
        rb2.add_menu_item(font.render("Revers with blackhall.",
                                      True, (255, 255, 255)),
                          b_font.render("Revers with blackhall.",
                                        True, (255, 255, 255)),
                          ReversWithBlackHall)

        y += self.img_dict[Img.radio_select].get_rect().h
        y += b_font.render("0", True, (255, 255, 255)).get_rect().h+30

        label3 = Label('Select size:',
                       int(self.manager.options[Opt.height]/15),
                       (x, y))
        y += label3.size()

        b1 = Button("Host", int(self.manager.options[Opt.height]/15),
                    (x, y+label3.size()), self.button_create_host)

        ti = TextInput(int(self.manager.options[Opt.height]/15),
                       (x, y),
                       self. manager.img_dict[Img.right_substrate],
                       2,
                       is_in_4_to_20,
                       "size ok",
                       "4 <= size <= 20",
                       b1,
                       "10")

        self._start([label2, label3, rb2, ti])

    def button_create_game(self, size):
        self.manager.music_dict[MUS.step].play()
        self.game_type[GM.size] = int(size)
        self.game_type[GM.rnd] = randint(0, 1)
        game = self.game_type[GM.type](self.game_type[GM.size],
                                       self.manager,
                                       Player.man,
                                       self.game_type[GM.opponent],
                                       self.game_type[GM.rnd])
        game.start()
        self.set_next_scene(GameScene(game, self.game_type))
        self.the_end()

    def button_create_host(self, size):
        self.manager.music_dict[MUS.step].play()
        x = int(self.manager.options[Opt.width]/4.5)
        y = int(self.manager.options[Opt.height]*0.05)
        label1 = Label('Waiting client:',
                       int(self.manager.options[Opt.height]/15),
                       (x, y))
        self.game_type[GM.size] = int(size)
        self.thread = Thread(target=self.hosting)
        self.thread.setDaemon(True)
        self.thread.start()

        self._start([label1])

    def select_point(self, style):
        self.manager.music_dict[MUS.step].play()
        self.manager.options[Opt.point_b] = style[0]
        self.manager.options[Opt.point_w] = style[1]
        self.manager.options[Opt.point] = style[2]
        self.manager.options[Opt.black_hall] = style[3]

        self.manager.dump_options()

    def select_resolution(self, res):
        self.manager.music_dict[MUS.step].play()
        self.manager.options[Opt.width] = res[0]
        self.manager.options[Opt.height] = res[1]

    def select_full_screen(self, res):
        self.manager.music_dict[MUS.step].play()
        self.manager.options[Opt.full_screen] = res

    def select_opponent(self, res):
        self.manager.music_dict[MUS.step].play()
        self.game_type[GM.opponent] = res

    def select_type(self, res):
        self.manager.music_dict[MUS.step].play()
        self.game_type[GM.type] = res

    def button_restart(self):
        self.manager.music_dict[MUS.step].play()
        self.manager.dump_options()
        thread = Thread(target=self.sub_function_n1)
        thread.setDaemon(True)
        thread.start()
        sys.exit(0)

    def sub_function_n1(self):
        subprocess.call("Python main.py")

    def hosting(self):
        if self.server is not None:
            self.server.close()
        self.server = Host(maxContacts=1, auto_message_get=False)
        self.server.start()
        try:
            self.game_type[GM.opponent] = Player.online
            self.game_type[GM.rnd] = randint(0, 1)
            game = self.game_type[GM.type](self.game_type[GM.size],
                                           self.manager,
                                           Player.man,
                                           self.game_type[GM.opponent],
                                           self.game_type[GM.rnd],
                                           self.server)
            game.start()
            dump = {GM.rnd: self.game_type[GM.rnd],
                    GM.size: self.game_type[GM.size],
                    GM.type: "Revers"
                    if self.game_type[GM.type] == Revers else "ReversBH",
                    GM.field: game.field}
            self.server.send_pickle(0, dump)
            self.set_next_scene(GameScene(game, self.game_type))
            self.the_end()
        except Exception:
            self.server.close()

    def button_connect(self, ip):
        self.manager.music_dict[MUS.step].play()
        try:
            client = Client()
            client.start(ip)
            if client.get_pickle()[0] != MSG.id:
                self.create_message("Server is busy")
            dump = client.get_pickle()
            self.game_type[GM.opponent] = Player.online
            self.game_type[GM.rnd] = 1-dump[GM.rnd]
            self.game_type[GM.size] = dump[GM.size]
            self.game_type[GM.type] == Revers\
                if dump[GM.type] == "Revers" else ReversWithBlackHall
            game = self.game_type[GM.type](self.game_type[GM.size],
                                           self.manager,
                                           Player.man,
                                           self.game_type[GM.opponent],
                                           self.game_type[GM.rnd],
                                           client)
            game.start()
            game.field = dump[GM.field]
            game.valid_path = game.get_valid_path()
            game.points = {-1: 0, 1: 0}
            for row in game.field:
                    for column in row:
                        if column == 1 or column == -1:
                            game.points[column] += 1
            self.set_next_scene(GameScene(game, self.game_type))
            self.the_end()

        except:
            self.create_message("Host not find")

    def create_message(self, msg):
        x = int(self.manager.options[Opt.width]/4.5)
        y = int(self.manager.options[Opt.height]*0.05)
        self.elem = ME.message
        m1 = Label(msg, int(self.manager.options[Opt.height]/15), (x, y))
        self._start([m1])


class GameScene(MenuScene):
    def __init__(self, game, game_type, *argv):
        MenuScene.__init__(self, *argv)
        self.message = None
        self.input = None
        self.game = game
        self.game_type = game_type

    def _start(self):
        tmp = self.img_dict[Img.left_substrate].get_rect().w
        self.menu = self.create_menu(cord=(10, 10),
                                     elements=(("Quit",
                                                self.button_back),
                                               ("Save&Quit",
                                                self.button_save)),
                                     width=tmp)

    def _update(self, dt):
        if self.message is None:
            self.game.update(dt)

    def _event(self, event):
        if self.input is not None:
            self.input.event(event)
        else:
            if self.game.message is not None:
                self.create_message(self.game.message)
            else:
                self.game.event(event)
        self.event(event)

    def _draw(self, dt):
        self.display.blit(self.img_dict[Img.background], (0, 0))
        self.display.blit(self.img_dict[Img.left_substrate], (0, 0))
        self.menu.draw(self.display)
        self.display.blit(self.img_dict[Img.right_substrate],
                          (self.img_dict[Img.left_substrate].get_rect().w, 0))
        if self.message is None:
            self.game.draw(self.display)
        else:
            self.message.draw(self.display)
            if self.input is not None:
                self.input.draw(self.display)

    def button_save(self):
        dump = {GM.opponent: "pc"
                if self.game_type[GM.opponent] == Player.pc else "man",
                GM.rnd: self.game_type[GM.rnd],
                GM.size: self.game_type[GM.size],
                GM.type: "Revers"
                if self.game_type[GM.type] == Revers else "ReversBH",
                GM.person: self.game.person,
                GM.field: self.game.field}
        self.manager.dump_game(dump)

    def button_back(self, name=""):
        self.manager.music_dict[MUS.step].play()
        if name != "":
            ivalue = 0
            old = None
            winner = 1 if self.game.points[1] > self.game.points[-1] else -1
            for value in self.manager.records[self.game.size]:
                if old is None:
                    if self.game.points[winner] > value[1]:
                        old = value
                        self.manager.records[self.game.size][ivalue] =\
                            (name, self.game.points[winner])
                else:
                    new_old = value
                    self.manager.records[self.game.size][ivalue] = old
                    old = new_old
                ivalue += 1

            self.manager.dump_records()

        if self.game.online is not None:
            self.game.online.send_pickle(0, (-1, -2))
            if self.game.online == Host:
                self.game.online.close()

        self.set_next_scene(MainScene())
        self.the_end()

    def create_message(self, msg):
        x = int(self.manager.options[Opt.width]/4.5)
        y = int(self.manager.options[Opt.height]*0.05)

        winner = 1 if self.game.points[1] > self.game.points[-1] else -1

        if self.game.players[winner] == Player.man:
            for value in self.manager.records[self.game.size]:
                if self.game.points[winner] > value[1]:
                    self.message = Label("Your new record is " +
                                         str(self.game.points[winner]) +
                                         ".\nEnter your name:",
                                         self.manager.options[Opt.height]//15,
                                         (x, y))
                    b1 = Button("To record",
                                int(self.manager.options[Opt.height]/15),
                                (x, y+self.message.size()*3),
                                self.button_back)
                    tmp = TextInput(self.manager.options[Opt.height]//15,
                                    (x, y+self.message.size()*2),
                                    self.manager.img_dict[Img.right_substrate],
                                    10,
                                    None,
                                    "",
                                    "",
                                    b1,
                                    "Man")
                    self.input = tmp
                    break
        else:
            self.message = Label(msg,
                                 int(self.manager.options[Opt.height]/15),
                                 (x, y))
        tmp = self.img_dict[Img.left_substrate].get_rect().w
        self.menu = self.create_menu(cord=(10, 10),
                                     elements=([("OK", self.button_back)]),
                                     width=tmp)
