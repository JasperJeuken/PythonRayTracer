# Custom libraries
from hittable import Hittable, HitRecord
from material import Lambertian, Metal
from aabb import AABB

# 3rd party library
from random import uniform


class HittableList(Hittable):
    '''Store a list of hittable objects'''

    def __init__(self, objects=[]):
        if not isinstance(objects, list):
            self.objects = [objects]
        else:
            self.objects = objects

    def clear(self):
        self.objects = []
    
    def add(self, obj):
        self.objects.append(obj)

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, key):
        return HittableList(self.objects[key])

    def bounding_box(self, t0, t1, output_box):
        if len(self.objects) == 0:
            return False

        temp_box = AABB()
        first_box = True

        for obj in self.objects:
            if not obj.bounding_box(t0, t1, temp_box):
                if first_box:
                    output_box = temp_box
                else:
                    output_box.replace_values(AABB.surrounding_box(output_box, temp_box))
                first_box = False
        
        return True

    def hit(self, r_in, t_min, t_max, rec):
        temp = HitRecord()
        dist_min = t_max
        hit_anything = False

        for obj in self.objects:
            if obj.hit(r_in, t_min, dist_min, temp):
                hit_anything = True
                dist_min = temp.t
                rec.replace_values(temp)
        
        return hit_anything

    def pdf_value(self, o, v):
        weight = 1.0 / len(self.objects)
        s = 0.0

        for obj in self.objects:
            s += weight * obj.pdf_value(o, v)
        
        return s

    def random(self, o):
        int_size = int(len(self.objects))
        return self.objects[int(uniform(0, int_size))].random(o)