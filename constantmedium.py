# Custom libraries
from hittable import Hittable, HitRecord
from material import Isotropic
from vec3 import Vec3
from aabb import AABB

# 3rd party libraries
from random import random
from math import log


class ConstantMedium(Hittable):
    '''Fills a boundary with a constant medium (based on its negative inverse density) and a phase function'''

    def __init__(self, b, d, a):
        self.boundary = b
        self.neg_inv_density = -1 / d
        self.phase_function = Isotropic(a)

    def bounding_box(self, t0, t1, output_box):
        temp_box = AABB()
        if self.boundary.bounding_box(t0, t1, temp_box):
            output_box.replace_values(temp_box)
            return True
        return False

    def hit(self, ray, t_min, t_max, rec):
        rec1 = HitRecord()
        rec2 = HitRecord()

        if not self.boundary.hit(ray, float('-inf'), float('inf'), rec1):
            return False
        
        if not self.boundary.hit(ray, rec1.t + 0.0001, float('inf'), rec2):
            return False

        ray_length = ray.dir.length()
        distance_inside_boundary = (rec2.t - rec1.t) * ray_length
        hit_distance = self.neg_inv_density * log(random())

        if hit_distance > distance_inside_boundary:
            return False
        
        rec.t = rec1.t + hit_distance / ray_length
        rec.p = ray.at(rec.t)
        rec.normal = Vec3(1, 0, 0) # Arbitrary
        rec.front_face = True # Arbitrary
        rec.mat = self.phase_function
        rec.u = rec1.u
        rec.v = rec1.v
        return True
