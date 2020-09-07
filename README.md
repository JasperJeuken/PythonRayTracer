# Pure Python Ray Tracer

<img src="https://i.imgur.com/XcFBDMq.png" alt="1000x1000 Cornell box render" width="50%" height="50%">

_1000 x 1000 [Cornell box](https://en.wikipedia.org/wiki/Cornell_box) rendered with 1500 samples per pixel_


## Features
* **Monte Carlo Ray Tracing**
* **Colorable volumetric light sources**
* **Multiple materials:**
  * Diffuse    (Lambertian)
  * Metallic   (with color and fuzziness)
  * Dielectric (glass) with refractive index
* **Multiple textures:**
  * Single color
  * Checkered
  * Perlin noise (marble-like)
  * Image (from file)
* **Multi-process rendering for multi-core CPUs**
* **Bounding volume hierarchy for faster rendering**
* **Customizable camera:**
  * Change position and target
  * Depth of field using aperture and focus distance
  * Field of view and aspect ratio
  
## Installation
Uses only helper functions from standard Python libraries, except for loading images to the image texture with the [Python Imaging Library](https://pypi.org/project/Pillow/).

## Usage
Run from command prompt:
```cmd
C:path_to_folder> python main.py
```

Optional argument for specifying the number of processes to spread the render over:
```cmd
C:path_to_folder> python main.py -p 4
```

Can also be compiled with [PyPy](https://www.pypy.org/) using Just-in-Time compiling (JIT):
```cmd
C:path_to_folder> pypy3 main.py
```
In `main.py` the camera and scene settings can be adjusted. `scene.py` contains several pre-made scenes, but more can easily be added by copying one of these functions.
  
## Attribution
Created using ["Ray Tracing in One Weekend Series"](https://raytracing.github.io/) (v3.2.0) for C++ by Peter Shirley (Steve Hollasch, Trevor David Black).<br />
With snippets of code from [Arun Ravindran ArunRocks](https://www.youtube.com/channel/UCj7bqdW_FLpzUIzlSbXLp_A) series _Puray_.

## Gallery
