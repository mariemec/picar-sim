import bpy
from math import *
from mathutils import *

# Variable for currently active object
# myobj = bpy.context.object

ball = bpy.context.scene.objects["Bille"]
socle = bpy.context.scene.objects["Socle"]

# Alternatively, if you know that the object is called 'Cube'
# you can reach it by
# myobj = bpy.data.objects['Cube']

# Clear all previous animation data
ball.animation_data_clear()

# set first and last frame index
total_time = 2*pi # Animation should be 2*pi seconds long
fps = 24 # Frames per second (fps)
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = int(total_time*fps)+1

# loop of frames and insert keyframes every 10th frame
keyframe_freq = 10
nlast = bpy.context.scene.frame_end
for n in range(nlast):
    t = total_time*n/nlast

    # Do computations here...
    new_x = math.cos(t)*5
    new_y = math.sin(t)*5
    new_z = math.sin(5*t)
    
    # Check if n is a multiple of keyframe_freq
    if n%keyframe_freq == 0:
        # Set frame like this
        bpy.context.scene.frame_set(n)

        # Set current location like this
        ball.location.x = ...
        ball.location.y = ...
        ball.location.z = ...

        # Insert new keyframe for "location" like this
        ball.keyframe_insert(data_path="location")

