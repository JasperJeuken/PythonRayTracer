# Custom libraries
from color import Color
from vec3 import Vec3
from point3 import Point3
from hittablelist import HittableList
from sphere import Sphere
from movingsphere import MovingSphere
from hittable import HitRecord
from ray import Ray
from camera import Camera
from material import *
from scene import *
from pdf import *

# 3rd party libraries
from random import random, uniform
import argparse
from multiprocessing import Value, Process, cpu_count
import tempfile
from pathlib import Path
import os
import stat
import time
from math import isnan


def vec_to_col(v):
    '''Convert a Vec3 object to a Color object'''
    return Color(v[0], v[1], v[2])


def de_nan(c):
    '''Remove NaN values from Color (change to 0)'''
    temp = c.copy()
    if isnan(temp[0]):
        temp[0] = 0
    if isnan(temp[1]):
        temp[1] = 0
    if isnan(temp[2]):
        temp[2] = 0
    return temp


def split_range(count, parts):
    '''Split some value count into multiple ranges'''
    d, r = divmod(count, parts)
    return [(i*d + min(i, r), (i+1)*d + min(i+1, r)) for i in range(parts)]


def ray_color(ray, background, world, lights, depth):
    '''Determine the color of a ray based on the objects in a scene (recursive with a max depth)'''
    rec = HitRecord()

    # Don't exceed ray bounce limit
    if depth <= 0:
        return Vec3(0, 0, 0)

    # If the ray hits nothing, return background color
    if not world.hit(ray, 0.001, float('inf'), rec):
        return background

    # Determine if the object emits light or has a specular material
    srec = ScatterRecord()
    emitted = rec.mat.emitted(ray, rec, rec.u, rec.v, rec.p)
    if not rec.mat.scatter(ray, rec, srec):
        return emitted
    if srec.is_specular:
        return srec.attenuation * ray_color(srec.specular_ray, background, world, lights, depth - 1)

    # Use PDFs to determine the next ray and call ray_color() again
    light_ptr = HittablePDF(lights, rec.p)
    p = MixturePDF(light_ptr, srec.pdf_ptr)
    scattered = Ray(rec.p, p.generate(), ray.time)
    pdf_val = p.value(scattered.dir)
    del srec.pdf_ptr

    return emitted + srec.attenuation * rec.mat.scattering_pdf(ray, rec, scattered) * ray_color(scattered, background, world, lights, depth - 1) / pdf_val


def render(scene, hmin, hmax, part_file, rows_done, samples_per_pixel, max_depth, background):
    '''Render horizontal strip of a scene (from hmin to hmax) by shooting multiple rays through each pixel'''
    width  = scene.width
    height = scene.height
    aspect_ratio = width / height
    world = scene.world
    lights = scene.lights

    camera = scene.camera

    with open(part_file, 'w') as part_fileobj:

        for j in range(hmax, hmin, -1):
            for i in range(width):
                pixel_color = Color(0, 0, 0)
                for s in range(samples_per_pixel):
                    u = (i + random()) / (width  - 1)
                    v = (j + random()) / (height - 1)
                    r = camera.get_ray(u, v)
                    pixel_color += de_nan(ray_color(r, background, world, lights, max_depth))
                part_fileobj.write(vec_to_col(pixel_color).write_color(samples_per_pixel))
            part_fileobj.write('\n')

            if rows_done:
                with rows_done.get_lock():
                    rows_done.value += 1
                    print(f'  {float(rows_done.value)/float(height) * 100:3.1f}%', end='\r')
            

def main():
    '''Set up the scene and camera and create multiple processes to render it'''
    # Image
    aspect_ratio = 1.0 # 16.0 / 9.0
    image_width  = 1000
    image_height = int(image_width / aspect_ratio)
    samples_per_pixel = 1500
    max_depth = 25

    # Multi-process calculations
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--processes', action='store', type=int, dest='processes', default=0, help='Number of processes (auto=0)')
    args = parser.parse_args()
    if args.processes == 0:
        process_count = cpu_count()
    else:
        process_count = args.processes
    print(f'Starting {process_count} processes...')
    ranges = split_range(image_height, process_count)

    # Lights
    lights = HittableList()
    #lights.add(Sphere(Point3(190, 90, 190), 90, 0))
    lights.add(xzRect(213, 343, 227, 332, 554, Material()))
    #lights.add(Sphere(Point3(190, 90, 190), 90, Material()))
    #lights.add(xzRect(123, 423, 147, 412, 554, Material()))

    # World
    #world = final_scene()
    #world = cornell_smoke()
    world = cornell_box()
    #world = simple_light()
    #world = earth()
    #world = two_perlin_spheres()
    #world = two_spheres()
    #world = random_scene()
    
    # Camera
    lookfrom      = Point3(278, 278, -800)
    lookat        = Point3(278, 278,    0)
    vup           = Point3(  0,   1,    0)
    dist_to_focus = 10.0
    aperture      = 0.0
    vfov          = 40
    background    = Color(0, 0, 0) # Color(0.70, 0.80, 1.00)
    camera = Camera(lookfrom, lookat, vup, vfov, aspect_ratio, aperture, dist_to_focus, 0.0, 1.0)

    # Scene
    scene = Scene(camera, world, lights, image_width, image_height)

    # Render scene
    with open('filename.ppm', 'w') as img_fileobj:

        temp_dir = Path(tempfile.mkdtemp())
        temp_file_tmpl = 'part-{}.temp'
        processes = []

        try:
            rows_done = Value('i', 0)
            print(f'  {float(rows_done.value)/float(image_height) * 100:3.1f}%', end='\r')
            for hmin, hmax in ranges:
                part_file = temp_dir / temp_file_tmpl.format(hmin)
                processes.append(Process(target=render, args=(scene, hmin, hmax, part_file, rows_done, samples_per_pixel, max_depth, background)))

            for process in processes:
                process.start()
            for process in processes:
                process.join()
            
            img_fileobj.write(f'P3 {image_width} {image_height}\n255\n')
            for hmin, _ in reversed(ranges):
                part_file = temp_dir / temp_file_tmpl.format(hmin)
                img_fileobj.write(open(part_file, 'r').read())

        finally:
            os.chmod(temp_dir, stat.S_IWRITE)
            os.remove(temp_dir)


if __name__ == '__main__':
    main()