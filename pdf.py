# Custom libraries
from vec3 import Vec3
from onb import ONB
from point3 import Point3

# 3rd party libraries
from math import pi
from random import random


class PDF:
    '''Parent class for storing probability density functions'''

    def __init__(self):
        pass

    def value(self, direction):
        pass
    
    def generate(self):
        pass


class CosinePDF(PDF):
    '''Cosine probability density function stored as an orthonormal basis'''

    def __init__(self, w):
        self.uvw = ONB()
        self.uvw.build_from_w(w)

    def value(self, direction):
        cosine = direction.unit_vector().dot(self.uvw.w())
        if cosine <= 0:
            return 0
        return cosine / pi

    def generate(self):
        return self.uvw.local(Vec3.random_cosine_direction())


class HittablePDF(PDF):
    '''Probabiltiy density function stored as a hittable object with an origin point'''

    def __init__(self, p, origin):
        self.p = p
        self.o = origin

    def value(self, direction):
        return self.p.pdf_value(self.o, direction)

    def generate(self):
        return self.p.random(self.o)


class MixturePDF(PDF):
    '''Probability density function consisting of two other PDFs'''

    def __init__(self, p0, p1):
        self.p = [p0, p1]

    def value(self, direction):
        return 0.5 * self.p[0].value(direction) + 0.5 * self.p[1].value(direction)

    def generate(self):
        if random() < 0.5:
            return self.p[0].generate()
        return self.p[1].generate()