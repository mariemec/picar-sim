# ----------------------- CAR -----------------------
class Car:
    car_obj = None
    length = 0.267
    width = 0.1
    suiveur_ligne_obj = []
    acceleration = 0
    current_radius = 0

    def __init__(self, map, x=0, y=0, orientation=0, speed_factor=0, refresh_rate=24):
        self.position = Position(x, y)
        self.orientation = orientation
        self.speed_factor = speed_factor
        self.refresh_rate = refresh_rate
        self.speed = (self.speed_factor / 100) / (1 / self.refresh_rate)
        self.line_follower = LineFollower(self.position, map, self.refresh_rate,
                                          position_offset=self.length / 2 * 100 + 2)
        self.distance_sensor = DistanceSensor(self.position, map._map)

    def calculate_next_pos(self):
        orientation = self.line_follower.update_orientation(self.orientation, self.speed, self.suiveur_ligne_obj)
        speed_factor = self.distance_sensor.update_speed_factor(self.speed_factor, self.orientation, self.position)

        x1 = self.position.x
        x2 = self.position.x + speed_factor * np.cos(orientation)
        y1 = self.position.y
        y2 = self.position.y + speed_factor * np.sin(orientation)

        delta_s = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        delta_theta = np.abs(self.orientation - orientation)

        if orientation > 2 * np.pi:
            orientation -= 2 * np.pi
        if orientation < 0:
            orientation += 2 * np.pi

        self.current_radius = (delta_s / delta_theta) / 100

        print(f'radius: {self.current_radius}')

        return (self.position.x + speed_factor * np.cos(orientation),
                self.position.y + speed_factor * np.sin(orientation),
                orientation,
                speed_factor)

    def blender_init(self):
        try:
            self.car_obj = bpy.data.objects['Car']
        except:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(self.position.x, self.position.y, 0),
                                            rotation=(0, 0, self.orientation), scale=(self.length, self.width, 0.1))
            bpy.context.active_object.name = 'Car'
            self.car_obj = bpy.data.objects['Car']

        for i in range(5):
            bpy.ops.mesh.primitive_cube_add(size=0.01, location=(self.position.x, self.position.y + (i - 2) / 100, 0),
                                            rotation=(0, 0, 0))
            bpy.context.active_object.name = f'suiveur_ligne{i}'
            self.suiveur_ligne_obj += [bpy.data.objects[f'suiveur_ligne{i}']]

    def blender_update(self):
        self.position.x, self.position.y, self.orientation, self.speed_factor = self.calculate_next_pos()
        self.car_obj.location[0] = self.position.x / 100
        self.car_obj.location[1] = self.position.y / 100
        self.car_obj.rotation_euler[2] = self.orientation
        old_speed = self.speed
        self.speed = (self.speed_factor / 100) / (1 / self.refresh_rate)
        self.acceleration = (self.speed - old_speed) / (1 / self.refresh_rate)


class LineFollower:
    """
    the line follower dictates the car orientation.

    >> update_orientation will return an updated orientation based on the line follower sensors state.
    """
    sensor_state = [0] * 5
    last_sensor = None

    def __init__(self, position, _map, refresh_rate):
        self.position = position
        self._map = _map
        self.refresh_rate = refresh_rate

    def __get_state(self, orientation, suiveur_ligne_obj):
        """
        private method to get the line follower sensors state
        :param orientation: current car orientation
        :return: list containing the 5 sensors state
        """

        if 0 <= orientation < np.pi / 2:
            phi = orientation
        elif np.pi / 2 <= orientation < np.pi:
            phi = np.pi - orientation
        elif np.pi <= orientation < 3 * np.pi / 2:
            phi = orientation - np.pi
        elif 3 * np.pi / 2 <= orientation < 2 * np.pi:
            phi = -orientation
        else:
            print('orientation is fucked')
            print(orientation)

        x0 = 4 * np.sin(phi)
        x1 = 2 * np.sin(phi)
        x2 = self.position.x + self.position_offset * np.cos(orientation)
        x3 = 2 * np.sin(phi)
        x4 = 4 * np.sin(phi)
        x_offsets = [x0, x1, x2, x3, x4]

        y0 = 4 * np.cos(phi)
        y1 = 2 * np.cos(phi)
        y2 = self.position.y + self.position_offset * np.sin(orientation)
        y3 = 2 * np.cos(phi)
        y4 = 4 * np.cos(phi)
        y_offsets = [y0, y1, y2, y3, y4]

        # loops through the sensors_state list to update their state
        for i in range(len(self.sensor_state)):
            if i == 2:
                x = int(round(x2))
                y = int(round(y2))
            else:
                if 0 <= orientation < np.pi / 2:
                    if i == 0 or i == 1:
                        x = int(round(x2 - x_offsets[i]))
                        y = int(round(y2 + y_offsets[i]))
                    if i == 3 or i == 4:
                        x = int(round(x2 + x_offsets[i]))
                        y = int(round(y2 - y_offsets[i]))
                elif np.pi / 2 <= orientation < np.pi:
                    if i == 0 or i == 1:
                        x = int(round(x2 - x_offsets[i]))
                        y = int(round(y2 - y_offsets[i]))
                    if i == 3 or i == 4:
                        x = int(round(x2 + x_offsets[i]))
                        y = int(round(y2 + y_offsets[i]))
                elif np.pi <= orientation < 3 * np.pi / 2:
                    if i == 0 or i == 1:
                        x = int(round(x2 + x_offsets[i]))
                        y = int(round(y2 - y_offsets[i]))
                    if i == 3 or i == 4:
                        x = int(round(x2 - x_offsets[i]))
                        y = int(round(y2 + y_offsets[i]))
                elif 3 * np.pi / 2 <= orientation < 2 * np.pi:
                    if i == 0 or i == 1:
                        x = int(round(x2 + x_offsets[i]))
                        y = int(round(y2 + y_offsets[i]))
                    if i == 3 or i == 4:
                        x = int(round(x2 - x_offsets[i]))
                        y = int(round(y2 - y_offsets[i]))

            self.sensor_state[i] = self._map.peek(x, y)
            suiveur_ligne_obj[i].location[0] = x / 100
            suiveur_ligne_obj[i].location[1] = y / 100

    def update_orientation(self, orientation, current_speed, suiveur_ligne_obj):
        """
        public method to get the updated car orientation
        :param current_speed: current car speed
        :param orientation: current car orientation
        :return: new car orientation
        """
        self.__get_state(orientation, suiveur_ligne_obj)

        print(f'sensor_state: {self.sensor_state} | last_sensor: {self.last_sensor}')
        if self.sensor_state[2] != 1:
            if 1 in self.sensor_state:
                adjacent_dist = current_speed * 100
                if self.sensor_state[1]:
                    orientation += np.arctan(2 / adjacent_dist)
                elif self.sensor_state[3]:
                    orientation -= np.arctan(2 / adjacent_dist)
                elif self.sensor_state[0]:
                    orientation += np.arctan(4 / adjacent_dist)
                elif self.sensor_state[4]:
                    orientation -= np.arctan(4 / adjacent_dist)
        elif self.sensor_state[2] == 1:
            adjacent_dist = current_speed * 100
            if self.last_sensor == 1:
                orientation -= np.arctan(2 / adjacent_dist) / 2
            elif self.last_sensor == 3:
                orientation += np.arctan(2 / adjacent_dist) / 2
        try:
            self.last_sensor = self.sensor_state.index(1)
        except:
            pass

        return round(orientation, 4)


class DistanceSensor:
    distance = 9999999999  # temporaire -> va être initialisé à 0 et updaté dans get_distance()
    slowing_distance = 50  # doit être changé par le bonne valeur
    stopping_distance = 20  # doit être changé par la bonne valeur

    def __init__(self, position, _map):
        self.position = position
        self._map = _map

    def get_distance(self, orientation, position):
        tt = np.argwhere(self._map == 1)
        # if tt.any():
        #    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        x = np.array([position.x, position.y])
        y = np.argwhere(self._map == 2)

        distance_min = self.distance
        if y.any():
            # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            d = y - x

            coord = []
            vals = []

            angle = int(np.rad2deg(orientation))
            min_angle = angle - 15 + 90
            max_angle = angle + 16 + 90

            #            if min_angle <0:
            #                min_angle = 360 + min_angle
            #            if max_angle > 360:
            #                max_angle =  0 + (max_angle - 360)

            print(f'min angle {min_angle}  max angle {max_angle}')

            for phi in range(min_angle, max_angle):
                yy = y
                for val in yy:
                    val = list(val)
                    if 0 < phi < 90:
                        if (val[0] < x[0]) and (val[1] > x[1]):
                            if val not in vals:
                                vals += [val]

                    if 90 < phi < 180:
                        if val[0] > x[0] and val[1] < x[1]:
                            if val not in vals:
                                vals += [val]

                    if 180 < phi < 270:
                        if val[0] > x[0] and val[1] > x[1]:
                            if val not in vals:
                                vals += [val]

                    if 270 < phi < 360:
                        if val[0] < x[0] and val[1] > x[1]:
                            if val not in vals:
                                vals += [val]

                    if phi == 0 or phi == 360:
                        if val[1] == x[1] and val[0] < x[0]:
                            if val not in vals:
                                vals += [val]
                    if phi == 90:
                        if val[1] == x[1] and val[0] > x[0]:
                            if val not in vals:
                                vals += [val]

                    if phi == 180:
                        if val[0] == x[0] and val[1] < x[1]:
                            if val not in vals:
                                vals += [val]
                    if phi == 270:
                        if val[1] == x[1] and val[0] > x[0]:
                            if val not in vals:
                                vals += [val]
            if np.array(vals).any():
                dd = np.array(vals) - x
                # +- 15 pcq le sensor voit dans un rayon de 30 deg
                for phi in range(min_angle, max_angle):
                    on_ray = np.abs(dd @ (np.sin(np.deg2rad(-phi - 90)), np.cos(np.deg2rad(-phi - 90)))) < np.sqrt(0.5)
                    if any(on_ray):
                        vals = np.array(vals)
                        ymin = vals[on_ray][np.argmin(np.einsum('ij,ij->i', dd[on_ray], dd[on_ray]))]
                        dist = np.sqrt((x[0] - ymin[0]) ** 2 + (x[1] - ymin[1]) ** 2)
                        if distance_min > dist:
                            print("**************************************************")
                            print(phi, x[0])
                            coord = ymin
                            distance_min = dist

        return distance_min

    def update_speed_factor(self, speed_factor, orientation, pos):
        isObstacle = False
        self.distance = self.get_distance(orientation, pos)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("distance : ", self.distance, "orientation", np.rad2deg(orientation))

        #####change ca pour des elsif
        if self.distance < self.stopping_distance:
            # arret
            speed_factor = 0
            isObstacle = True
            # contourner(orientation)
        elif self.distance < self.slowing_distance:
            # ralenti
            speed_factor -= 0.01
        elif self.distance > self.slowing_distance:
            if speed_factor < 0.91666:
                speed_factor += 0.1

        return round(speed_factor, 4)