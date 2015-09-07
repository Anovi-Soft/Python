from header import *


class Scene:
    """abstract class implements the standard scene"""
    def __init__(self, next_scene=None):
        self.__next_scene = next_scene

    def loop(self, dt):
        self.__event(pygame.event)
        self._update(dt)
        self._draw(dt)

    def start(self, display, manager):
        self.display = display
        self.manager = manager
        self.img_dict = manager.img_dict
        self._start()
        self.__end = False

    def _start(self):
        pass

    def __event(self, event):
        if len(event.get(pygame.QUIT)) > 0:
            self.__end = True
            self.set_next_scene(None)
            return

        events = {}
        for e in event.get():
            try:
                if False:
                    print(e)
            except UnicodeEncodeError:
                print('Russian text input')
            type = e.type
            key = None
            try:
                key = e.key
            except:
                pass
            events[type] = key

        self._event(events)

        if END_SCENE in events:
            self.__end = True

    def _draw(self, dt):
        pass

    def _event(self, event):
        pass

    def _update(self, dt):
        pass

    def next(self):
        return self.__next_scene

    def is_end(self):
        return self.__end

    def the_end(self):
        if not self.is_end():
            pygame.event.post(pygame.event.Event(END_SCENE))

    def set_next_scene(self, scene):
        self.__next_scene = scene


class Menu:
    """This class realized menu element"""
    def __init__(self, position=(0, 0), loop=True):
        self.index = 0
        self.x = position[0]
        self.y = position[1]
        self.menu = list()

    def down(self):
        self.index += 1
        if self.index >= len(self.menu):
            self.index = 0

    def up(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.menu)-1

    def event(self, event):
        mouse = pygame.mouse.get_pos()
        mouseUp = False
        if pygame.MOUSEBUTTONUP in event:
            mouseUp = True
        index = 0
        x = self.x
        y = self.y
        for item in self.menu:
            if self.index == index:
                if mouse_in(mouse, (x, y), (x+item['select'].get_rect().w,
                                            y+item['select'].get_rect().h)):
                    self.index = index
                    if mouseUp:
                        self.call()
                        break
                y += item['select'].get_rect().h
            else:
                if mouse_in(mouse, (x, y), (x+item['no select'].get_rect().w,
                                            y+item['no select'].get_rect().h)):
                    self.index = index
                y += item['no select'].get_rect().h
            index += 1

    def add_menu_item(self, no_select, select, func, args=None):
        self.menu.append({'no select': no_select,
                          'select': select,
                          'func': func,
                          'args': args})

    def call(self):
        if self.menu[self.index]['func'] is not None:
            if self.menu[self.index]['args'] is not None:
                self.menu[self.index]['func'](self.menu[self.index]['args'])
            else:
                self.menu[self.index]['func']()

    def draw(self, display):
        index = 0
        x = self.x
        y = self.y
        for item in self.menu:
            if self.index == index:
                display.blit(item['select'], (x, y))
                y += item['select'].get_rect().h
            else:
                display.blit(item['no select'], (x, y))
                y += item['no select'].get_rect().h
            index += 1


class RadioButtons:
    """This class realized radio buttons element"""
    def __init__(self, position=(0, 0), function=None, select=0, loop=True,
                 radio_s=None, radio_n=None):
        self.index = -1
        self.select_value = select
        self.select = -1
        self.function = function
        self.x = position[0]
        self.y = position[1]
        self.menu = list()
        self.click = False
        self.radio_s = radio_s
        self.radio_n = radio_n
        self.r_size = radio_s.get_rect().h

    def event(self, event):
        mouse = pygame.mouse.get_pos()

        mouseUp = False
        if pygame.MOUSEBUTTONUP in event:
            mouseUp = True

        index = 0
        x = self.x
        y = self.y
        assign = False
        for item in self.menu:
            type = 'select' if self.index == index else 'no select'
            if mouse_in(mouse,
                        (x, y),
                        (x+item[type].get_rect().w,
                         y+item[type].get_rect().h+self.r_size)):
                self.index = index
                assign = True
                if mouseUp:
                    self.select = index
                    self.call()
                    break
            else:
                if not assign:
                    self.index = -1

            x += item[type].get_rect().w
            index += 1

    def add_menu_item(self, no_select, select, value):
        self.menu.append({'no select': no_select,
                          'select': select,
                          'value': value})
        if value == self.select_value:
            self.select = len(self.menu)-1

    def call(self):
        self.function(self.menu[self.index]['value'])

    def draw(self, display):
        index = 0
        x = self.x
        y = self.y
        for item in self.menu:
            if self.select == index:
                display.blit(self.radio_s,
                             (x +
                              (item['select'].get_rect().w - self.r_size)//2,
                              y))
            else:
                display.blit(self.radio_n,
                             (x +
                              (item['no select'].get_rect().w -
                               self.r_size)//2, y))
            if self.index == index:
                display.blit(item['select'], (x, y+self.r_size+10))
                x += item['select'].get_rect().w+20
            else:
                display.blit(item['no select'], (x, y+self.r_size+10))
                x += item['no select'].get_rect().w+20
            index += 1


class Label:
    """This class realized label element"""
    def __init__(self, text, font_size, pos):
        self.text = text.split("\n")
        self.font = pygame.font.SysFont("Monospace",
                                        font_size,
                                        bold=False,
                                        italic=False)
        self.pos = pos
        self.step = self.font.render("0", True, WHITE).get_rect().h

    def event(self, event):
        pass

    def draw(self, display):
        index = 0
        for part in self.text:
            display.blit(self.font.render(part, True, WHITE),
                         (self.pos[0], self.pos[1]+index*self.step))
            index += 1

    def size(self):
        return self.step


class Button:
    """This class realized button element"""
    def __init__(self, text, font_size, pos, function):
        self.image = \
            {"select": pygame.font.SysFont("Monospace",
                                           font_size,
                                           bold=True,
                                           italic=False).render(text,
                                                                True,
                                                                WHITE),
             "no select": pygame.font.SysFont("Monospace",
                                              font_size,
                                              bold=False,
                                              italic=False).render(text,
                                                                   True,
                                                                   WHITE)}
        self.pos = pos
        self.select = False
        self.func = function

    def call(self, arg):
        if arg is None:
            self.func()
        else:
            self.func(arg)

    def event(self, event, arg=None):
        mouse = pygame.mouse.get_pos()
        mouseUp = False
        type = "select" if self.select else "no select"
        if mouse_in(mouse, self.pos,
                    (self.pos[0] + self.image[type].get_rect().w,
                     self.pos[1] + self.image[type].get_rect().h)):
            self.select = True
            if pygame.MOUSEBUTTONUP in event:
                self.call(arg)

    def draw(self, display):
        type = "select" if self.select else "no select"
        display.blit(self.image[type], self.pos)

    def size(self):
        return len(self.text)*self.step


class TextInput:
    """This class realized label element"""
    def __init__(self, font_size, pos, back, text_size=10, check=None,
                 message_ok="", message_wrong="", button=None, text=""):
        self.text = text
        self.text_size = text_size
        self.font = pygame.font.SysFont("Monospace",
                                        font_size,
                                        bold=False,
                                        italic=False)
        self.pos = pos
        rect = self.font.render("0", True, WHITE).get_rect()
        self.symbol_width = rect.w
        self.symbol_height = rect.h
        self.width = rect.w*(text_size+2)
        self.height = int(rect.w*2)
        self.back = pygame.transform.scale(back, (self.width, self.height))
        self.check = check
        self.message_ok = message_ok
        self.message_wrong = message_wrong
        self.all_right = False if check is not None else True
        self.button = button

    def is_ok(self):
        return self.all_right

    def event(self, event):
        if pygame.KEYDOWN in event:
            if len(self.text) < self.text_size:
                if event[pygame.KEYDOWN] in range(48, 58):
                    self.text += chr(event[pygame.KEYDOWN])
                if event[pygame.KEYDOWN] in range(256, 266):
                    self.text += chr(event[pygame.KEYDOWN]-208)
                if event[pygame.KEYDOWN] in range(97, 123):
                        self.text += chr(event[pygame.KEYDOWN])
                if event[pygame.KEYDOWN] == pygame.K_PERIOD:
                    self.text += '.'
                if event[pygame.KEYDOWN] == 266:
                    self.text += '.'
            if event[pygame.KEYDOWN] == pygame.K_BACKSPACE:
                if self.text != "":
                    self.text = self.text[:-1]

        self.__check()
        if self.button is not None and self.is_ok():
            self.button.event(event, self.text)

    def __check(self):
        if self.check is not None:
            self.all_right = self.check(self.text)

    def draw(self, display):
        display.blit(self.back, (self.pos[0], self.pos[1]))
        display.blit(self.font.render(self.text, True, WHITE),
                     (self.pos[0]+self.symbol_width,
                      self.pos[1]+self.symbol_height//8))
        if self.check is not None:
            display.blit(self.font.render(self.message_ok if self.all_right
                                          else self.message_wrong,
                                          True, WHITE),
                         (self.pos[0] + self.width + self.symbol_width,
                          self.pos[1]))
        if self.button is not None and self.is_ok():
            self.button.draw(display)

    def size(self):
        return self.step


class MenuScene(Scene):
    """class scene with menu"""
    def __init__(self, next_scene=None):
        Scene.__init__(self, next_scene)

    def create_menu(self, cord=(5, 5), elements=[], width=300, font_size = 60):
        menu = Menu(cord)
        i = font_size
        for element in elements:
            while pygame.font.SysFont("Monospace", i, bold=True, italic=False)\
                    .render(element[0], True, WHITE).get_rect().w\
                    > width-20 and i > 10:
                i -= 2
        font = pygame.font.SysFont("Monospace", int(i/1.2),
                                   bold=False, italic=False)
        font_bold = pygame.font.SysFont("Monospace", i,
                                        bold=True, italic=False)

        for element in elements:
            menu.add_menu_item(font.render(element[0],
                                           True,
                                           WHITE),
                               font_bold.render(element[0],
                                                True,
                                                WHITE),
                               element[1],
                               None if len(element) != 3 else element[2])

        return menu

    def event(self, event):
        if not self.is_end() and self.menu is not None:
            self.menu.event(event)
            if pygame.KEYDOWN in event:
                if event[pygame.KEYDOWN] == pygame.K_DOWN:
                        self.menu.down()
                elif event[pygame.KEYDOWN] == pygame.K_UP:
                        self.menu.up()
                elif event[pygame.KEYDOWN] == pygame.K_RETURN:
                        self.menu.call()

    def _draw(self, dt):
        if self.menu is not None:
            self.menu.draw(self.display)
