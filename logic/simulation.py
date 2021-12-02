from trajectoire import *
from car import Car


class Simulation:
    def __init__(self, m, n, segments):
        self.trajectoire = Trajectoire(m=m, n=n, segments=segments)
        self.car = Car(self.trajectoire.map)

## MAIN CODE
# m, n = 300, 300
# nb_frame = 1500
# bpy.context.scene.frame_end = nb_frame
# fps = 24
# # sim = Simulation(500, 500, [Droite((0, 10), (50, 10)),
# # Courbe((50, 30), 20, 3*np.pi/2, 5*np.pi/2),
# # Courbe((50, 70), 20, np.pi, 3*np.pi/2),
# # Droite((30, 70), (30, 199))])
# segs = []
#
# # Départ
# segs.append(Droite((0, 0), (183, 0)))
# segs.append(Courbe((183, 17), 17, math.pi * 3 / 2, math.pi * 5 / 2))
#
# # Zone 1
# segs.append(Droite((183, 34), (17, 34)))
# # segs.append(Obstacle((1000,340), 0)
#
# segs.append(Courbe((17, 51), 17, math.pi * 1 / 2, math.pi * 3 / 2))
# segs.append(Droite((17, 68), (51, 68)))
# segs.append(Courbe((51, 85), 17, math.pi * 3 / 2, math.pi * 2))
#
# # Zone 2
# segs.append(Droite((68, 85), (68, 149)))
# # segs.append(Obstacle((680,1000), 90)
#
# segs.append(Courbe((85, 149), 17, math.pi * 1 / 2, math.pi))
# segs.append(Courbe((85, 183), 17, math.pi * 3 / 2, math.pi * 2))
# segs.append(Courbe((119, 183), 17, math.pi * 1 / 2, math.pi))
# segs.append(Droite((119, 200), (149, 200)))
# segs.append(Courbe((149, 183), 17, 0, math.pi * 1 / 2))
#
# # Zone 3
# segs.append(Droite((166, 183), (166, 68)))
# # segs.append(Obstacle((1660,1000), 90)
#
# # T final
# segs.append(Droite((156, 68), (176, 68)))
# sim = Simulation(m, n, segs)
# sim.trajectoire.map.print_map_to_file()
#
# car = sim.car
# car.position.x = 0
# car.position.y = 0
# car.blender_init()
#
# my_bille = Bille()
# my_bille.blender_init()
# my_bille._socle.parent = car.car_obj
#
# init_conditions = InitialConditions(theta_x=0, theta_y=0, omega_x=0, omega_y=0)
# t_relatif = 0
# sx_t = np.array([])
# sy_t = np.array([])
# wx_t = np.array([])
# wy_t = np.array([])
#
# last_a_x = 0
# last_a_y = 0
# a_x = 0
# a_y = 0
# x_0 = 0
# y_0 = 0
# vx_0 = 0
# vy_0 = 0
# last_radius = 0
# wheelbase = 0.14
#
# for i in range(nb_frame):
#     bpy.context.scene.frame_set(i)
#     car.blender_update()
#     a = car.acceleration
#     v = car.speed
#     radius = car.current_radius
#     if radius != last_radius and radius != 0:
#         # Car is turning
#         a_tangential = v * v / radius
#         a_x = a_tangential * np.cos(np.deg2rad(car.orientation))
#         a_y = a_tangential * np.sin(np.deg2rad(car.orientation))
#         last_radius = radius
#     else:
#         a_x = a * np.cos(np.deg2rad(car.orientation))
#         a_y = a * np.sin(np.deg2rad(car.orientation))
#
#     if ((a_x != last_a_x) or (a_y != last_a_y)) and (i != 0):
#         init_conditions.reset(theta_x=sx_t[-1], theta_y=sy_t[-1], omega_x=wx_t[-1], omega_y=wy_t[-1])
#         last_a_x = a_x
#         last_a_y = a_y
#
#         t_relatif = 1 / fps
#
#     theta_x = my_bille.calculate_next_theta(t_relatif, a_x, init_conditions.theta_x, init_conditions.omega_x, 1)
#     omega_x = my_bille.calculate_next_omega(t_relatif, a_x, init_conditions.theta_x, init_conditions.omega_x, 1)
#     sx_t = np.append(sx_t, theta_x)
#     wx_t = np.append(wx_t, omega_x)
#
#     theta_y = my_bille.calculate_next_theta(t_relatif, a_y, init_conditions.theta_y, init_conditions.omega_y, 1)
#     omega_y = my_bille.calculate_next_omega(t_relatif, a_y, init_conditions.theta_y, init_conditions.omega_y, 1)
#     sy_t = np.append(sy_t, theta_y)
#     wy_t = np.append(wy_t, omega_y)
#
#     next_x, next_y = my_bille.calculate_next_pos(theta_x, theta_y)
#     my_bille.blender_update(next_x, next_y)
#     my_bille._bille.keyframe_insert(data_path="location")
#     my_bille._socle.keyframe_insert(data_path="location")
#     car.car_obj.keyframe_insert(data_path='location')
#     car.car_obj.keyframe_insert(data_path='rotation_euler')
#     for sensor_obj in car.suiveur_ligne_obj:
#         sensor_obj.keyframe_insert(data_path='location')
#     print(
#         f'n={i}\torientation={np.rad2deg(car.orientation)}\tax={a_x}\tay={a_y}\ttheta_x={np.rad2deg(theta_x):.2f}\tthta_y={np.rad2deg(theta_y):.2f}')
#     t_relatif += 1 / fps

