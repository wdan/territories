# -*- coding: utf-8 -*-

from util import interp
from random import uniform


class Constraint(object):

    C = -20

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
        degree = min(degree, 3)
        (xA, yA) = interp(self.mid_x, self.mid_y, self.x1, self.y1, degree *
                          self.C)
        (xB, yB) = interp(self.mid_x, self.mid_y, self.x2, self.y2, degree *
                          self.C)
        return (xA, yA, xB, yB)

    def get_y(self, degree, x):
        degree = min(degree, 3)
        (xA, yA, xB, yB) = self.get_constraint(degree)
        k = (yB - yA) / (xB - xA)
        c = yB - k * xB
        if x < xA:
            return self.get_random_coordinate(degree)
        elif x > xB:
            return self.get_random_coordinate(degree)
        else:
            return (x, x * k + c)

    def get_random_coordinate(self, degree):
        degree = min(degree, 3)
        (xA, yA, xB, yB) = self.get_constraint(degree)
        x = uniform(xA, xB)
        (x, y) = self.get_y(degree, x)
        return (x, y)
