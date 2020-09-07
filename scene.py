# Custom libraries
from point3 import Point3
from vec3 import Vec3
from sphere import Sphere
from movingsphere import MovingSphere
from material import *
from color import Color
from hittablelist import HittableList
from texture import *
from aarect import *
from box import Box
from hittable import *
from constantmedium import ConstantMedium
from bvh import BvhNode

# 3rd party library
from random import random, uniform


class Scene:
    '''Contains the width and height of the image, and the objects and lights in the scene'''

    def __init__(self, camera, world, lights, width, height):
        self.camera = camera
        self.world  = world
        self.width  = width
        self.height = height
        self.lights = lights


def random_scene():
    '''Generate a scene with three main spheres and several randomly placed spheres with random textures'''
    world = HittableList()

    checker = CheckerTexture(Color(0.2, 0.3, 0.1), Color(0.9, 0.9, 0.9))
    ground_material = Lambertian(checker)
    world.add(Sphere(Point3(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random()
            center = Point3(a + 0.9 * random(), 0.2, b + 0.9 * random())

            if (center - Point3(4, 0.2, 0)).length() > 0.9:

                if choose_mat < 0.8:
                    albedo = Color.random() * Color.random()
                    sphere_material = Lambertian(albedo)
                    center2 = center + Vec3(0, uniform(0, 0.5), 0)
                    world.add(MovingSphere(center, center2, 0.0, 1.0, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    albedo = Color.random(0.5, 1)
                    fuzz = uniform(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))

    material1 = Dielectric(1.5)
    world.add(Sphere(Point3( 0,  1,  0), 1.0, material1))

    material2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4,  1,  0), 1.0, material2))

    material3 = Metal(Color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(Point3( 4,  1,  0), 1.0, material3))

    return world


def two_spheres():
    '''Generate a scene with two checkered spheres'''
    world = HittableList()

    checker = CheckerTexture(Color(0.2, 0.3, 0.1), Color(0.9, 0.9, 0.9))

    world.add(Sphere(Point3(0, -10, 0), 10, Lambertian(checker)))
    world.add(Sphere(Point3(0,  10, 0), 10, Lambertian(checker)))

    return world


def two_perlin_spheres():
    '''Generate a scene with two spheres using a custom Perlin noise texture'''
    world = HittableList()

    pertext = NoiseTexture(4)
    world.add(Sphere(Point3(0, -1000, 0), 1000, Lambertian(pertext)))
    world.add(Sphere(Point3(0,     2, 0),    2, Lambertian(pertext)))

    return world


def earth():
    '''Generate a scene with a sphere using an image texture of Earth'''
    world = HittableList()

    earth_texture = ImageTexture('earthmap.jpg')
    earth_surface = Lambertian(earth_texture)
    world.add(Sphere(Point3(0, 0, 0), 2, earth_surface))

    return world


def simple_light():
    '''Generate a scene with two spheres and a diffusive light'''
    world = HittableList()

    pertext = NoiseTexture(4)
    world.add(Sphere(Point3(0, -1000, 0), 1000, Lambertian(pertext)))
    world.add(Sphere(Point3(0,     2, 0),    2, Lambertian(pertext)))

    difflight = DiffuseLight(Color(4, 4, 4))
    world.add(xyRect(3, 5, 1, 3, -2, difflight))

    return world

def cornell_box():
    '''Generate a scene with a Cornell box, using rectangles and boxes'''
    world = HittableList()

    red   = Lambertian(Color(0.65, 0.05, 0.05))
    white = Lambertian(Color(0.73, 0.73, 0.73))
    green = Lambertian(Color(0.12, 0.45, 0.15))
    light = DiffuseLight(Color(15, 15, 15))
    aluminum = Metal(Color(0.8, 0.85, 0.88), 0.0)
    glass = Dielectric(1.5)

    box1 = Box(Point3(0, 0,  0), Point3(165, 330, 165), aluminum)
    box1 = RotateY(box1, 15)
    box1 = Translate(box1, Vec3(265, 0, 295))

    box2 = Box(Point3(0, 0, 0), Point3(165, 165, 165), white)
    box2 = RotateY(box2, -18)
    box2 = Translate(box2, Vec3(130, 0, 65))

    world.add(yzRect(0, 555, 0, 555, 555, green))
    world.add(yzRect(0, 555, 0, 555,   0, red  ))
    world.add(xzRect(0, 555, 0, 555, 555, white))
    world.add(xzRect(0, 555, 0, 555,   0, white))
    world.add(xyRect(0, 555, 0, 555, 555, white))

    world.add(box1)
    world.add(box2)

    world.add(FlipFace(xzRect(213, 343, 227, 332, 554, light)))

    return world

def cornell_smoke():
    '''Generate a scene with a Cornell box where the boxes are filled with smoke'''
    world = HittableList()

    red   = Lambertian(Color(0.65, 0.05, 0.05))
    white = Lambertian(Color(0.73, 0.73, 0.73))
    green = Lambertian(Color(0.12, 0.45, 0.15))
    light = DiffuseLight(Color(7, 7, 7))

    box1 = Box(Point3(0, 0,  0), Point3(165, 330, 165), white)
    box1 = RotateY(box1, 15)
    box1 = Translate(box1, Vec3(265, 0, 295))

    box2 = Box(Point3(0, 0, 0), Point3(165, 165, 165), white)
    box2 = RotateY(box2, -18)
    box2 = Translate(box2, Vec3(130, 0, 65))

    world.add(yzRect(0, 555, 0, 555, 555, green))
    world.add(yzRect(0, 555, 0, 555,   0, red  ))
    world.add(xzRect(0, 555, 0, 555, 555, white))
    world.add(xzRect(0, 555, 0, 555,   0, white))
    world.add(xyRect(0, 555, 0, 555, 555, white))

    world.add(ConstantMedium(box1, 0.01, Color(0, 0, 0)))
    world.add(ConstantMedium(box2, 0.01, Color(1, 1, 1)))

    world.add(xzRect(113, 443, 127, 432, 554, light))

    return world

def final_scene():
    '''Generate a scene with all currently available textures'''
    boxes1 = HittableList()
    ground = Lambertian(Color(0.48, 0.83, 0.53))

    boxes_per_side = 20
    for i in range(boxes_per_side):
        for j in range(boxes_per_side):
            w = 100.0
            x0 = -1000.0 + i * w
            z0 = -1000.0 + j * w
            y0 = 0.0
            x1 = x0 + w
            y1 = uniform(1, 101)
            z1 = z0 + w

            boxes1.add(Box(Point3(x0, y0, z0), Point3(x1, y1, z1), ground))

    world = HittableList()

    world.add(BvhNode(boxes1, 0, 1))

    light = DiffuseLight(Color(7, 7, 7))
    world.add(xzRect(123, 423, 147, 412, 554, light))

    center1 = Point3(400, 400, 200)
    center2 = center1 + Vec3(50, 0, 0)
    moving_sphere_material = Lambertian(Color(0.7, 0.3, 0.1))
    world.add(MovingSphere(center1, center2, 0, 1, 50, moving_sphere_material))

    world.add(Sphere(Point3(260, 150,  45), 50, Dielectric(1.5)))
    world.add(Sphere(Point3(  0, 150, 145), 50, Metal(Color(0.8, 0.8, 0.9), 10.0)))

    boundary = Sphere(Point3(360, 150, 145), 70, Dielectric(1.5))
    world.add(boundary)
    world.add(ConstantMedium(boundary, 0.2, Color(0.2, 0.4, 0.9)))
    boundary = Sphere(Point3(0, 0, 0), 5000, Dielectric(1.5))
    world.add(ConstantMedium(boundary, .0001, Color(1, 1, 1)))

    emat = Lambertian(ImageTexture('earthmap.jpg'))
    world.add(Sphere(Point3(400, 200, 400), 100, emat))
    pertext = NoiseTexture(0.1)
    world.add(Sphere(Point3(220, 280, 300), 80, Lambertian(pertext)))

    boxes2 = HittableList()
    white = Lambertian(Color(.73, .73, .73))
    ns = 1000
    for j in range(ns):
        boxes2.add(Sphere(Point3.random(0, 165), 10, white))
    
    world.add(Translate(RotateY(BvhNode(boxes2, 0, 1), 15), Vec3(-100, 270, 395)))

    return world