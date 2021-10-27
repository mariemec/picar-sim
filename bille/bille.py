import bpy
import math
import numpy as np

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
total_time = 2*math.pi # Animation should be 2*pi seconds long
fps = 24 # Frames per second (fps)
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = int(total_time*fps)+1

# loop of frames and insert keyframes every 10th frame
keyframe_freq = 10
nlast = bpy.context.scene.frame_end

r = 1.4  # radius of the pendulum
m = 0.04  # mass of ball
g = 9.81
a = 0.1465  # rad, amplitude initiale
lamda = 0.02  # Friction coeff
p = lamda
k = math.sqrt(m * g / r)
h = math.sqrt(k ** 2 / m - p ** 2 / (4 * m ** 2))

xs = [-0.2, 0, 0.2]
ys = [0, -0.015, 0]
coeffs_parabole = np.polyfit(xs, ys, 2)


for n in range(nlast):
    t = total_time*n/nlast

    # Do computations here...
    theta = a * math.e ** (-lamda * t / (2 * m))*(math.cos(h * t) + lamda / (2 * m * h) * math.sin(h * t))
    new_x = r * math.sin(theta)
    new_y = 0
    new_z = coeffs_parabole[0] * new_x ** 2 +coeffs_parabole[1]*new_x + coeffs_parabole[2] + (0.02) # polyfit de la parabole +offset radius de la bille
    print(new_z)
    
    # Check if n is a multiple of keyframe_freq
    if n%keyframe_freq == 0:
        # Set frame like this
        bpy.context.scene.frame_set(n)

        # Set current location like this
        ball.location.x = new_x
        ball.location.y = new_y
        ball.location.z = new_z

        # Insert new keyframe for "location" like this
        ball.keyframe_insert(data_path="location")

