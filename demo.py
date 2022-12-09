import Engine as fx
import math
import pygame



fx.asset_liste.append([fx.cube, [0, 2, 3], [0, 0, 0], [1, 1, 1], [255, 255, 255], 0])       #testcube, included in code
fx.asset_liste.append([fx.cube, [0, 2, 3], [0, 0, 0], [0, 0, 0], [255, 255, 255], 1])       #testcube
fx.asset_liste.append([fx.cube, [0, 2, 3], [0, 0, 0], [0, 0, 0], [255, 255, 255], 2])       #testcube
fx.asset_liste.append([fx.cube, [0, 2, 3], [0, 0, 0], [0, 0, 0], [255, 255, 255], 3])       #testcube
fx.load_model("plane.obj", id=40)                                                           #loaded form obj file
#fx.load_model("teapot.obj", id=41)
fx.load_model("Lowpoly_tree_sample.obj", id=50)

fx.sun_color = [400, 320, 240]
fx.shade_fallof = 1
fx.sun_direction = [0, 1, 0]
fx.shadow_color = [0, 0, 0]

offset = 0
while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    pygame.time.Clock().tick(100)

    offset += 0.01
    fx.sun_direction = [math.cos(offset*10), math.sin(offset*10), math.sin(offset*10)]

    fx.modify_object(0, [math.cos(offset)*3, -3, 5], [math.sin(offset), 0, offset], color=[255, 0, 0])
    fx.modify_object(1, [math.sin(offset)*3, 0, 5], [math.tan(offset), 2, 0])
    fx.modify_object(2, [3, math.cos(offset)*-3, 5], [math.sin(offset), offset, offset/2], color=[204, 255, 102])
    fx.modify_object(3, [math.cos(offset/3)*3, -3, 5], [math.sin(offset), 4, 2])
    fx.modify_object(40, [math.cos(offset/3)*200, -3, 300], [-math.pi/4+math.sin(offset), math.pi /2, 0], scale=[0.5, 1, 1])
    fx.modify_object(41, location=[0, -3, 10], rotation=[0, offset*10, 0], scale=[2, 2, 1.5], color=[255, 51, 151])
    fx.modify_object(50, location=[0, -5, 30], color=[102, 255, 51], rotation=[0, -3.14/2, 0])

    fx.draw()