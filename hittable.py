# Custom libraries
from aabb import AABB
from ray import Ray
from utils import deg_to_rad
from point3 import Point3
from vec3 import Vec3

# 3rd party library
from math import sin, cos


class HitRecord:
    '''Stores information when a ray hits a hittable object'''

    def __init__(self):
        pass

    def set_face_normal(self, ray, outward_normal):
        self.front_face = (ray.dir.dot(outward_normal) < 0)
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = - outward_normal

    def replace_values(self, other):
        self.t = other.t
        self.p = other.p
        self.mat = other.mat
        self.normal = other.normal
        self.front_face = other.front_face
        self.u = other.u
        self.v = other.v

    def clear(self):
        self.t = float('inf')


class Hittable:
    '''Parent class storing geometric information about a hittable object'''

    def __init__(self):
        pass

    def hit(self, ray, t_min, t_max, rec):
        pass

    def bounding_box(self, t0, t1, output_box):
        pass

    def pdf_value(self, o, v):
        return 0.0

    def random(self, o):
        return Vec3(1, 1, 1)


class Translate(Hittable):
    '''Translate a hittable object with a vector indicating the displacement'''

    def __init__(self, obj, displacement):
        self.obj = obj
        self.offset = displacement

    def bounding_box(self, t0, t1, output_box):
        if not self.obj.bounding_box(t0, t1, output_box):
            return False
        output_box.replace_values(AABB(output_box._min + self.offset, output_box._max + self.offset))
        return True

    def hit(self, ray, t_min, t_max, rec):
        moved_r = Ray(ray.orig - self.offset, ray.dir, ray.time)

        if not self.obj.hit(moved_r, t_min, t_max, rec):
            return False
        
        rec.p += self.offset
        rec.set_face_normal(moved_r, rec.normal)
        return True


class RotateY(Hittable):
    '''Rotate a hittable object with an angle indicating the rotation about the Y-axis'''

    def __init__(self, obj, angle):
        self.obj = obj

        radians = deg_to_rad(angle)
        self.sin_theta = sin(radians)
        self.cos_theta = cos(radians)

        self.bbox = AABB()
        self.hasbox = obj.bounding_box(0, 1, self.bbox)

        _min = Point3( float('inf'),  float('inf'),  float('inf'))
        _max = Point3(float('-inf'), float('-inf'), float('-inf'))

        for i in range(2):
            for j in range(2):
                for k in range(2):
                    x = i * self.bbox._max.x + (1 - i) * self.bbox._min.x
                    y = j * self.bbox._max.y + (1 - j) * self.bbox._min.y
                    z = k * self.bbox._max.z + (1 - k) * self.bbox._min.z

                    newx =  self.cos_theta * x + self.sin_theta * z
                    newz = -self.sin_theta * x + self.cos_theta * z

                    tester = Vec3(newx, y, newz)

                    for c in range(3):
                        _min[c] = min(_min[c], tester[c])
                        _max[c] = max(_max[c], tester[c])

        self.bbox = AABB(_min, _max)

    def bounding_box(self, t0, t1, output_box):
        output_box.replace_values(self.bbox)
        return self.hasbox

    def hit(self, ray, t_min, t_max, rec):
        origin = ray.orig.copy()
        direction = ray.dir.copy()

        origin[0] = self.cos_theta * ray.orig[0] - self.sin_theta * ray.orig[2]
        origin[2] = self.sin_theta * ray.orig[0] + self.cos_theta * ray.orig[2]

        direction[0] = self.cos_theta * ray.dir[0] - self.sin_theta * ray.dir[2]
        direction[2] = self.sin_theta * ray.dir[0] + self.cos_theta * ray.dir[2]

        rotated_r = Ray(origin, direction, ray.time)

        if not self.obj.hit(rotated_r, t_min, t_max, rec):
            return False
        
        p = rec.p.copy()
        normal = rec.normal.copy()

        p[0] =  self.cos_theta * rec.p[0] + self.sin_theta * rec.p[2]
        p[2] = -self.sin_theta * rec.p[0] + self.cos_theta * rec.p[2]

        normal[0] =  self.cos_theta * rec.normal[0] + self.sin_theta * rec.normal[2]
        normal[2] = -self.sin_theta * rec.normal[0] + self.cos_theta * rec.normal[2]

        rec.p = p
        rec.set_face_normal(rotated_r, normal)

        return True


class FlipFace(Hittable):
    '''Flip a rectangle about the axis normal to its surface'''

    def __init__(self, p):
        self.p = p

    def bounding_box(self, t0, t1, output_box):
        return self.p.bounding_box(t0, t1, output_box)

    def hit(self, ray, t_min, t_max, rec):
        if not self.p.hit(ray, t_min, t_max, rec):
            return False
        rec.front_face = not rec.front_face
        return True