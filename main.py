from scene import Scene
import taichi as ti
from taichi.math import vec3

scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(-1, (0.8, 0.8, 0.8))
scene.set_directional_light((-1, 1, 1), 0.2, (1, 1, 1))
scene.set_background_color((0.8, 0.8, 0.8))

red = vec3(255 / 255, 40. / 255, 40. / 255)
yellow = vec3(239. / 255, 243. / 255, 109. / 255)
black = vec3(0, 0, 0)
brown = vec3(45. / 255, 45. / 255, 2. / 255)
green = vec3(13. / 255, 100. / 255, 13. / 255)


@ti.func
def circle(pos, j, r, mat, color):
    # draw a circle on plane as a slice
    for i, k in ti.ndrange((-64, 64), (-64, 0)):
        if abs(((i - pos[0])**2 + (k - pos[2])**2)**0.5 - r) <= 1:
            scene.set_voxel(vec3(i, j, k), mat, color)


@ti.func
def ellipse(pos, a, b, mat, color):
    for i, j in ti.ndrange((-64, 64), (-64, 64)):
        if (a * (i - pos[0])**2 + b * (j - pos[1])**2)**0.5 - a * b <= 1:
            scene.set_voxel(vec3(i, j, 0), mat, color)


@ti.func
def body(pos, a, mat):
    # draw the apple's half body with a cross-section
    for j, r in ti.ndrange((-64, 64), (0, 64)):
        rho = ((j - pos[1])**2 + r**2)**0.5
        sin = j / rho
        # draw the body
        if abs(rho - a * (1 - sin)) <= 2:
            circle(pos, j, r, mat, red)
        # draw the cross-section
        if rho - a * (1 - sin) < 0:
            scene.set_voxel(vec3(r, j, 0), mat, yellow)
            scene.set_voxel(vec3(-r, j, 0), mat, yellow)

    # draw the apple's core
    ellipse(vec3(5, -24, 0), 4, 1, mat, black)
    ellipse(vec3(-5, -24, 0), 4, 1, mat, black)


@ti.func
def stem(pos, height, dir, mat, color):
    for i in range(height + 1):
        for j in range(pos[1] + 2 * i, pos[1] + 2 * i + 4):
            scene.set_voxel(vec3(dir * i, j, 0), mat, color)


@ti.func
def leaf(pos, mat, size, color):
    for i, j in ti.ndrange((0, size), (0, size)):
        if (i**2 + (j - size)**2)**0.5 - size <= 0 and (
            (i - size)**2 + j**2)**0.5 - size <= 0:
            scene.set_voxel(vec3(pos[0] + i, pos[1] + j, pos[2]), mat, color)


@ti.func
def top(pos, mat):
    root = 10
    stem(pos, root, 1, mat, brown)
    stem(pos, 7, -1, mat, brown)
    leaf((pos[0] + root, pos[1] + 2 * root, pos[2]), mat, 20, green)


@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    pos = vec3(0, 0, 0)
    body(pos, 32, 1)
    top(pos, 1)


initialize_voxels()

scene.finish()
