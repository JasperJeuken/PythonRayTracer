# Custom libraries
from hittable import Hittable
from aabb import AABB

# 3rd party library
from random import uniform


class BvhNode(Hittable):
    '''Node in a bounding volume hierarchy for grouping objects together, speeding up rendering by making a tree of nodes'''

    def __init__(self, objects, time0, time1, start=None, end=None):
        self.objects = objects
        self.time0   = time0
        self.time1   = time1

        self.box = AABB()

        if start is None:
            self.start   = 0
        else:
            self.start = start
        if end is None:
            self.end = len(self.objects)
        else:
            self.end = end

        axis = int(uniform(0, 3))

        if axis == 0:
            comparator = self.box_x_compare
        elif axis == 1:
            comparator = self.box_y_compare
        else:
            comparator = self.box_z_compare

        object_span = self.end - self.start

        if object_span == 1:
            self.left  = self.objects[self.start]
            self.right = self.objects[self.start]
        elif object_span == 2:
            if comparator(self.objects[self.start], self.objects[self.start + 1]):
                self.left = self.objects[self.start]
                self.right = self.objects[self.start + 1]
            else:
                self.left = self.objects[self.start + 1]
                self.right = self.objects[self.start]
        else:
            s = sorted(self.objects[self.start:self.end + 1], key=comparator)

            mid = self.start + object_span / 2
            self.left  = BvhNode(self.objects, self.start,      mid, self.time0, self.time1)
            self.right = BvhNode(self.objects,        mid, self.end, self.time0, self.time1)

        box_left = AABB()
        box_right = AABB()
        
        if (not self.left.bounding_box(self.time0, self.time1, box_left)) or (not self.right.bounding_box(self.time0, self.time1, box_right)):
            print('No bounding box in BvhNode constructor')
        
        self.box = AABB.surrounding_box(box_left, box_right)

    def bounding_box(self, t0, t1, output_box):
        output_box.replace_values(self.box)
        return True

    def hit(self, ray, t_min, t_max, rec):
        if not self.box.hit(ray, t_min, t_max):
            return False

        hit_left  = self.left.hit(ray, t_min, t_max, rec)
        hit_right = self.right.hit(ray, t_min, t_max, rec)

        return (hit_left or hit_right)

    def box_compare(self, a, b, axis):
        box_a = AABB()
        box_b = AABB()

        if (not a.bounding_box(0, 0, box_a)) or (not b.bounding_box(0, 0, box_b)):
            print('No bounding box in BvhNode constructor')
            
        return (box_a._min[axis] < box_b._min[axis])

    def box_x_compare(self, b):
        return self.box_compare(self, b, 0)
    
    def box_y_compare(self, b):
        return self.box_compare(self, b, 1)

    def box_z_compare(self, b):
        return self.box_compare(self, b, 2) 
