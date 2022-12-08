# 3D-graphics-engine

This is a pure python 3d graphics engine that can render 3d obj models in space with shading.

Creator: Jens Petersen

Licensing: Use as you like, open source.

Prerequisites librarys required to run:

  - pygame    to output lines and pixels to screen and recieve keyboard input.
  - numpy     for faster math to speed up rendering.

API:
  
  To load a model use this function, all but filename and id is optional and can be set later. RGB values in collor can not exceed 255.
  Id is used to modify the model later during rendering.
  
    - engine.load_model("filename.obj", location=[x, y, z], rotation=[angle_x, angle_y, angle_z], scale=[scale_x, scale_y, scale_z], color=[rrr, ggg, bbb], id)
    
  A model can be alterred before drawing to new values. Keep in mind that these values can not be left blank as they default to zero so that after modifying the new value, the model will move from the previous value to zero. 
    
    - engine.modify(id, location, rotation, scale, color)
    
  To output an image to screen / update the screen, use this command:
    
    - engine.draw()
  
    

Todo list:
  - shadows
  - camera control
  - texturing of triangles
  - sub model cooridonate inheritance (flaps on an aircraft defined relative to the wing it is attatcehed to).
  - define api for use as a library.
  
