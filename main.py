from scene import Scene
import taichi as ti
from taichi.math import vec3

scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(-1, (0.8, 0.8, 0.8))
scene.set_directional_light((-1, 1, 1), 0.2, (1, 1, 1))
scene.set_background_color((0.8, 0.8, 0.8))

red = vec3(255 / 255, 40.0 / 255, 40.0 / 255)
yellow = vec3(239.0 / 255, 243.0 / 255, 109.0 / 255)
black = vec3(0, 0, 0)
brown = vec3(45.0 / 255, 45.0 / 255, 2.0 / 255)
green = vec3(13.0 / 255, 100.0 / 255, 13.0 / 255)


@ti.func
def circle(pos, j, r, mat, color, fill):
    # draw a circle on plane as a slice
    for i, k in ti.ndrange((-64, 64), (-64, 0)):
        if fill:
            if ((i - pos[0]) ** 2 + (k - pos[2]) ** 2) ** 0.5 - r <= 1:
                scene.set_voxel(vec3(i, j, k), mat, color)
        else:
            if abs(((i - pos[0]) ** 2 + (k - pos[2]) ** 2) ** 0.5 - r) <= 1:
                scene.set_voxel(vec3(i, j, k), mat, color)


@ti.func
def ellipse(pos, a, b, mat, color):
    for i, j in ti.ndrange((-64, 64), (-64, 64)):
        if ((a * (i - pos[0])) ** 2 + (b * (j - pos[1])) ** 2) ** 0.5 - a * b <= 1:
            scene.set_voxel(vec3(i, j, 0), mat, color)


@ti.func
def body(pos, a, mat):
    # draw the apple's half body with a cross-section
    for j, r in ti.ndrange((-64, 64), (0, 64)):
        rho = ((j - pos[1]) ** 2 + r**2) ** 0.5
        sin = j / rho
        # draw the body
        if abs(rho - a * (1 - sin)) <= 2:
            circle(pos, j, r, mat, red, False)
        # draw the cross-section
        if rho - a * (1 - sin) < 0:
            scene.set_voxel(vec3(r, j, 0), mat, yellow)
            scene.set_voxel(vec3(-r, j, 0), mat, yellow)
            if j < 0:
                circle(pos, j, r, mat, yellow, True)

    # draw the apple's core
    ellipse(vec3(5, -24, 0), 6, 2, mat, black)
    ellipse(vec3(-5, -24, 0), 6, 2, mat, black)


@ti.func
def leaf(pos, dir, mat, size, color1, color2):
    for i in range(size + 1):
        for j in range(pos[1] + 2 * i, pos[1] + 2 * i + 4):
            scene.set_voxel(vec3(dir * i, j, 0), mat, color1)
    for i, j in ti.ndrange((0, 2 * size), (0, 2 * size)):
        if (i**2 + (j - 2 * size) ** 2) ** 0.5 - 2 * size <= 0 and (
            (i - 2 * size) ** 2 + j**2
        ) ** 0.5 - 2 * size <= 0:
            scene.set_voxel(
                vec3(pos[0] + dir * (size + i), pos[1] + 2 * size + j, pos[2]),
                mat,
                color2,
            )


@ti.func
def top(pos, mat, root1, root2):
    leaf(pos, 1, mat, root1, brown, green)
    leaf(pos, -1, mat, root2, brown, green)


@ti.func
def bite(pos, a, b, c):
    # subtract a ellptic sphere
    for i, j, k in ti.ndrange((-64, 64), (-64, 64), (-64, 64)):
        if (
            (b * c * (i - pos[0])) ** 2 + (a * c * (j - pos[1])) ** 2 + (a * b * (k - pos[2])) ** 2
        ) ** 0.5 - a * b * c <= 1:
            scene.set_voxel(vec3(i, j, k), 0, yellow)


@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    pos = vec3(0, 0, 0)
    body(pos, 32, 1)
    top(pos, 1, 10, 7)
    bite(vec3(40, -24, 0), 10, 16, 32)


initialize_voxels()

scene.finish()
