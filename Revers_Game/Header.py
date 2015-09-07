from pygame.locals import USEREVENT
from pygame import MOUSEBUTTONUP
from random import randint
import os
import pygame
from enum import Enum
from random import shuffle
from time import sleep
import re


END_SCENE = USEREVENT + 1
PASSIVE = 500
WHITE = (255, 255, 255)


def mouse_in(mouse, start, end):
    return (start[0] < mouse[0] < end[0]) and (start[1] < mouse[1] < end[1])


ipReg = \
    re.compile(r'^(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[0-9])'
               r'(\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[0-9])){2}'
               r'(\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[1-9]))$')


def is_it_ip(ip):
    if ipReg.match(ip) is None:
        return False
    return True


def is_in_4_to_20(value):
    int_value = 0
    try:
        int_value = int(value)
    except:
        return False
    return 4 <= int_value <= 20


def play_music():
    play_list = ["Cafe_Del_Mare_-_Sun_Is_Shinnig.ogg",
                 "Cafe_Del_Mare_-_relax.ogg",
                 "Cafe_Del_Mare_-_I_Don_39_t_Care.ogg",
                 "Cafe_Del_Mare_-_Beautiful_Morning.ogg",
                 "Cafe_del_mare_-_Thomas_newman.ogg"]
    [shuffle(play_list) for i in range(0, 10)]
    track = {True: None, False: None}
    index = True
    work = len(play_list)
    while work > 0:
        work = len(play_list)
        for i in play_list:
            try:
                track[index] = get_music(i)
                if track[index is False] is not None:
                    sleep(track[index is False].get_length())
                track[index].play()
                track[index].set_volume(0.3)
                index = not index
                print("Now playing {}".format(i[:len(i)-4]))
            except Exception:
                work -= 1
                break


def get_music(name):
    fullname = os.path.join('data', os.path.join('music', name))
    return pygame.mixer.Sound(fullname)


class Player:
    def man(self, event):
        pair = -1, 0
        if MOUSEBUTTONUP in event:
            pair = self.interface.event()
        if self.online is not None:
            self.online.send_pickle(0, pair)
        return pair

    def pc(self, event):
        maxValue = -1
        pairs = []
        for key in self.valid_path:
            if len(self.valid_path[key]) == maxValue:
                pairs.append(key)
            if len(self.valid_path[key]) > maxValue:
                pairs = [key]
                maxValue = len(self.valid_path[key])
        if pairs:
            rnd = randint(0, len(pairs)-1)
            return pairs[rnd]
        else:
            return -1, 0

    def online(self, event):
        return self.online.get_pickle(0)


class Img(Enum):
    background = 0
    load_background = 1
    logo = 2
    point_b = 3
    point_w = 4
    block_b = 5
    block_w = 6
    point = 7
    black_hall = 8
    left_substrate = 9
    right_substrate = 10
    radio_select = 11
    radio_no_select = 12
    select_stock_point = 13
    deselect_stock_point = 14
    select_politics_point = 15
    deselect_politics_point = 16
    step_black = 17
    step_white = 18
    loading_end = 19


class Opt(Enum):
    full_screen = 0
    width = 1
    height = 2
    point_b = 3
    point_w = 4
    block_b = 5
    block_w = 6
    point = 7
    background = 8
    black_hall = 9


class ME(Enum):
    main = 0
    options = 1
    online = 2
    message = 3


class GM(Enum):
    pc = 0
    player = 1
    online = 2
    origin = 3
    with_black_hall = 4
    host = 5
    client = 6
    offline = 7

    opponent = 8
    type = 9
    game_online = 10
    size = 11
    rnd = 12
    field = 13
    person = 14


class MUS(Enum):
    menu = 0
    step = 1


class MSG(Enum):
    """list of messages"""
    """Low level messages"""
    max_contacts = 0
    id = 1
    map_name = 2
    map_data = 3
    exit = 4
