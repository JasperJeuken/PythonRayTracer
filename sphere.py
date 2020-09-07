# Custom libraries
from hittable import Hittable, HitRecord
from aabb import AABB
from vec3 import Vec3
from onb import ONB
from ray import Ray

# 3rd party library
from math import sqrt, atan2, asin, pi


class Sphere(Hittable):
    '''Sphere described by a center, radius and material'''

    def __init__(self, center, radius, material):
        self.c   = center
        self.r   = radius
        self.mat = material

    def bounding_box(self, t0, t1, output_box):
        output_box.replace_values(AABB(self.c - Vec3(self.r, self.r, self.r), self.c + Vec3(self.r, self.r, self.r)))
        return True

    def hit(self, ray, t_min, t_max, hit_rec):
        oc = ray.orig - self.c
        
        a = ray.dir.length_squared()
        half_b = oc.dot(ray.dir)
        c = oc.length_squared() - self.r * self.r

        discriminant = half_b * half_b - a * c

        if discriminant > 0:
            root = sqrt(discriminant)
            
            temp = (-half_b - root) / a
            if t_min < temp < t_max:
                hit_rec.t = temp
                hit_rec.p = ray.at(hit_rec.t)
                outward_normal = (hit_rec.p - self.c) / self.r
                get_sphere_uv((hit_rec.p - self.c) / self.r, hit_rec)
                hit_rec.set_face_normal(ray, outward_normal)
                hit_rec.mat = self.mat
                return True

            temp = (-half_b + root) / a
            if t_min < temp < t_max:
                hit_rec.t = temp
                hit_rec.p = ray.at(hit_rec.t)
                outward_normal = (hit_rec.p - self.c) / self.r
                get_sphere_uv((hit_rec.p - self.c) / self.r, hit_rec)
                hit_rec.set_face_normal(ray, outward_normal)
                hit_rec.mat = self.mat
                return True
        return False

    def pdf_value(self, o, v):
        rec = HitRecord()
        if not self.hit(Ray(o, v), 0.001, float('inf'), rec):
            return 0
    
        cos_theta_max = sqrt(1 - self.r * self.r / (self.c - o).length_squared())
        solid_angle = 2 * pi * (1 - cos_theta_max)

        return 1 / solid_angle

    def random(self, o):
        direction = self.c - o
        distance_squared = direction.length_squared()
        uvw = ONB()
        uvw.build_from_w(direction)
        return uvw.local(Vec3.random_to_sphere(self.r, distance_squared))


def get_sphere_uv(p, hit_rec):
    '''Calculate UV coordinates on a sphere'''
    phi = atan2(p.z, p.x)
    theta = asin(p.y)
    hit_rec.u = 1 - (phi + pi) / (2 * pi)
    hit_rec.v = (theta + pi / 2) / pi