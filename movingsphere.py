# Custom libraries
from hittable import Hittable
from aabb import AABB
from vec3 import Vec3
from sphere import Sphere

# 3rd party library
from math import sqrt, atan2, asin, pi


class MovingSphere(Hittable):
    '''Sphere which moves from one point to another in a given time (for simulating motion blur)'''

    def __init__(self, center0, center1, t0, t1, radius, material):
        self.center0 = center0
        self.center1 = center1
        self.time0 = t0
        self.time1 = t1
        self.r = radius
        self.mat = material

    def center(self, time):
        return self.center0 + ((time - self.time0) / (self.time1 - self.time0)) * (self.center1 - self.center0)

    def bounding_box(self, t0, t1, output_box):
        self.box0 = AABB(self.center(t0) - Vec3(self.r, self.r, self.r), self.center(t0) + Vec3(self.r, self.r, self.r))
        self.box1 = AABB(self.center(t1) - Vec3(self.r, self.r, self.r), self.center(t1) + Vec3(self.r, self.r, self.r))
        output_box.replace_values(AABB.surrounding_box(self.box0, self.box1))
        return True

    def hit(self, ray, t_min, t_max, hit_rec):
        oc = ray.orig - self.center(ray.time)
        
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
                outward_normal = (hit_rec.p - self.center(ray.time)) / self.r
                get_sphere_uv((hit_rec.p - self.center(ray.time)) / self.r, hit_rec)
                hit_rec.set_face_normal(ray, outward_normal)
                hit_rec.mat = self.mat
                return True

            temp = (-half_b + root) / a
            if t_min < temp < t_max:
                hit_rec.t = temp
                hit_rec.p = ray.at(hit_rec.t)
                outward_normal = (hit_rec.p - self.center(ray.time)) / self.r
                get_sphere_uv((hit_rec.p - self.center(ray.time)) / self.r, hit_rec)
                hit_rec.set_face_normal(ray, outward_normal)
                hit_rec.mat = self.mat
                return True
        return False


def get_sphere_uv(p, hit_rec):
    '''Calculate UV coordinates on a sphere'''
    phi = atan2(p.z, p.x)
    theta = asin(p.y)
    hit_rec.u = 1 - (phi + pi) / (2 * pi)
    hit_rec.v = (theta + pi / 2) / pi