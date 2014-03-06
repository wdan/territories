# -*- coding: utf-8 -*-

from util import interp
from random import randint


class Constraint(object):

    C = -10

    def __init__(self, x1, y1, x2, y2, mid_x, mid_y):
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.mid_x = mid_x
        self.mid_y = mid_y

    def get_constraint(self, degree):
        (xA, yA) = interp(self.mid_x, self.mid_y, self.x1, self.y1, degree *
                          self.C)
        (xB, yB) = interp(self.mid_x, self.mid_y, self.x2, self.y2, degree *
                          self.C)
        return (xA, yA, xB, yB)

    def get_y(self, degree, x):
        (xA, yA, xB, yB) = self.get_constraint(degree)
        if x <= xA:
            return yA
        elif x >= xB:
            return yB
        else:
            return x * (yB - yA) / (xB - xA)

    def get_random_coordinate(self, degree):
        (xA, yA, xB, yB) = self.get_constraint(degree)
        x = randint(xA, xB)
        y = self.get_y(degree, x)
        return (x, y)
