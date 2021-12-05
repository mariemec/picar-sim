class Simulation:
    def __init__(self, m, n, segments):
        self.trajectory = Trajectory(m=m, n=n, segments=segments)
        self.car = Car(self.trajectory.map)


## MAIN CODE
m, n = 300, 300
nb_frame = 1800
bpy.context.scene.frame_end = nb_frame
fps = 24
segs = []

# Départ
segs.append(Line((0, 0), (183, 0)))
segs.append(Curve((183, 17), 17, math.pi * 3 / 2, math.pi * 5 / 2))
# segs.append(Obstacle((100,0), 0))

# Zone 1
segs.append(Line((183, 34), (17, 34)))
# segs.append(Obstacle((100,34), 0))

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
segs.append(Obstacle((166, 100), 90))

# T final
segs.append(Line((156, 68), (176, 68)))
sim = Simulation(m, n, segs)
# sim.trajectoire.map.print_map_to_file()

car = sim.car
car.position.x = 0
car.position.y = 0
car.blender_init()

my_ball = Ball(z=car.height)
my_ball.blender_init()
my_ball.holder_obj.parent = car.car_obj
my_ball.holder_obj.location[2] = car.height / 2 + my_ball.holder_obj.dimensions[2] / 2

init_conditions = InitialConditions(theta_x=0, theta_y=0, omega_x=0, omega_y=0)
t_relatif = 0
sx_t = np.array([])
sy_t = np.array([])
wx_t = np.array([])
wy_t = np.array([])

last_a_x = 0
last_a_y = 0
a_x = 0
a_y = 0
x_0 = 0
y_0 = 0
vx_0 = 0
vy_0 = 0

for i in range(nb_frame):
    bpy.context.scene.frame_set(i)
    car.blender_update()
    a = car.acceleration
    v = car.speed
    radius = car.current_radius
    if radius != 0 and radius < 100:
        # Car is turning
        a_centripetal = (v * v) / radius
        a_x = a_centripetal * np.cos(car.orientation)
        a_y = a_centripetal * np.sin(car.orientation)
    else:
        a_x = a * np.cos(car.orientation)
        a_y = a * np.sin(car.orientation)

    if ((a_x != last_a_x) or (a_y != last_a_y)) and (i != 0):
        init_conditions.reset(theta_x=sx_t[-1], theta_y=sy_t[-1], omega_x=wx_t[-1], omega_y=wy_t[-1])
        last_a_x = a_x
        last_a_y = a_y

        t_relatif = 1 / fps

    theta_x = my_ball.calculate_next_theta(t_relatif, a_x, init_conditions.theta_x, init_conditions.omega_x, 0.2)
    omega_x = my_ball.calculate_next_omega(t_relatif, a_x, init_conditions.theta_x, init_conditions.omega_x, 0.2)
    sx_t = np.append(sx_t, theta_x)
    wx_t = np.append(wx_t, omega_x)

    theta_y = my_ball.calculate_next_theta(t_relatif, a_y, init_conditions.theta_y, init_conditions.omega_y, 0.2)
    omega_y = my_ball.calculate_next_omega(t_relatif, a_y, init_conditions.theta_y, init_conditions.omega_y, 0.2)
    sy_t = np.append(sy_t, theta_y)
    wy_t = np.append(wy_t, omega_y)

    next_x, next_y = my_ball.calculate_next_pos(theta_x, theta_y)
    my_ball.blender_update(next_x + car.car_obj.location.x, next_y + car.car_obj.location.y)

    my_ball.ball_obj.keyframe_insert(data_path="location")
    my_ball.holder_obj.keyframe_insert(data_path="location")
    car.car_obj.keyframe_insert(data_path='location')
    car.car_obj.keyframe_insert(data_path='rotation_euler')
    for sensor_obj in car.line_follower.line_follower_obj:
        sensor_obj.keyframe_insert(data_path='location')
    print(
        f'n={i}\torientation={np.rad2deg(car.orientation)}\tradius={car.current_radius}\tv={car.speed:.2f}m/s\tax={a_x}\tay={a_y}\ttheta_x={np.rad2deg(theta_x):.2f}\tthta_y={np.rad2deg(theta_y):.2f}')
    t_relatif += 1 / fps

