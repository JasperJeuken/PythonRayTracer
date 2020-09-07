# Custom libraries
from hittable import Hittable, HitRecord
from hittablelist import HittableList
from aabb import AABB
from aarect import *


class Box(Hittable):
    '''Create a box with two given corner points by adding six rectangles as sides'''

    def __init__(self, p0, p1, material):
        self.box_min  = p0
        self.box_max  = p1
        self.mat = material

        self.sides = []

        self.sides.append(xyRect(p0.x, p1.x, p0.y, p1.y, p1.z, material))
        self.sides.append(xyRect(p0.x, p1.x, p0.y, p1.y, p0.z, material))

        self.sides.append(xzRect(p0.x, p1.x, p0.z, p1.z, p1.y, material))
        self.sides.append(xzRect(p0.x, p1.x, p0.z, p1.z, p0.y, material))

        self.sides.append(yzRect(p0.y, p1.y, p0.z, p1.z, p1.x, material))
        self.sides.append(yzRect(p0.y, p1.y, p0.z, p1.z, p0.x, material))

    def bounding_box(self, t0, t1, output_box):
        output_box.replace_values(AABB(self.box_min, self.box_max))
        return True

    def hit(self, ray, t_min, t_max, rec):
        temp = HitRecord()
        dist_min = t_max
        hit_anything = False

        for obj in self.sides:
            if obj.hit(ray, t_min, dist_min, temp):
                hit_anything = True
                dist_min = temp.t
                rec.replace_values(temp)
        
        return hit_anything