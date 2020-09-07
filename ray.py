# Custom libraries
from point3 import Point3
from vec3 import Vec3


class Ray:
    '''A ray described by an origin, direction and time (for motion blur)'''

    def __init__(self, origin=Point3(0, 0, 0), direction=Vec3(1, 1, 1), time=0.0):
        self.orig = origin
        self.dir = direction
        self.time = time

    def at(self, t):
        return self.orig + t * self.dir

    def __str__(self):
        return f'orig: {self.orig}, dir: {self.dir}'

    def replace_values(self, other):
        self.orig = other.orig
        self.dir = other.dir
        self.time = other.time