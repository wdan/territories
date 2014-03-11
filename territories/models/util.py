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


def rotate(l, n):
    return l[n:] + l[:n]


def cross(p0, p1, p2):
    return (p1["x"] - p0["x"]) * (p2["y"] - p0["y"]) - (p2["x"] - p0["x"]) * (p1["y"] - p0["y"])


#def inside_polygon(p, points):
    #eps = 0.0001
    #l = len(points)
    #if l < 3:
        #return False
    #if cross(points[0], p, points[1]) > -eps:
        #return False
    #if cross(points[0], p, points[l - 1]) < eps:
        #return False
    #i, j = 2, l - 1
    #line = -1
    #while i <= j:
        #mid = (i + j) / 2
        #if cross(points[0], p, points[mid]) > -eps:
            #line = mid
            #j = mid - 1
        #else:
            #j = mid + 1
    #return cross(points[line - 1], p, points[line]) < eps
def inside_polygon(x, y, points):
    l = len(points)
    j = l - 1
    ret = False
    for i in xrange(0, l):
        p1 = points[i]
        p2 = points[j]
        if ((p1["y"] > y) != (p2["y"] > y)) and (x < (p2["x"] - p1["x"]) * (y - p1["y"]) / (p2["y"] - p1["y"]) + p1["x"]):
            ret = not ret
        j = i
    return ret
