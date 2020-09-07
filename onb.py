# Custom library
from vec3 import Vec3


class ONB:
    '''Orthonormal basis stored as three vectors'''

    def __init__(self):
        self.axis = [Vec3() for _ in range(3)]

    def __getitem__(self, key):
        return self.axis[key]

    def __setitem__(self, key, value):
        self.axis[key] = value

    def u(self):
        return self.axis[0]
    
    def v(self):
        return self.axis[1]
    
    def w(self):
        return self.axis[2]

    def local(self, a):
        return a.x * self.u() + a.y * self.v() + a.z * self.w()

    def build_from_w(self, n):
        self.axis[2] = n.unit_vector()
        if abs(self.w().x) > 0.9:
            a = Vec3(0, 1, 0)
        else:
            a = Vec3(1, 0, 0)
        self.axis[1] = self.w().cross(a).unit_vector()
        self.axis[0] = self.w().cross(self.v())