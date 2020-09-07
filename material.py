# Custom libraries
from ray import Ray
from vec3 import Vec3
from color import Color
from texture import *
from onb import ONB
from pdf import *

# 3rd party libraries
from math import sqrt, pi
from random import random


class ScatterRecord:
    '''Class to store ray properties when a ray hits a material'''

    def __init__(self):
        pass

    def replace_values(self, other):
        self.specular_ray = other.specular_ray
        self.is_specular = other.is_specular
        self.attenuation = other.attenuation
        self.pdf_ptr = other.pdf_ptr


class Material:
    '''Parent material class storing light interaction properties of certain material types'''

    def __init__(self):
        pass

    def scatter(self, ray, rec, srec):
        return False

    def scattering_pdf(self, ray, rec, scattered):
        return 0

    def emitted(self, ray, rec, u, v, p):
        return Color(0, 0, 0)


class Lambertian(Material):
    '''Diffusive material properties stored as a texture'''

    def __init__(self, albedo):
        if isinstance(albedo, Color) or isinstance(albedo, Vec3):
            self.a = SolidColor(albedo)
        else:
            self.a = albedo

    def scatter(self, ray, rec, srec):
        srec.is_specular = False
        srec.attenuation = self.a.value(rec.u, rec.v, rec.p)
        srec.pdf_ptr = CosinePDF(rec.normal)
        return True
        #uvw = ONB()
        #uvw.build_from_w(rec.normal)
        #direction = uvw.local(Vec3.random_cosine_direction())
        #scattered.replace_values(Ray(rec.p, direction.unit_vector(), ray.time))
        #alb.replace_values(self.a.value(rec.u, rec.v, rec.p))
        #pdf.replace_values(Carry(uvw.w().dot(scattered.dir) / pi))
        #return True

    def scattering_pdf(self, ray, rec, scattered):
        cosine = rec.normal.dot(scattered.dir.unit_vector())
        if cosine < 0:
            return 0
        return cosine / pi


class Metal(Material):
    '''Metallic (reflective) material stored as a texture and a fuzz variable indicating the clearness of the reflections'''

    def __init__(self, albedo, fuzz=0.0):
        self.a = albedo
        if fuzz < 1:
            self.fuzz = fuzz
        else:
            self.fuzz = 1

    def scatter(self, ray, rec, srec):
        reflected = ray.dir.unit_vector().reflect(rec.normal)
        srec.specular_ray = Ray(rec.p, reflected + self.fuzz * Vec3.random_in_unit_sphere())
        srec.attenuation = self.a
        srec.is_specular = True
        srec.pdf_ptr = 0
        return True
        #reflected = ray.dir.unit_vector().reflect(rec.normal)
        #scattered.replace_values(Ray(rec.p, reflected + self.fuzz * Vec3.random_in_hemisphere(rec.normal), ray.time))
        #attenuation.replace_values(self.a)
        #return (scattered.dir.dot(rec.normal) > 0)


class Dielectric(Material):
    '''Glass material stored with a refractive index and Schlick-approximated refracting'''

    def __init__(self, ref_idx):
        self.ref_idx = ref_idx

    def schlick(self, cosine, ref_idx):
        r0 = (1 - ref_idx) / (1 + ref_idx)
        r0 = r0 * r0
        return r0 + (1 - r0) * pow(1 - cosine, 5)

    def refract(self, v, n, ni_over_nt, refracted):
        uv = v.unit_vector()
        dt = uv.dot(n)
        discriminant = 1.0 - ni_over_nt * ni_over_nt * (1 - dt * dt)
        if discriminant > 0:
            refracted.replace_values(ni_over_nt * (uv - n * dt) - n * sqrt(discriminant))
            return True
        return False

    def scatter(self, ray, rec, srec):
        srec.is_specular = True
        srec.pdf_ptr = 0
        srec.attenuation = Vec3(1.0, 1.0, 1.0)
        outward_normal = Vec3()
        reflected = ray.dir.reflect(rec.normal)
        refracted = Vec3()

        if ray.dir.dot(rec.normal) > 0:
            outward_normal = -rec.normal
            ni_over_nt = self.ref_idx
            cosine = self.ref_idx * ray.dir.dot(rec.normal) / ray.dir.length()
        else:
            outward_normal = rec.normal
            ni_over_nt = 1.0 / self.ref_idx
            cosine = -ray.dir.dot(rec.normal) / ray.dir.length()

        if self.refract(ray.dir, outward_normal, ni_over_nt, refracted):
            reflect_prob = self.schlick(cosine, self.ref_idx)
        else:
            reflect_prob = 1.0

        if random() < reflect_prob:
            srec.specular_ray = Ray(rec.p, reflected)
        else:
            srec.specular_ray = Ray(rec.p, refracted)
        return True


class DiffuseLight(Material):
    '''(Colourable) material emitting light, stored as a texture'''

    def __init__(self, a):
        if isinstance(a, Color):
            self.emit = SolidColor(a)
        else:
            self.emit = a

    def emitted(self, ray, rec, u, v, p):
        if rec.front_face:
            return self.emit.value(u, v, p)
        else:
            return Color(0, 0, 0)


class Isotropic(Material):
    '''Material for a constant (gaseous) medium'''

    def __init__(self, a):
        if isinstance(a, Color):
            self.albedo = SolidColor(a)
        else:
            self.albedo = a

    def scatter(self, ray, rec, attenuation, scattered):
        scattered.replace_values(Ray(rec.p, Vec3.random_in_unit_sphere(), ray.time))
        attenuation.replace_values(self.albedo.value(rec.u, rec.v, rec.p))
        return True