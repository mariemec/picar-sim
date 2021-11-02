# ----------------------- BILLE -----------------------
from position import Position
import numpy as np


class Bille:
    g = 9.81

    def __init__(self, theta=0, x=0, y=0):
        self.mass = 0.005
        self.radius_bille = 0.016
        self.radius_pendule = 0.14
        self.position = Position(x, y)
        self.theta = theta

    def calculate_next_theta(self, t, a, theta_0, omega_0, u):
        damping = np.exp(-u * t)
        b = self.g / self.radius_pendule
        c = -a / self.radius_pendule
        b_sqrt = np.sqrt(b)

        A = theta_0 - c / b
        B = omega_0 / b_sqrt

        position = A * np.cos(b_sqrt * t) + B * np.sin(b_sqrt * t) + c / b

        return position * damping  # Position = Theta * e^(-damp*t)

    def calculate_next_omega(self, t, a, theta_0, omega_0, u):
        damping = np.exp(-u * t)
        b = self.g / self.radius_pendule
        c = -a / self.radius_pendule
        b_sqrt = np.sqrt(b)

        A = theta_0 - c / b
        B = omega_0 / b_sqrt

        position = A * np.cos(b_sqrt * t) + B * np.sin(b_sqrt * t) + c / b
        angular_velocity = -A * np.sin(b_sqrt * t) * b_sqrt + B * np.cos(b_sqrt * t) * b_sqrt

        return angular_velocity * damping + -u * damping * position  # Velocity = d/dt(Position)


    # CODE BELOW ONLY WORKS IN BLENDER - UNCOMMENT PLZ
    # def blender_init(self):
    #     bpy.ops.mesh.primitive_uv_sphere_add(radius=0.016, enter_editmode=False, align='WORLD', location=(0, 0, 0),
    #                                          scale=(1, 1, 1))
    #     bpy.context.active_object.name = 'bille'
    #     self._bille = myobj = bpy.data.objects['bille']
    #
    # def blender_update(self, x, y):
    #     self.position.x = x
    #     self.position.y = y
    #     self._bille.location.x = x
    #     self._bille.location.y = y

# Example
# my_bille = Bille()
# my_bille.blender_init()
# my_bille._bille.animation_data_clear()
# total_time = 2*math.pi # Animation should be 2*pi seconds long
# fps = 24 # Frames per second (fps)
# bpy.context.scene.frame_start = 0
# bpy.context.scene.frame_end = int(total_time*fps)+1
# keyframe_freq = 10
# nlast = bpy.context.scene.frame_end

# for n in range(nlast):
#     t = total_time*n/nlast
#
#     if n%keyframe_freq == 0:
#         bpy.context.scene.frame_set(n)
#         my_bille.blender_update(0.1*math.sin(t), 0)
