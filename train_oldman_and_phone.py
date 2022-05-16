from matplotlib.pyplot import draw
from scene import Scene
import taichi as ti
from taichi.math import vec3

scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(-1, (0.8, 0.8, 0.8))
scene.set_directional_light((-1, 1, 1), 0.2, (0.5, 0.5, 0.5))
scene.set_background_color((0.8, 0.8, 0.8))

skin = vec3(224.0 / 255, 197.0 / 255, 167.0 / 255)
hat = vec3(7.0 / 255, 25.0 / 255, 51.0 / 255)
hair = vec3(158.0 / 255, 175.0 / 255, 179.0 / 255)


@ti.func
def draw_cuboid(center, size, mat, color):
    for i, j, k in ti.ndrange((-size[0], size[0]), (-size[1], size[1]), (-size[2], size[2])):
        scene.set_voxel(vec3(center[0] + i, center[1] + j, center[2] + k), mat, color)


@ti.func
def draw_line(start, dir, len, bold, mat, color):
    for i, j in ti.ndrange(len, bold):
        scene.set_voxel(
            vec3(start[0] + dir[0] * i + j, start[1] + dir[1] * i + j, start[2] + dir[2] * i + j), mat, color
        )
        scene.set_voxel(
            vec3(start[0] + dir[0] * i + j, start[1] + dir[1] * i - j, start[2] + dir[2] * i + j), mat, color
        )
        scene.set_voxel(
            vec3(start[0] + dir[0] * i - j, start[1] + dir[1] * i + j, start[2] + dir[2] * i + j), mat, color
        )
        scene.set_voxel(
            vec3(start[0] + dir[0] * i - j, start[1] + dir[1] * i - j, start[2] + dir[2] * i + j), mat, color
        )


@ti.kernel
def initialize_voxels():
    draw_cuboid(vec3(0, 0, 0), (20, 20, 20), 1, skin)  # 头部
    draw_cuboid(vec3(0, 20, 30), (20, 2, 10), 1, hat)  # 帽檐
    draw_cuboid(vec3(0, 26, 0), (20, 6, 20), 1, hat)  # 冒顶
    draw_cuboid(vec3(0, 26, 21), (2, 1, 1), 1, vec3(1, 1, 1))  # 帽子logo
    draw_cuboid(vec3(20, 15, 0), (2, 5, 20), 1, hair)  # 右侧头发
    draw_cuboid(vec3(-20, 15, 0), (2, 5, 20), 1, hair)  # 左侧头发
    draw_cuboid(vec3(10, 10, 20), (5, 1, 1), 1, vec3(0, 0, 0))  # 右眉毛
    draw_cuboid(vec3(10, 7, 20), (4, 1, 1), 1, vec3(0, 0, 0))  # 右眼
    draw_cuboid(vec3(-10, 10, 20), (5, 1, 1), 1, vec3(0, 0, 0))  # 右眉毛
    draw_cuboid(vec3(-10, 7, 20), (4, 1, 1), 1, vec3(0, 0, 0))  # 右眼
    draw_cuboid(vec3(0, -10, 21), (7, 1, 1), 1, vec3(0, 0, 0))  # 嘴巴

    draw_cuboid(vec3(0, -42, 0), (20, 20, 20), 1, hat)  # 身体
    draw_line(vec3(10, -22, 19), vec3(-1, -2, 0), 25, 2, 1, vec3(0, 0, 0))  # 背带

    draw_cuboid(vec3(0, 0, 50), (8, 15, 1), 1, vec3(0, 0, 0))  # 手机
    draw_cuboid(vec3(0, 7, 50), (2, 5, 1), 1, hair)  # 摄像头


initialize_voxels()

scene.finish()
