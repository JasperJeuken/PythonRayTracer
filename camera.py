# Custom libraries
from point3 import Point3
from vec3 import Vec3
from ray import Ray
from utils import deg_to_rad

# 3rd party libraries
from math import tan
from random import uniform


class Camera:
    '''Stores properties of the camera and generates rays for creating renders'''
    
    def __init__(self, lookfrom, lookat, vup, vfov, aspect_ratio, aperture, focus_dist, t0=0, t1=0):
        self.lookfrom = lookfrom
        self.lookat = lookat
        self.vup = vup
        self.vfov = vfov
        self.aspect_ratio = aspect_ratio
        self.aperture = aperture
        self.focus_dist = focus_dist

        self.theta = deg_to_rad(self.vfov)
        self.h = tan(self.theta / 2)
        self.viewport_height = 2.0 * self.h
        self.viewport_width = self.aspect_ratio * self.viewport_height

        self.w = (self.lookfrom - self.lookat).unit_vector()
        self.u = (self.vup.cross(self.w)).unit_vector()
        self.v = self.w.cross(self.u)

        self.origin = self.lookfrom
        self.horizontal = self.focus_dist * self.viewport_width * self.u
        self.vertical = self.focus_dist * self.viewport_height * self.v
        self.lower_left_corner = self.origin - self.horizontal / 2 - self.vertical / 2 - self.focus_dist * self.w

        self.lens_radius = aperture / 2
        self.time0 = t0
        self.time1 = t1

    def get_ray(self, s, t):
        rd = self.lens_radius * Vec3.random_in_unit_disk()
        offset = self.u * rd.x + self.v * rd.y

        return Ray(self.origin + offset, self.lower_left_corner + s * self.horizontal + t * self.vertical - self.origin - offset, uniform(self.time0, self.time1))