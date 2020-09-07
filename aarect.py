# Custom libraries
from hittable import Hittable, HitRecord
from aabb import AABB
from point3 import Point3
from vec3 import Vec3
from ray import Ray

# 3rd party library
from random import uniform


class xyRect(Hittable):
    '''Rectangle in the XY-plane'''

    def __init__(self, x0, x1, y0, y1, k, material):
        self.x0  = x0
        self.x1  = x1
        self.y0  = y0
        self.y1  = y1
        self.k   = k
        self.mat = material

    def bounding_box(self, t0, t1, output_box):
        output_box.replace_values(AABB(Point3(self.x0, self.y0, self.k - 0.0001), Point3(self.x1, self.y1, self.k + 0.0001)))
        return True

    def hit(self, ray, t_min, t_max, rec):
        t = (self.k - ray.orig.z) / ray.dir.z
        if t < t_min or t > t_max:
            return False

        x = ray.orig.x + t * ray.dir.x
        y = ray.orig.y + t * ray.dir.y

        if x < self.x0 or x > self.x1 or y < self.y0 or y > self.y1:
            return False
        
        rec.u = (x - self.x0) / (self.x1 - self.x0)
        rec.v = (y - self.y0) / (self.y1 - self.y0)
        rec.t = t
        outward_normal = Vec3(0, 0, 1)
        rec.set_face_normal(ray, outward_normal)
        rec.mat = self.mat
        rec.p = ray.at(t)
        return True

    def pdf_value(self, origin, v):
        rec = HitRecord()

        if not self.hit(Ray(origin, v), 0.001, float('inf'), rec):
            return 0

        area = (self.x1 - self.x0) * (self.y1 - self.y0)
        distance_squared = rec.t * rec.t * v.length_squared()
        cosine = abs(v.dot(rec.normal) / v.length())

        return distance_squared / (cosine * area)

    def random(self, origin):
        random_point = Point3(uniform(self.x0, self.x1), uniform(self.y0, self.y1), self.k + 0.001)
        return random_point - origin


class xzRect(Hittable):
    '''Rectangle in the XZ-plane'''

    def __init__(self, x0, x1, z0, z1, k, material):
        self.x0  = x0
        self.x1  = x1
        self.z0  = z0
        self.z1  = z1
        self.k   = k
        self.mat = material

    def bounding_box(self, t0, t1, output_box):
        output_box.replace_values(AABB(Point3(self.x0, self.k - 0.0001, self.z0), Point3(self.x1, self.k + 0.0001, self.z1)))
        return True

    def hit(self, ray, t_min, t_max, rec):
        t = (self.k - ray.orig.y) / ray.dir.y
        if t < t_min or t > t_max:
            return False

        x = ray.orig.x + t * ray.dir.x
        z = ray.orig.z + t * ray.dir.z

        if x < self.x0 or x > self.x1 or z < self.z0 or z > self.z1:
            return False
        
        rec.u = (x - self.x0) / (self.x1 - self.x0)
        rec.v = (z - self.z0) / (self.z1 - self.z0)
        rec.t = t
        outward_normal = Vec3(0, 1, 0)
        rec.set_face_normal(ray, outward_normal)
        rec.mat = self.mat
        rec.p = ray.at(t)
        return True

    def pdf_value(self, origin, v):
        rec = HitRecord()

        if not self.hit(Ray(origin, v), 0.001, float('inf'), rec):
            return 0

        area = (self.x1 - self.x0) * (self.z1 - self.z0)
        distance_squared = rec.t * rec.t * v.length_squared()
        cosine = abs(v.dot(rec.normal) / v.length())

        return distance_squared / (cosine * area)

    def random(self, origin):
        random_point = Point3(uniform(self.x0, self.x1), self.k + 0.001, uniform(self.z0, self.z1))
        return random_point - origin


class yzRect(Hittable):
    '''Rectangle in the YZ-plane'''

    def __init__(self, y0, y1, z0, z1, k, material):
        self.y0  = y0
        self.y1  = y1
        self.z0  = z0
        self.z1  = z1
        self.k   = k
        self.mat = material

    def bounding_box(self, t0, t1, output_box):
        output_box.replace_values(AABB(Point3(self.k - 0.0001, self.y0, self.z0), Point3(self.k + 0.0001, self.y1, self.z1)))
        return True

    def hit(self, ray, t_min, t_max, rec):
        t = (self.k - ray.orig.x) / ray.dir.x
        if t < t_min or t > t_max:
            return False
        
        y = ray.orig.y + t * ray.dir.y
        z = ray.orig.z + t * ray.dir.z

        if y < self.y0 or y > self.y1 or z < self.z0 or z > self.z1:
            return False

        rec.u = (y - self.y0) / (self.y1 - self.y0)
        rec.v = (z - self.z0) / (self.z1 - self.z0)
        rec.t = t
        outward_normal = Vec3(1, 0, 0)
        rec.set_face_normal(ray, outward_normal)
        rec.mat = self.mat
        rec.p = ray.at(t)
        return True

    def pdf_value(self, origin, v):
        rec = HitRecord()

        if not self.hit(Ray(origin, v), 0.001, float('inf'), rec):
            return 0

        area = (self.y1 - self.y0) * (self.z1 - self.z0)
        distance_squared = rec.t * rec.t * v.length_squared()
        cosine = abs(v.dot(rec.normal) / v.length())

        return distance_squared / (cosine * area)

    def random(self, origin):
        random_point = Point3(self.k + 0.001, uniform(self.y0, self.y1), uniform(self.z0, self.z1))
        return random_point - origin