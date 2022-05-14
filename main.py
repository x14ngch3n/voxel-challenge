from scene import Scene
import taichi as ti
from taichi.math import vec3, ivec3

scene = Scene(exposure=1)
scene.set_floor(-1, (0.8, 0.8, 0.8))
scene.set_directional_light((0, 1, 0), 0.2, (1, 1, 1))
scene.set_background_color((0.8, 0.8, 0.8))


@ti.func
def sphere(pos, r, mat, color):
    for i, j, k in ti.ndrange((-64, 64), (-64, 64), (-64, 64)):
        x = ivec3(i - pos[0], j - pos[1], k - pos[2])
        if x.dot(x) < r * r:
            scene.set_voxel(vec3(i, j, k), mat, color)


@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    pos = vec3(0, 0, 0)
    color = vec3(213. / 255, 255. / 255, 13. / 255)
    sphere(pos, 10, 1, color)


initialize_voxels()

scene.finish()
