from interface import Interface
from header import *

class Game:
    def __init__(self, size, manager=None, player_one=None,
                 player_two=None, rnd=1, online=None):
        self.size = size
        self.manager = manager
        if manager is not None:
            self.manager.load_images(size)
            self.interface = Interface(size,
                                   self.manager.img_dict,
                                   self.manager.options)
        self.person = 1
        self.online = online
        self.end = False
        self.message = None
        self.players = {1-2*rnd: player_one, -1+2*rnd: player_two}
        self.points = {-1: 2, 1: 2}
        self.active = False
        self.load = 0
        self.field = [[0] * size for i in range(size)]
        self.size = size
        if manager is not None:
            self.interface.set_information(self.points, self.person, self.players)

    def is_end(self):
        return self.end

    def the_end(self):
        self.end = True

    def descend(self, x, y):
        pass

    def get_valid_path(self):
        pass

    def start(self):
        pass

    def event(self, events):
        pass

    def update(self, dt):
        if not self.active:
            if self.load <= PASSIVE:
                self.load += dt
            else:
                self.active = True

    def draw(self, display):
        path = self.valid_path if (self.players[self.person] == Player.man) \
            else {}
        self.interface.draw(display, self.field, path)


class Revers(Game):
    def descend(self, x, y):
        if self.active and (x, y) in self.valid_path:
            if self.manager is not None:
                self.manager.music_dict[MUS.step].play()
            self.field[x][y] = self.person
            for value in self.valid_path[(x, y)]:
                self.field[value[0]][value[1]] = self.person
            self.person = 1 if self.person == -1 else -1
            self.valid_path = self.get_valid_path()
            self.active = False
            self.load = 0
            self.points = self.points = {-1: 0, 1: 0}
            for row in self.field:
                for column in row:
                    if column == 1 or column == -1:
                        self.points[column] += 1
            if self.manager is not None:
                self.interface.set_information(self.points,
                                               self.person,
                                               self.players)
            #print("{},".format((x, y)))

    def start(self):
        middle = int(self.size/2-1)
        self.field[middle][middle] = -1
        self.field[middle+1][middle] = 1
        self.field[middle][middle+1] = 1
        self.field[middle+1][middle+1] = -1
        self.valid_path = self.get_valid_path()

    def __revers_g_v_p_search(self, _x, _y, person):
        directions = [(-1, 1), (-1, 0), (-1, -1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]
        size = len(self.field)
        deletePath = []
        for direction in directions:
            tmpPath = []
            x = _x+direction[0]
            y = _y+direction[1]
            while (0 <= x < size) and (0 <= y < size) and \
                    (self.field[x][y] == -person):
                tmpPath.append((x, y))
                x += direction[0]
                y += direction[1]
            if (0 <= x < size) and (0 <= y < size) and \
                    (self.field[x][y] == person):
                deletePath += tmpPath
        return deletePath

    def get_valid_path(self):
        valid_path = {}
        for row in range(0, self.size):
            for column in range(0, self.size):
                if self.field[row][column] == 0:
                    part = self.__revers_g_v_p_search(row, column, self.person)
                    if len(part) != 0:
                        valid_path[(row, column)] = part
        return valid_path

    def event(self, events):
        pair = self.players[self.person](self, events)
        try:
            if pair[0] != -1:
                self.descend(pair[0], pair[1])
            elif pair[1] == -2:
                self.message = "Opponent close the game\n" + self.who_win()
        except:
            self.message = "Lost connection\n" + self.who_win()
        if self.online is not None:
            if not self.online.is_work:
                self.message = 'Connection lost\n' + self.who_win()
        if len(self.valid_path) == 0:
            self.person = 1 if self.person == -1 else -1
            self.valid_path = self.get_valid_path()
            if len(self.valid_path) == 0:
                if self.size*self.size == self.points[-1]+self.points[1]:
                    self.message = self.who_win()
                else:
                    self.message = "Steps End\n"+self.who_win()

    def who_win(self):
        if self.points[-1] == self.points[1]:
            return "Tie!"
        elif self.points[-1] > self.points[1]:
            return "Black win!"
        else:
            return "White win!"


class ReversWithBlackHall(Revers):
    def start(self):
        Revers.start(self)
        success = False
        while not success:
            x = randint(0, self.size-1)
            y = randint(0, self.size-1)
            if self.field[x][y] == 0:
                self.field[x][y] = 2
                success = True
