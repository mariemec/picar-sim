class Car:
    car_obj = None
    length = 0.267
    width = 0.1
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
        self.distance_sensor = DistanceSensor(self.position, map)

    def update_position(self):
        self.line_follower.check_sensors(self.orientation)
        next_orientation = self.get_next_orientation()
        self.distance_sensor.check_sensor(self.orientation)
        self.update_speed_factor()
        self.current_radius = self.get_turn_radius(next_orientation)
        self.orientation = self.normalize_angle(next_orientation)
        self.position.x = self.position.x + self.speed_factor * np.cos(self.orientation)
        self.position.y = self.position.y + self.speed_factor * np.sin(self.orientation)

    def get_next_orientation(self):
        """
        public method to car orientation
        """
        ss = self.line_follower.sensor_state
        next_orientation = self.orientation
        if ss[2] != 1:
            if 1 in ss:
                adjacent_dist = self.speed * 100
                if ss[1]:
                    next_orientation += np.arctan(2 / adjacent_dist)
                elif ss[3]:
                    next_orientation -= np.arctan(2 / adjacent_dist)
                elif ss[0]:
                    next_orientation += np.arctan(4 / adjacent_dist)
                elif ss[4]:
                    next_orientation -= np.arctan(4 / adjacent_dist)
        elif ss[2] == 1:
            adjacent_dist = self.speed * 100
            if self.line_follower.last_sensor == 1:
                next_orientation -= np.arctan(2 / adjacent_dist) / 2
            elif self.line_follower.last_sensor == 3:
                next_orientation += np.arctan(2 / adjacent_dist) / 2
        try:
            self.line_follower.last_sensor = ss.index(1)  # get index of active sensor
        except:
            pass

        return round(next_orientation, 4)

    def update_speed_factor(self):
        dist = self.distance_sensor.distance
        stop_dist = self.distance_sensor.stopping_distance
        slow_dist = self.distance_sensor.slowing_distance

        if dist < stop_dist:
            # arret
            self.speed_factor = 0
        elif dist < slow_dist:
            # ralentir
            self.speed_factor -= 0.01
        elif dist > slow_dist:
            if self.speed_factor < 0.91666:
                self.speed_factor += 0.1

        self.speed_factor = round(self.speed_factor, 4)

    def get_turn_radius(self, next_orientation):
        x1 = self.position.x
        x2 = self.position.x + self.speed_factor * np.cos(next_orientation)
        y1 = self.position.y
        y2 = self.position.y + self.speed_factor * np.sin(next_orientation)

        delta_s = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        delta_theta = np.abs(self.orientation - next_orientation)
        return (delta_s / delta_theta) / 100

    def normalize_angle(self, angle):
        if angle > 2 * np.pi:
            angle -= 2 * np.pi
        if angle < 0:
            angle += 2 * np.pi
        return angle

    def blender_init(self):
        try:
            self.car_obj = bpy.data.objects['Car']
        except:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(self.position.x, self.position.y, 0),
                                            rotation=(0, 0, self.orientation), scale=(self.length, self.width, 0.1))
            bpy.context.active_object.name = 'Car'
            self.car_obj = bpy.data.objects['Car']

        self.line_follower.blender_init()

    def blender_update(self):
        self.update_position()
        self.car_obj.location[0] = self.position.x / 100
        self.car_obj.location[1] = self.position.y / 100
        self.car_obj.rotation_euler[2] = self.orientation
        old_speed = self.speed
        self.speed = (self.speed_factor / 100) / (1 / self.refresh_rate)
        self.acceleration = (self.speed - old_speed) / (1 / self.refresh_rate)

        self.line_follower.blender_update()


class LineFollower:
    """
    the line follower dictates the car orientation.

    >> update_orientation will return an updated orientation based on the line follower sensors state.
    """
    line_follower_obj = []
    sensor_state = [0] * 5
    x_pos = [0] * 5
    y_pos = [0] * 5
    last_sensor = None

    def __init__(self, position, _map, refresh_rate, position_offset=0):
        self.position = position
        self._map = _map
        self.refresh_rate = refresh_rate
        self.position_offset = position_offset

    def blender_init(self):
        for i in range(5):
            bpy.ops.mesh.primitive_cube_add(size=0.01, location=(self.position.x, self.position.y + (i - 2) / 100, 0),
                                            rotation=(0, 0, 0))
            bpy.context.active_object.name = f'suiveur_ligne{i}'
            self.line_follower_obj += [bpy.data.objects[f'suiveur_ligne{i}']]

    def blender_update(self):
        for i in range(5):
            self.line_follower_obj[i].location[0] = self.x_pos[i] / 100
            self.line_follower_obj[i].location[1] = self.y_pos[i] / 100

    def check_sensors(self, orientation):
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
                x = x2
                y = y2
            else:
                if 0 <= orientation < np.pi / 2:
                    if i == 0 or i == 1:
                        x = x2 - x_offsets[i]
                        y = y2 + y_offsets[i]
                    if i == 3 or i == 4:
                        x = x2 + x_offsets[i]
                        y = y2 - y_offsets[i]
                elif np.pi / 2 <= orientation < np.pi:
                    if i == 0 or i == 1:
                        x = x2 - x_offsets[i]
                        y = y2 - y_offsets[i]
                    if i == 3 or i == 4:
                        x = x2 + x_offsets[i]
                        y = y2 + y_offsets[i]
                elif np.pi <= orientation < 3 * np.pi / 2:
                    if i == 0 or i == 1:
                        x = x2 + x_offsets[i]
                        y = y2 - y_offsets[i]
                    if i == 3 or i == 4:
                        x = x2 - x_offsets[i]
                        y = y2 + y_offsets[i]
                elif 3 * np.pi / 2 <= orientation < 2 * np.pi:
                    if i == 0 or i == 1:
                        x = x2 + x_offsets[i]
                        y = y2 + y_offsets[i]
                    if i == 3 or i == 4:
                        x = x2 - x_offsets[i]
                        y = y2 - y_offsets[i]

            self.sensor_state[i] = self._map.peek(int(round(x)), int(round(y)))
            self.x_pos[i] = x
            self.y_pos[i] = y


class DistanceSensor:
    distance = 9999999999  # temporaire -> va être initialisé à 0 et updaté dans get_distance()
    slowing_distance = 70  # doit être changé par le bonne valeur
    stopping_distance = 27  # doit être changé par la bonne valeur

    def __init__(self, position, map):
        self.position = position
        self.map = map

    def check_sensor(self, orientation):
        x = np.array([self.position.x, self.position.y])
        y = np.argwhere(self.map._map == 2)

        distance_min = self.distance
        if y.any():
            vals = []

            angle = int(np.rad2deg(orientation))
            min_angle = angle - 15 + 90
            max_angle = angle + 16 + 90

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
                            distance_min = dist

        self.distance = distance_min
