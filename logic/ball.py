# ----------------------- BILLE -----------------------
class Ball:
    g = 9.81

    def __init__(self, theta=0, x=0, y=0, z=0):
        self.mass = 0.005
        self.radius_ball = 0.008
        self.radius_pendulum = 0.14
        self.position = Position(x, y, z)
        self.theta = theta
        self.ball_obj = None
        self.holder_obj = None

    def calculate_next_theta(self, t, a, theta_0, omega_0, u):
        damping = np.exp(-u * t)
        b = self.g / self.radius_pendulum
        c = -a / self.radius_pendulum
        b_sqrt = np.sqrt(b)

        A = theta_0 - c / b
        B = omega_0 / b_sqrt

        position = A * np.cos(b_sqrt * t) + B * np.sin(b_sqrt * t) + c / b

        return position * damping  # Position = Theta * e^(-damp*t)

    def calculate_next_omega(self, t, a, theta_0, omega_0, u):
        damping = np.exp(-u * t)
        b = self.g / self.radius_pendulum
        c = -a / self.radius_pendulum
        b_sqrt = np.sqrt(b)

        A = theta_0 - c / b
        B = omega_0 / b_sqrt

        position = A * np.cos(b_sqrt * t) + B * np.sin(b_sqrt * t) + c / b
        angular_velocity = -A * np.sin(b_sqrt * t) * b_sqrt + B * np.cos(b_sqrt * t) * b_sqrt

        return angular_velocity * damping + -u * damping * position  # Velocity = d/dt(Position)

    def calculate_next_pos(self, theta_x, theta_y):
        next_x = self.radius_pendulum * np.sin(theta_x)
        next_y = self.radius_pendulum * np.sin(theta_y)
        return next_x, next_y

    def blender_init(self):
        try:
            self.holder_obj = bpy.data.objects['socle']
        except:
            bpy.ops.mesh.primitive_cube_add(size=0.05, enter_editmode=False, align='WORLD', location=(0, 0, -0.005),
                                            scale=(1, 1, 0.2))
            bpy.context.active_object.name = 'socle'
            self.holder_obj = bpy.data.objects['socle']

        try:
            self.ball_obj = bpy.data.objects['bille']
        except:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=self.radius_ball, enter_editmode=False, align='WORLD',
                                                 location=(self.holder_obj.location.x, self.position.y,
                                                           self.holder_obj.location.z + self.holder_obj.dimensions[
                                                               2] - 0.0015 + self.radius_ball), scale=(1, 1, 1))
            bpy.context.active_object.name = 'bille'
            self.ball_obj = bpy.data.objects['bille']

    def blender_update(self, x, y):
        self.position.x = x
        self.position.y = y
        self.ball_obj.location.x = x
        self.ball_obj.location.y = y
        self.ball_obj.location.z = self.position.z
        self.ball_obj.keyframe_insert(data_path="location")


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
