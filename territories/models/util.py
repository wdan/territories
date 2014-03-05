# -*- coding: utf-8 -*-

import math


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftMin = leftMin - 20
    leftMax = leftMax + 20
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def vector_norm(x1, y1, x2, y2):
    v = {}
    v["x"] = x2 - x1
    v["y"] = y2 - y1
    v["length"] = math.sqrt(v["x"] * v["x"] + v["y"] * v["y"])
    v["x"] = v["x"] / v["length"]
    v["y"] = v["y"] / v["length"]
    return v


def interp(x1, y1, x2, y2, scale):
    v = vector_norm(x1, y1, x2, y2)
    k = (v["length"] - scale) / v["length"]
    x = k * v["length"] * v["x"] + x1
    y = k * v["length"] * v["y"] + y1
    return (x, y)
