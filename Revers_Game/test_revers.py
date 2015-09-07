__author__ = 'Андрей'
import header
from game import Revers, ReversWithBlackHall
import unittest

real_fields =\
    [[[0, 0, 0, 0], [0, -1, 1, 0], [0, 1, 1, 1], [0, 0, 0, 0]],
     [[0, 0, 0, 0], [0, -1, 1, 0], [0, 1, -1, 1], [0, 0, 0, -1]],
     [[0, 0, 0, 0], [0, -1, 1, 0], [0, 1, 1, 1], [0, 0, 1, -1]],
     [[0, 0, 0, 0], [0, -1, -1, -1], [0, 1, 1, -1], [0, 0, 1, -1]],
     [[0, 0, 1, 0], [0, -1, 1, -1], [0, 1, 1, -1], [0, 0, 1, -1]],
     [[0, 0, 1, 0], [0, -1, 1, -1], [0, -1, -1, -1], [0, -1, -1, -1]],
     [[0, 0, 1, 0], [1, 1, 1, -1], [0, -1, -1, -1], [0, -1, -1, -1]],
     [[0, -1, 1, 0], [1, -1, -1, -1], [0, -1, -1, -1], [0, -1, -1, -1]],
     [[0, -1, 1, 0], [1, 1, -1, -1], [1, -1, -1, -1], [0, -1, -1, -1]],
     [[0, -1, -1, -1], [1, 1, -1, -1], [1, -1, -1, -1], [0, -1, -1, -1]],
     [[0, -1, -1, -1], [1, 1, -1, -1], [1, -1, -1, -1], [0, -1, -1, -1]],
     [[0, -1, -1, -1], [1, 1, -1, -1], [1, -1, -1, -1], [0, -1, -1, -1]]]

real_steps = [(2, 3),
              (3, 3),
              (3, 2),
              (1, 3),
              (0, 2),
              (3, 1),
              (1, 0),
              (0, 1),
              (2, 0),
              (0, 3),
              (0, 0),
              (3, 0)]


real_valid_path = \
    [{(1, 3): [(1, 2)], (3, 1): [(2, 1)], (3, 3): [(2, 2)]},
     {(0, 1): [(1, 1)], (1, 0): [(1, 1)], (3, 2): [(2, 2)]},
     {(1, 3): [(1, 2), (2, 3)], (3, 1): [(2, 1), (3, 2)]},
     {(0, 1): [(1, 1)], (0, 3): [(1, 2)], (0, 0): [(1, 1)], (0, 2): [(1, 2)]},
     {(0, 1): [(1, 2)], (2, 0): [(2, 1), (2, 2)], (3, 1): [(2, 2), (2, 1), (3, 2)]},
     {(3, 0): [(2, 1)], (2, 0): [(1, 1)], (1, 0): [(1, 1)]},
     {(0, 1): [(1, 1), (1, 2)], (0, 3): [(1, 2)], (0, 0): [(1, 1)]},
     {(2, 0): [(1, 1)], (0, 0): [(0, 1)]},
     {(0, 3): [(0, 2)], (0, 0): [(1, 1)]},
     {},
     {},
     {}]


class MyTestCase(unittest.TestCase):
    def test_ip_check(self):
        self.assertEqual(header.is_it_ip("192.168.0.1"), True)
        self.assertEqual(header.is_it_ip("255.255.255.255"), True)
        self.assertEqual(header.is_it_ip("1.001.1.1"), True)
        self.assertEqual(header.is_it_ip("192.048.007.001"), True)
        self.assertEqual(header.is_it_ip("192.168.0.0"), False)
        self.assertEqual(header.is_it_ip("192.168.0.256"), False)
        self.assertEqual(header.is_it_ip("192.168.0.0.1"), False)
        self.assertEqual(header.is_it_ip("192.0.1"), False)

    def test_reverse(self):
        test_game = Revers(4,
                           None,
                           header.Player().man,
                           header.Player().man,
                           0,
                           None)
        test_game.start()
        test_game.active = True
        for i in range(0, len(real_steps)):
            test_game.active = True
            test_game.descend(real_steps[i][0], real_steps[i][1])
            test_field = test_game.field
            self.assertEqual(test_field, real_fields[i])
            test_vp = test_game.valid_path
            self.assertEqual(test_vp, real_valid_path[i])
