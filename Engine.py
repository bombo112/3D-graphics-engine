import math
import pygame
import time

screen_height = 1080
screen_width =  (screen_height * (16/9))

screensize = (screen_width, screen_height)
window = pygame.display.set_mode(screensize)
loop = range(0, 3, 1)   #used to loop through x, y and z or the 3 vertexes in a triangle.

#projection data
Zfar = 1000
Znear = 0.1
fov = 90
aspect_ratio = screen_height/screen_width
fov_rad = 1/math.tan(math.radians(fov *0.5))

#camera and sun data
camera = [[0, 0, 0], [0]]
asset_liste = []
sun_direction = [1,3, 0]

#sun and shadow color in rgb
sun_color = [255, 255, 150]
shadow_color = [10, 10, 20]
shade_fallof = 1


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
        output[i][0] = triangle[i][0] * screen_width/2 + screen_width/2
        output[i][1] = triangle[i][1] * screen_height/2 + screen_height/2
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

def triangle_shade(triangle, normalvector, light, max_color, min_color, object_color = [255, 255, 255]):
    color = [0, 0, 0]
    vector_length = math.sqrt(triangle[0][0]**2 + triangle[0][1]**2 + triangle[0][2]**2)
    light_length = math.sqrt(light[0]**2 + light[1]**2 + light[2]**2)
    raw_lightfaktor =(normalvector[0] *(triangle[0][0]/vector_length - light[0]/light_length) + 
                  normalvector[1] *(triangle[0][1]/vector_length - light[1]/light_length) + 
                  normalvector[2] *(triangle[0][2]/vector_length - light[2]/light_length))
    linear_lightfaktor = (raw_lightfaktor + 2) /4

    lightfactor = (10**(linear_lightfaktor-1))*linear_lightfaktor**shade_fallof

    for i in loop:
        color[i] = translate_value(lightfactor, 0, 1, min_color[i], max_color[i])
        color[i] *= (object_color[i]/255)
        if color[i] > 255:
            color[i] = 255
    
    return (color[0], color[1], color[2])


def translate_value(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def load_model(filename, location = [0, 0, 0], rotation = [0, 0, 0], scale = [0, 0, 0], color = [255, 255, 255], id = 0):

    new_object = []
    model_vertex_list = []
    triangle = []
    triangle_list = []

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

                triangle = [model_vertex_list[vektor1[0]-1], model_vertex_list[vektor2[0]-1], model_vertex_list[vektor3[0]-1]]
                
                triangle_list.append(triangle)

    new_object.append(triangle_list)
    new_object.append(location)
    new_object.append(rotation)
    new_object.append(scale)
    new_object.append(color)
    new_object.append(id)
    
    asset_liste.append(new_object)  #legger til objeketet til listen med objekter
    print(f"Finished loading model: {filename}")
    return len(asset_liste)     #returnerer objektets liste adresse


def modify_object(id, location = [0, 0, 0], rotation = [0, 0, 0], scale = [1, 1, 1], color = [255, 255, 255]):
    object_index = find_index(asset_liste, id)
    if object_index == "object does not exist":
        return "object does not exist"
    
    asset_liste[object_index][1] = location
    asset_liste[object_index][2] = rotation
    asset_liste[object_index][3] = scale
    asset_liste[object_index][4] = color
    return "success"


def find_index(liste, key):
    for i in range(len(liste)):
        if liste[i][5] == key:
            return i
    return("object does not exist")


def remove_object(id):
    object_index = find_index(id)
    asset_liste.pop(object_index)

def scale_triangle(trigon, x=1, y=1, z=1):
    output = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in loop:
        output[i][0] = x * trigon[i][0]
        output[i][1] = y * trigon[i][1]
        output[i][2] = z * trigon[i][2]
    return output


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


def draw():
    window.fill((0, 0, 0))
    
    startime = time.time()
    render_qew = []

    for objekt in asset_liste:
        for triangles in objekt[0]:

            scaled_triangle = scale_triangle(triangles, objekt[3][0], objekt[3][1], objekt[3][2])                               #scale triangle

            rotated_triangle = rotate_multiaxis(scaled_triangle, angle_x_axis=objekt[2][0], angle_y_axis = objekt[2][1], angle_z_axis=objekt[2][2])     #rotate the cube

            offseted_triangles2 = translate_triangle(rotated_triangle, x=objekt[1][0], y=objekt[1][1], z=objekt[1][2])                   #move cube to location in space

            normal = normal_finder_triangle(offseted_triangles2)

            if (normal[0] *(offseted_triangles2[0][0] - camera[0][0]) + 
                normal[1] *(offseted_triangles2[0][1] - camera[0][1]) + 
                normal[2] *(offseted_triangles2[0][2] - camera[0][2])) > 0:

                projected_triangles = project_triangle2(offseted_triangles2)                    #project to screenspace

                screen_normalized_triangles = screen_normalize(projected_triangles)             #adapt to screen dimentions

                complete_triangle = []
                complete_triangle.append(screen_normalized_triangles)
                complete_triangle.append(triangle_shade(offseted_triangles2, normal, sun_direction, sun_color, shadow_color, objekt[4]))

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
    pygame.display.update()