# ----------------------- BILLE -----------------------

class Ball:
    g = 9.81

    def __init__(self, theta=0, x=0, y=0, z=0):
        self.radius_ball = 0.008
        self.radius_pendulum = 0.14
        self.position = Position(x, y, z)
        self.theta = theta
        self.ball_obj = None
        self.socket_obj = None

    def calculate_next_theta(self, t, a, theta_0, omega_0, u):
        """
        :param t: time (float)
        :param a: linear acceleration of the car (float)
        :param theta_0: initial angle with vertical (float)
        :param omega_0: initial angular velocity (float)
        :param u: friction coefficient (float)
        :return: next angle with vertical of ball, in rads (float)
        """
        # Differential equation of accelerating pendulum (based on force diagram) : theta'' + g/L theta' = a/L
        friction_curve = np.exp(-u * t)
        b = self.g / self.radius_pendulum
        c = -a / self.radius_pendulum
        b_sqrt = np.sqrt(b)

        A = theta_0 - c / b
        B = omega_0 / b_sqrt

        # By solving the differential equation mentionned above, we get:
        theta = A * np.cos(b_sqrt * t) + B * np.sin(b_sqrt * t) + c / b

        return theta * friction_curve

    def calculate_next_omega(self, t, a, theta_0, omega_0, u):
        """
        :param t: time (float)
        :param a: linear acceleration of the car (float)
        :param theta_0: initial angle with vertical (float)
        :param omega_0: initial angular velocity (float)
        :param u: friction coefficient (float)
        :return: next angular velocity of ball(float)
        """
        # Diffrential equation of accelerating pendulum (based on force diagram) : theta'' + g/L theta' = -a/L
        friction_curve = np.exp(-u * t)
        b = self.g / self.radius_pendulum
        c = -a / self.radius_pendulum
        b_sqrt = np.sqrt(b)

        A = theta_0 - c / b
        B = omega_0 / b_sqrt

        # By solving the differential equation mentionned above, we get:
        theta = A * np.cos(b_sqrt * t) + B * np.sin(b_sqrt * t) + c / b

        # By differentiating theta, we get:
        angular_velocity = -A * np.sin(b_sqrt * t) * b_sqrt + B * np.cos(b_sqrt * t) * b_sqrt

        return angular_velocity * friction_curve + -u * friction_curve * theta  # Dampened Angular velocity = d/dt(theta*friction_curve)

    def calculate_next_pos(self, theta_x, theta_y):
        """
        :param theta_x: angle with vertical in x-axis(rads)
        :param theta_y: angle with vertical in y-axis(rads)
        :return: x, y positions
        """
        next_x = self.radius_pendulum * np.sin(theta_x)
        next_y = self.radius_pendulum * np.sin(theta_y)
        return next_x, next_y

    def blender_init(self):
        try:
            self.socket_obj = bpy.data.objects['socle']
        except:
            bpy.ops.mesh.primitive_cube_add(size=0.05, enter_editmode=False, align='WORLD', location=(0, 0, -0.005),
                                            scale=(1, 1, 0.2))
            bpy.context.active_object.name = 'socle'
            self.socket_obj = bpy.data.objects['socle']

        try:
            self.ball_obj = bpy.data.objects['bille']
        except:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=self.radius_ball, enter_editmode=False, align='WORLD',
                                                 location=(self.socket_obj.location.x, self.position.y,
                                                           self.socket_obj.location.z + self.socket_obj.dimensions[
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
        """
        Function that keeps track of most recent initial conditions of ball. Every time the acceleration of the car
        changes, the ball oscillation must be recalculated with new parameters.
        :param theta_x: current angle with vertical of the ball in x-axis (rads)
        :param theta_y: current angle with vertical of the ball in y-axis (rads)
        :param omega_x: current angular velocity in x-axis
        :param omega_y: current angular velocity in y-axis
        """
        self.theta_x = theta_x
        self.theta_y = theta_y

        self.omega_x = omega_x
        self.omega_y = omega_y
