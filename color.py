# Custom libraries
from vec3 import Vec3
from utils import clamp

# 3rd party library
from math import isnan


class Color(Vec3):
    '''Store color as a 3D vector (RGB)'''

    def write_color(self, samples_per_pixel):
        r = self.x
        g = self.y
        b = self.z

        #if isnan(r):
            #r = 0.0
        #if isnan(g):
            #g = 0.0
        #if isnan(b):
            #b = 0.0

        scl = 1.0 / samples_per_pixel
        gamma = 1.5
        r = pow(scl * r, 1/gamma)
        g = pow(scl * g, 1/gamma)
        b = pow(scl * b, 1/gamma)

        ir = int(256 * clamp(r, 0.0, 0.999))
        ig = int(256 * clamp(g, 0.0, 0.999))
        ib = int(256 * clamp(b, 0.0, 0.999))

        return f'{ir} {ig} {ib} '