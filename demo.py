import Engine as fx
import math
import pygame

fx.asset_liste.append([fx.cube, [0, 2, 3], [0, 0, 0], [0, 0, 0], [255, 255, 255], 0])       #testcube, included in code
fx.asset_liste.append([fx.cube, [0, 2, 3], [0, 0, 0], [0, 0, 0], [255, 255, 255], 1])       #testcube
fx.asset_liste.append([fx.cube, [0, 2, 3], [0, 0, 0], [0, 0, 0], [255, 255, 255], 2])       #testcube
fx.asset_liste.append([fx.cube, [0, 2, 3], [0, 0, 0], [0, 0, 0], [255, 255, 255], 3])       #testcube
fx.load_model("plane.obj", id=40)                                                           #loaded form obj file


offset = 0
while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    offset += 0.01
    fx.modify_object(0, [math.cos(offset)*3, -3, 5], [math.sin(offset), 0, offset])
    fx.modify_object(1, [math.sin(offset)*3, 0, 5], [math.tan(offset), 2, 0])
    fx.modify_object(2, [3, math.cos(offset)*-3, 5], [math.sin(offset), offset, offset/2])
    fx.modify_object(3, [math.cos(offset/3)*3, -3, 5], [math.sin(offset), 4, 2])
    fx.modify_object(40, [math.cos(offset/3)*200, -3, 300], [-math.pi/4+math.sin(offset), math.pi /2, 0])
    fx.draw()