# 3rd party libraries
from math import sqrt, pi, cos, sin
from random import uniform, random


class Vec3:
    '''3D vector storing XYZ coordinates and multiple helper functions'''

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __getitem__(self, key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.z
        return None

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        if key == 1:
            self.y = value
        if key == 2:
            self.z = value

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        assert not isinstance(other, Vec3)
        return Vec3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return Vec3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        if other == 0:
            return Vec3(float('NaN'), float('NaN'), float('NaN'))
        return Vec3(self.x / other, self.y / other, self.z / other)

    def copy(self):
        return Vec3(self.x, self.y, self.z)

    def length(self):
        return sqrt(self.length_squared())

    def length_squared(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vec3(x, y, z)

    def unit_vector(self):
        return self / self.length()

    def reflect(self, other):
        return self - 2 * self.dot(other) * other
    
    def refract(self, other, etai_over_etat):
        cos_theta = (-self).dot(other)
        r_out_perp = etai_over_etat * (self + cos_theta * other)
        r_out_parallel = -sqrt(abs(1.0 - r_out_perp.length_squared())) * other
        return r_out_perp + r_out_parallel

    def replace_values(self, other):
        self.x = other.x
        self.y = other.y
        self.z = other.z

    @classmethod
    def random(self, minimum=0, maximum=1):
        return Vec3(uniform(minimum, maximum), uniform(minimum, maximum), uniform(minimum, maximum))

    @classmethod
    def random_in_unit_sphere(self):
        while True:
            p = Vec3.random(-1, 1)
            if p.length_squared() >= 1: continue
            return p

    @classmethod
    def random_unit_vector(self):
        a = uniform(0, 2 * pi)
        z = uniform(-1, 1)
        r = sqrt(1 - z * z)
        return Vec3(r * cos(a), r * sin(a), z)

    @classmethod
    def random_in_hemisphere(self, normal):
        in_unit_sphere = Vec3.random_in_unit_sphere()
        if in_unit_sphere.dot(normal) > 0.0:
            return in_unit_sphere
        return - in_unit_sphere

    @classmethod
    def random_in_unit_disk(self):
        while True:
            p = Vec3(uniform(-1, 1), uniform(-1, 1), 0)
            if p.length_squared() >= 1:
                continue
            return p

    @classmethod
    def random_cosine_direction(self):
        r1 = random()
        r2 = random()
        z = sqrt(1 - r2)

        phi = 2 * pi * r1
        x = cos(phi) * sqrt(r2)
        y = sin(phi) * sqrt(r2)

        return Vec3(x, y, z)

    @classmethod
    def random_to_sphere(self, radius, distance_squared):
        r1 = random()
        r2 = random()
        z = 1 + r2 * (sqrt(1 - radius * radius / distance_squared) - 1)

        phi = 2 * pi * r1
        x = cos(phi) * sqrt(1 - z * z)
        y = sin(phi) * sqrt(1 - z * z)

        return Vec3(x, y, z)