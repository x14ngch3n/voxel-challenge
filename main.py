from scene import Scene
import taichi as ti
from taichi.math import vec3

scene = Scene(exposure=10)
scene.set_floor(-0.05, (1.0, 1.0, 1.0))
scene.set_background_color((1.0, 0, 0))


@ti.func
def sphere(pos, r, mat, color):
    for i, j, k in ti.ndrange((-64, 64), (-64, 64), (-64, 64)):
        if (i - pos[0])**2 + (j - pos[1])**2 + (k - pos[2])**2 < r * r:
            scene.set_voxel(vec3(i, j, k), mat, (1, 1, 1))


@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    pos = vec3(0, 0, 0)
    color = vec3(213. / 255, 255. / 255, 13. / 255)
    sphere(pos, 15, 1, color)


initialize_voxels()

scene.finish()
