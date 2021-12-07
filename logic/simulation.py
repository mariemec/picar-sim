# ----------------------SIMULATION-----------------------------
class Simulation:

    def __init__(self, m, n, segments):
        self.trajectory = Trajectory(m=m, n=n, segments=segments)
        self.car = Car(self.trajectory.map)
        self.ball = Ball(z=self.car.height)
        self.init_conditions = InitialConditions(theta_x=0, theta_y=0, omega_x=0, omega_y=0)

    def run(self):
        nb_frame = 1800
        bpy.context.scene.frame_end = nb_frame
        fps = 24
        t_relatif = 0
        sx_t = np.array([])
        sy_t = np.array([])
        wx_t = np.array([])
        wy_t = np.array([])
        last_a_x = 0
        last_a_y = 0

        self.car.blender_init()
        self.ball.blender_init()
        self.ball.socket_obj.parent = self.car.car_obj
        self.ball.socket_obj.location[2] = self.car.height / 2 + self.ball.socket_obj.dimensions[2] / 2

        for i in range(nb_frame):
            bpy.context.scene.frame_set(i)

            # Update car position
            self.car.blender_update()

            a = self.car.acceleration
            v = self.car.speed
            radius = self.car.current_radius

            # If the car is turning, calculate centripetal acceleration. Otherwise, split a into x,y components
            if radius != 0 and radius < 100:
                # Car is turning
                a_centripetal = (v * v) / radius
                a_x = a_centripetal * np.cos(self.car.orientation)
                a_y = a_centripetal * np.sin(self.car.orientation)
            else:
                a_x = a * np.cos(self.car.orientation)
                a_y = a * np.sin(self.car.orientation)

            # If acceleration is changing, ball trajectory needs to be recalculated
            if ((a_x != last_a_x) or (a_y != last_a_y)) and (i != 0):
                self.init_conditions.reset(theta_x=sx_t[-1], theta_y=sy_t[-1], omega_x=wx_t[-1], omega_y=wy_t[-1])
                last_a_x = a_x
                last_a_y = a_y
                t_relatif = 1 / fps

            # Friction coefficient
            mu = 0.2

            # Calculate next ball angle with vertical (x-axis)
            theta_x = self.ball.calculate_next_theta(t_relatif, a_x, self.init_conditions.theta_x,
                                                     self.init_conditions.omega_x, mu)
            omega_x = self.ball.calculate_next_omega(t_relatif, a_x, self.init_conditions.theta_x,
                                                     self.init_conditions.omega_x, mu)
            sx_t = np.append(sx_t, theta_x)
            wx_t = np.append(wx_t, omega_x)

            # Calculate next ball angle with vertical (y-axis)
            theta_y = self.ball.calculate_next_theta(t_relatif, a_y, self.init_conditions.theta_y,
                                                     self.init_conditions.omega_y, mu)
            omega_y = self.ball.calculate_next_omega(t_relatif, a_y, self.init_conditions.theta_y,
                                                     self.init_conditions.omega_y, mu)
            sy_t = np.append(sy_t, theta_y)
            wy_t = np.append(wy_t, omega_y)

            # Pendulum calculation (2 angles)
            next_x, next_y = self.ball.calculate_next_pos(theta_x, theta_y)

            # Update position of ball
            self.ball.blender_update(next_x + self.car.car_obj.location.x, next_y + self.car.car_obj.location.y)

            # Insert all keyframes for animation
            self.ball.ball_obj.keyframe_insert(data_path="location")
            self.ball.socket_obj.keyframe_insert(data_path="location")
            self.car.car_obj.keyframe_insert(data_path='location')
            self.car.car_obj.keyframe_insert(data_path='rotation_euler')
            for sensor_obj in self.car.line_follower.line_follower_obj:
                sensor_obj.keyframe_insert(data_path='location')

            # increase timeframe
            t_relatif += 1 / fps


## MAIN CODE
segs = []

# Départ
segs.append(Line((0, 0), (183, 0)))
segs.append(Curve((183, 17), 17, math.pi * 3 / 2, math.pi * 5 / 2))

# Zone 1
segs.append(Line((183, 34), (17, 34)))
segs.append(Obstacle((100,34), 0))

segs.append(Curve((17, 51), 17, math.pi * 1 / 2, math.pi * 3 / 2))
segs.append(Line((17, 68), (51, 68)))
segs.append(Curve((51, 85), 17, math.pi * 3 / 2, math.pi * 2))

# Zone 2
segs.append(Line((68, 85), (68, 149)))
segs.append(Obstacle((68,110), 90))

segs.append(Curve((85, 149), 17, math.pi * 1 / 2, math.pi))
segs.append(Curve((85, 183), 17, math.pi * 3 / 2, math.pi * 2))
segs.append(Curve((119, 183), 17, math.pi * 1 / 2, math.pi))
segs.append(Line((119, 200), (149, 200)))
segs.append(Curve((149, 183), 17, 0, math.pi * 1 / 2))

# Zone 3
segs.append(Line((166, 183), (166, 68)))
segs.append(Obstacle((166, 120), 90))

# T final
segs.append(Line((156, 68), (176, 68)))
m = 250
n = 250
sim = Simulation(m, n, segs)
# sim.trajectoire.map.print_map_to_file()

sim.run()

