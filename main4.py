import math
import pygame
import time


SCREEN_HEIGHT = 1080
SCREEN_WIDTH =  (SCREEN_HEIGHT * (16/9))

SCREENSIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
window = pygame.display.set_mode(SCREENSIZE)
clock = pygame.time.Clock()

loop = range(0, 3, 1)
offset = 2


#projection data
Zfar = 1000
Znear = 0.1
fov = 90
aspect_ratio = SCREEN_HEIGHT/SCREEN_WIDTH
fov_rad = 1/math.tan(math.radians(fov *0.5))


camera = [[0, 0, 0], [0]]
asset_liste = []
sun_direction = [1,3, 0]

sun_color = [255, 255, 150]
shadow_color = [10, 10, 20]


def project_triangle(triangle):
    output = [[0, 0],[0, 0],[0, 0]]
    for i in loop:
        output[i][0] = triangle[i][0] / triangle[i][2]
        output[i][1] = triangle[i][1] / triangle[i][2]
    return output


def project_triangle2(triangle):
    output = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
    for i in loop:
        output[i][0] = aspect_ratio * fov_rad * triangle[i][0]
        output[i][1] = fov_rad * -triangle[i][1]
        output[i][2] = triangle[i][2] * (Zfar/(Zfar-Znear))-((Zfar*Znear)/(Zfar-Znear))
        if triangle[i][2] != 0:
            output[i][0] /= triangle[i][2]
            output[i][1] /= triangle[i][2]
    return(output)


def translate_triangle(triangle, x=0, y=0, z=0):
    output = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in loop:
        output[i][0] = triangle[i][0] + x
        output[i][1] = triangle[i][1] + y
        output[i][2] = triangle[i][2] + z
    return output


def screen_normalize(triangle = [[0, 0], [0, 0], [0, 0]]):
    output = [[0, 0], [0, 0], [0, 0]]
    for i in loop:
        output[i][0] = triangle[i][0] * SCREEN_WIDTH/2 + SCREEN_WIDTH/2
        output[i][1] = triangle[i][1] * SCREEN_HEIGHT/2 + SCREEN_HEIGHT/2
    return output


def draw_triangle_screen(triangle=[[0, 0], [0, 0], [0, 0]]):
    color_white = (255, 255, 255)
    pygame.draw.line(window, color_white, (triangle[0]), (triangle[1]))
    pygame.draw.line(window, color_white, (triangle[1]), (triangle[2]))
    pygame.draw.line(window, color_white, (triangle[0]), (triangle[2]))


def rotate_x(triangle, angle):
    output = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in loop:
        output[i][1] = triangle[i][1] * math.cos(angle)   -   triangle[i][2] * math.sin(angle)
        output[i][2] = triangle[i][1] * math.sin(angle)   +   triangle[i][2] * math.cos(angle)
        output[i][0] = triangle[i][0]
    return output


def rotate_y(triangle, angle):
    output = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in loop:
        output[i][0] = triangle[i][2] * math.cos(angle)   +   triangle[i][0] * math.sin(angle)
        output[i][2] = triangle[i][2] * -math.sin(angle)   +   triangle[i][0] * math.cos(angle)
        output[i][1] = triangle[i][1]
    return output


def rotate_z(triangle, angle):
    output = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in loop:
        output[i][0] = triangle[i][0] * math.cos(angle)   -   triangle[i][1] * math.sin(angle)
        output[i][1] = triangle[i][0] * math.sin(angle)   +   triangle[i][1] * math.cos(angle)
        output[i][2] = triangle[i][2]
    return output


def rotate_multiaxis(triangle,
                     angle_x_axis = 0,
                     angle_y_axis = 0,
                     angle_z_axis = 0):
    return rotate_z(rotate_y(rotate_x(triangle, angle_x_axis), angle_y_axis), angle_z_axis)


def array_sub(array1, array2):
    output = [0, 0, 0]
    for i in loop:
        output[i] = array1[i] - array2[i]
    return output


def normal_finder_triangle(triangle):
    #gets the line segments of the triangle
    line_a = array_sub(triangle[1], triangle[0])
    line_b = array_sub(triangle[2], triangle[0])

    normal = [0, 0, 0]

    #calculates the crossproduct from each line segment in the triangle
    normal[0] = line_a[1] * line_b[2] - line_a[2] * line_b[1]   #x
    normal[1] = line_a[2] * line_b[0] - line_a[0] * line_b[2]   #y
    normal[2] = line_a[0] * line_b[1] - line_a[1] * line_b[0]   #z

    normal_length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
    if normal_length == 0:
        normal_length += 0.000000000001
    for i in loop:
        normal[i] /= normal_length

    return normal


def normal_finder_vector(vector1, vector2):

    normal = [0, 0, 0]
    #calculates the crossproduct from each line segment in the triangle
    normal[0] = vector1[1] * vector2[2] - vector1[2] * vector2[1]   #x
    normal[1] = vector1[2] * vector2[0] - vector1[0] * vector2[2]   #y
    normal[2] = vector1[0] * vector2[1] - vector1[1] * vector2[0]   #z

    normal_length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
    if normal_length == 0:
        normal_length += 0.000000000001
    for i in loop:
        normal[i] /= normal_length

    return normal

def triangle_shade(triangle, normalvector, light, max_color, min_color):
    color = [0, 0, 0]
    vector_length = math.sqrt(triangle[0][0]**2 + triangle[0][1]**2 + triangle[0][2]**2)
    light_length = math.sqrt(light[0]**2 + light[1]**2 + light[2]**2)
    lightfaktor =(normalvector[0] *(triangle[0][0]/vector_length - light[0]/light_length) + 
                  normalvector[1] *(triangle[0][1]/vector_length - light[1]/light_length) + 
                  normalvector[2] *(triangle[0][2]/vector_length - light[2]/light_length))
    lightfaktor += 2
    #print(lightfaktor)
    if lightfaktor < 2:
        lightfaktor = lightfaktor-0.5

    if lightfaktor < 0:
        lightfaktor = 0

    for i in loop:
        color[i] = translate_value(lightfaktor, 0, 4, min_color[i], max_color[i])

    return (color[0], color[1], color[2])


def translate_value(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def load_model(filename):
    new_object = []                 #triangles listed
    model_vertex_list = [[0, 0, 0]]
    triangle = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    with open(filename, "r") as fil:
        lines = fil.readlines()
        for linje in lines:
            linje = linje.rstrip("\n")
            linje_elementer = linje.split(" ")

            if linje_elementer[0] == "v":
                model_vertex_list.append([float(linje_elementer[1]), float(linje_elementer[2]), float(linje_elementer[3])])

        for linje in lines:
            linje = linje.rstrip("\n")
            linje_elementer = linje.split(" ")
        
            if linje_elementer[0] == "f":
                vektor1 = linje_elementer[1].split("/")
                vektor2 = linje_elementer[2].split("/")
                vektor3 = linje_elementer[3].split("/")

                vektor1[0] = int(vektor1[0])
                vektor2[0] = int(vektor2[0])
                vektor3[0] = int(vektor3[0])

                triangle = [model_vertex_list[vektor1[0]], model_vertex_list[vektor2[0]], model_vertex_list[vektor3[0]]]
            new_object.append(triangle)
    asset_liste.append(new_object)  #legger til objeketet til listen med objekter
    print(f"Finished loading model: {filename}")
    return len(asset_liste)     #returnerer objektets liste adresse


cube = [

    [[0, 0, 0],[0, 1, 0],[1, 1, 0]],
    [[0, 0, 0],[1, 1, 0],[1, 0, 0]],

    [[1, 0, 0],[1, 1, 0],[1, 1, 1]],
    [[1, 0, 0],[1, 1, 1],[1, 0, 1]],

    [[1, 0, 1],[1, 1, 1],[0, 1, 1]],
    [[1, 0, 1],[0, 1, 1],[0, 0, 1]],

    [[0, 0, 1],[0, 1, 1],[0, 1, 0]],
    [[0, 0, 1],[0, 1, 0],[0, 0, 0]],

    [[0, 1, 0],[0, 1, 1],[1, 1, 1]],
    [[0, 1, 0],[1, 1, 1],[1, 1, 0]],

    [[1, 0, 1],[0, 0, 1],[0, 0, 0]],
    [[1, 0, 1],[0, 0, 0],[1, 0, 0]]
]


load_model("teapot.obj")
#asset_liste.append(cube)
#load_model("nymph1.obj")
#load_model("Soap_holder.obj")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    clock.tick(50)
    pygame.display.update()
    window.fill((0, 0, 0))
    
    startime = time.time()
    render_qew = []

    
    offset += 0.01
    for objekt in asset_liste:
        for triangles in objekt:
    
            #offseted_triangles1 = translate_triangle(triangles, x=-0.5, y=-0.5, z=-0.5)         #center the cube due to model having origin in corner

            rotated_triangle = rotate_multiaxis(triangles, angle_x_axis=-3.14/2, angle_y_axis = offset*10+3.14/2, angle_z_axis=0)     #rotate the cube

            offseted_triangles2 = translate_triangle(rotated_triangle, z = 10, y=-5)                   #move cube to location in space

            normal = normal_finder_triangle(offseted_triangles2)

            if (normal[0] *(offseted_triangles2[0][0] - camera[0][0]) + 
                normal[1] *(offseted_triangles2[0][1] - camera[0][1]) + 
                normal[2] *(offseted_triangles2[0][2] - camera[0][2])) > 0:

                projected_triangles = project_triangle2(offseted_triangles2)                    #project to screenspace

                screen_normalized_triangles = screen_normalize(projected_triangles)             #adapt to screen dimentions

                complete_triangle = []
                complete_triangle.append(screen_normalized_triangles)
                complete_triangle.append(triangle_shade(offseted_triangles2, normal, sun_direction, sun_color, shadow_color))

                sum_z = (offseted_triangles2[0][2] + offseted_triangles2[1][2] + offseted_triangles2[2][2])/3
                complete_triangle.append(sum_z)

                render_qew.append(complete_triangle)


                #draw_triangle_screen(screen_normalized_triangles)                               #draw to screen
                #pygame.draw.polygon(window, triangle_shade(offseted_triangles2, normal, sun_direction, sun_color, shadow_color), screen_normalized_triangles)
    
    sorted_render_qew = sorted(render_qew, key= lambda x:x[2], reverse=True)
    for triangle in sorted_render_qew:
        try:
            pygame.draw.polygon(window, triangle[1], triangle[0])
        except:
            print(triangle[1])

    stoptime = time.time()
    print(f"fps: {1/(stoptime-startime+0.0000000000000000000000001)}")
    print(f"frametime: {stoptime-startime}")