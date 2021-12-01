# ----------------------- BILLE -----------------------
from position import Position
import numpy as np


class Bille:

    g = 9.81

    def __init__(self, theta=0, x=0, y=0, z=0):
        self.mass = 0.005
        self.radius_bille = 0.008
        self.radius_pendule = 0.14
        self.position = Position(x, y, z)
        self.theta = theta
        self._bille = None
        self._socle = None

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

    def calculate_next_pos(self, theta_x, theta_y):
        return self.radius_pendule * np.sin(theta_x), self.radius_pendule * np.sin(theta_y)

    def blender_init(self):
        try:
            self._socle = bpy.data.objects['socle']
        except:
            bpy.ops.mesh.primitive_cube_add(size=0.05, enter_editmode=False, align='WORLD', location=(0, 0, -0.005),
                                            scale=(1, 1, 0.2))
            bpy.context.active_object.name = 'socle'
            self._socle = bpy.data.objects['socle']

        try:
            self._bille = bpy.data.objects['bille']
        except:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=self.radius_bille, enter_editmode=False, align='WORLD',
                                                 location=(self._socle.location.x, self.position.y,
                                                           self._socle.location.z + self._socle.dimensions[
                                                               2] - 0.0015 + self.radius_bille), scale=(1, 1, 1))
            bpy.context.active_object.name = 'bille'
            self._bille = bpy.data.objects['bille']

        self._bille.parent = self._socle

    def blender_update(self, x, y):
        self.position.x = x
        self.position.y = y
        self._bille.location.x = x
        self._bille.location.y = y
        self._bille.keyframe_insert(data_path="location")

# -------------------- INITIAL CONDITIONS ----------
class InitialConditions():
    def __init__(self, theta_x, theta_y, omega_x, omega_y):
        self.theta_x = theta_x
        self.theta_y = theta_y

        self.omega_x = omega_x
        self.omega_y = omega_y

    def reset(self, theta_x, theta_y, omega_x, omega_y):
        self.theta_x = theta_x
        self.theta_y = theta_y

        self.omega_x = omega_x
        self.omega_y = omega_y


def test_bille():
    # Example
    my_bille = Bille()
    my_bille.blender_init()
    my_bille._bille.animation_data_clear()
    my_bille._socle.animation_data_clear()

    total_time = 3
    fps = 24  # Frames per second (fps)
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = int(total_time * fps) + 1
    keyframe_freq = 1
    nlast = bpy.context.scene.frame_end
    dt = 1 / fps

    init_conditions = InitialConditions(theta_x=0, theta_y=0, omega_x=0, omega_y=0)
    a_x = 0.5
    a_y = 0.5

    t_relatif = 0
    sx_t = np.array([])
    sy_t = np.array([])
    wx_t = np.array([])
    wy_t = np.array([])

    x_0 = 0
    y_0 = 0
    vx_0 = 0
    vy_0 = 0

    for n in range(nlast):
        t = total_time * n / nlast

        if n % keyframe_freq == 0:
            bpy.context.scene.frame_set(n)
            if n == 24:  # In full code, if condifiton will be something like if new_accel_x != old_accel_x or y
                init_conditions.reset(theta_x=sx_t[-1], theta_y=sy_t[-1], omega_x=wx_t[-1], omega_y=wy_t[-1])
                vx_0 = vx_0 + a_x * t_relatif
                x_0 = my_bille._socle.location.x
                a_x = -0.5

                vy_0 = vy_0 + a_y * t_relatif
                y_0 = my_bille._socle.location.y
                a_y = -0.5

                t_relatif = 1 / fps

            theta_x = my_bille.calculate_next_theta(t_relatif, a_x, init_conditions.theta_x, init_conditions.omega_x, 1)
            omega_x = my_bille.calculate_next_omega(t_relatif, a_x, init_conditions.theta_x, init_conditions.omega_x, 1)
            sx_t = np.append(sx_t, theta_x)
            wx_t = np.append(wx_t, omega_x)

            theta_y = my_bille.calculate_next_theta(t_relatif, a_y, init_conditions.theta_y, init_conditions.omega_y, 1)
            omega_y = my_bille.calculate_next_omega(t_relatif, a_y, init_conditions.theta_y, init_conditions.omega_y, 1)
            sy_t = np.append(sy_t, theta_y)
            wy_t = np.append(wy_t, omega_y)

            next_x, next_y = my_bille.calculate_next_pos(theta_x, theta_y)
            my_bille.blender_update(next_x, next_y)
            my_bille._bille.keyframe_insert(data_path="location")
            my_bille._socle.location.x = 1 / 2 * a_x * t_relatif ** 2 + vx_0 * t_relatif + x_0
            my_bille._socle.location.y = 1 / 2 * a_y * t_relatif ** 2 + vy_0 * t_relatif + y_0
            my_bille._socle.keyframe_insert(data_path="location")

            print(f'n={n}\ta={a_x}\tt_relatif={t_relatif}\tx_0={x_0}\tv_0={vx_0}')
            t_relatif += 1 / fps