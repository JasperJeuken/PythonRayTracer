# 3rd party library
from math import pi


def deg_to_rad(deg):
    '''Convert degrees to radians'''
    return deg * pi / 180.0


def clamp(x, min, max):
    '''Restrict a value between a minimum and a maximum value'''
    if x < min:
        return min
    if x > max:
        return max
    return x