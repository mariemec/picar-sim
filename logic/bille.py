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
    #     bpy.ops.mesh.primitive_cube_add(size=0.05, enter_editmode=False, align='WORLD', location=(0, 0, -0.005),
    #                                     scale=(1, 1, 0.2))
    #     bpy.context.active_object.name = 'socle'
    #     self._socle = bpy.data.objects['socle']
    #
    #     bpy.ops.mesh.primitive_uv_sphere_add(radius=self.radius_bille, enter_editmode=False, align='WORLD', location=(
    #     self._socle.location.x, self.position.y,
    #     self._socle.location.z + self._socle.dimensions[2] - 0.0015 + self.radius_bille), scale=(1, 1, 1))
    #     bpy.context.active_object.name = 'bille'
    #     self._bille = bpy.data.objects['bille']
    #
    #     self._bille.parent = self._socle

    # def blender_update(self, x, y):
    #     self.position.x = x
    #     self.position.y = y
    #     self._bille.location.x = x
    #     self._bille.location.y = y


# Example
# my_bille = Bille()
# my_bille.blender_init()
# my_bille._bille.animation_data_clear()
# my_bille._socle.animation_data_clear()
#
# total_time = 2  # Animation should be 2*pi seconds long
# fps = 24  # Frames per second (fps)
# bpy.context.scene.frame_start = 0
# bpy.context.scene.frame_end = int(total_time * fps) + 1
# keyframe_freq = 5
# nlast = bpy.context.scene.frame_end
#
# a = 1.37
# dt = 1 / fps
# theta_init = 0
# omega_init = 0
# t_relatif = 0
# s_t = np.array([])
# w_t = np.array([])
# x_0 = 0
# v_0 = 0
#
# for n in range(nlast):
#     t = total_time * n / nlast
#
#     if n % keyframe_freq == 0:
#         bpy.context.scene.frame_set(n)
#         if n == 10:
#             theta_init = s_t[-1]
#             omega_init = w_t[-1]
#             t_relatif = 1 / fps
#             x_0 = x_0 + my_bille.position.x
#             v_0 = v_0 + a * t
#             a = 0
#         if n == 40:
#             theta_init = s_t[-1]
#             omega_init = w_t[-1]
#             t_relatif = 1 / fps
#             x_0 = x_0 + my_bille.position.x
#             v_0 = v_0 + a * t
#             a = -1.37
#
#         theta = my_bille.calculate_next_theta(t_relatif, a, theta_init, omega_init, 1)
#         omega = my_bille.calculate_next_omega(t_relatif, a, theta_init, omega_init, 1)
#         s_t = np.append(s_t, theta)
#         w_t = np.append(w_t, omega)
#
#         next_x, next_z = my_bille.calculate_next_pos(theta)
#         my_bille.blender_update(next_x, next_z)
#         my_bille._bille.keyframe_insert(data_path="location")
#         my_bille._socle.location.x = 1 / 2 * a * t ** 2 + v_0 * t + x_0
#         my_bille._socle.keyframe_insert(data_path="location")
#         t_relatif += 1 / fps