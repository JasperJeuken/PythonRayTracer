# Custom library
from point3 import Point3


class AABB:
    '''Axis-aligned bounding box stored with two points'''

    def __init__(self, a=Point3(0, 0, 0), b=Point3(0, 0, 0)):
        self._min = a
        self._max = b

    def hit(self, ray, tmin, tmax):
        for a in range(3):
            inv_dir = 1.0 / ray.dir[a]
            t0 = (self._min[a] - ray.orig[a]) * inv_dir
            t1 = (self._max[a] - ray.orig[a]) * inv_dir

            if inv_dir < 0.0:
                temp = t0
                t0 = t1
                t1 = temp

            if t0 > tmin:
                tmin = t0
            if t1 < tmax:
                tmax = t1

            if tmax <= tmin:
                return False
        return True

    def replace_values(self, other):
        self._min = other._min
        self._max = other._max

    @classmethod
    def surrounding_box(self, box0, box1):
        small = Point3(min(box0._min.x, box1._min.x), min(box0._min.y, box1._min.y), min(box0._min.z, box1._min.z))
        big   = Point3(min(box0._max.x, box1._max.x), min(box0._max.y, box1._max.y), min(box0._max.z, box1._max.z))

        return AABB(small, big)