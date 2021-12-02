class Car:
    car_obj = None
    suiveur_ligne_obj = []
    acceleration = 0
    current_radius = 0

    def __init__(self, _map, x=0, y=0, orientation=0, speed_factor=0, refresh_rate=24):
        self.position = Position(x, y)
        self.orientation = orientation
        self.speed_factor = speed_factor
        self.refresh_rate = refresh_rate
        self.speed = (self.speed_factor / 100) / (1 / self.refresh_rate)
        self.line_follower = LineFollower(self.position, _map, self.refresh_rate)
        self.distance_sensor = DistanceSensor(self.position)

    def calculate_next_pos(self):
        orientation, self.current_radius = self.line_follower.update_orientation(self.orientation, self.speed,
                                                                                 self.suiveur_ligne_obj)
        speed_factor = self.distance_sensor.update_speed_factor(self.speed_factor)

        return (self.position.x + speed_factor * np.cos(orientation),
                self.position.y + speed_factor * np.sin(orientation),
                orientation,
                speed_factor)

    def blender_init(self):
        try:
            self.car_obj = bpy.data.objects['Car']
        except:
            bpy.ops.mesh.primitive_cube_add(size=0.1, location=(self.position.x, self.position.y, 0),
                                            rotation=(0, 0, self.orientation), scale=(2, 1, 1))
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
    last_turn_direction = None

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

        x0 = 4 * np.sin(phi)
        x1 = 2 * np.sin(phi)
        x2 = self.position.x
        x3 = 2 * np.sin(phi)
        x4 = 4 * np.sin(phi)
        x_offsets = [x0, x1, x2, x3, x4]

        y0 = 4 * np.cos(phi)
        y1 = 2 * np.cos(phi)
        y2 = self.position.y
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
        temp = orientation
        current_radius = 0
        # get current sensors state
        self.__get_state(orientation, suiveur_ligne_obj)

        # placeholder values, will have to fine tune them
        small_radius = 170 / 1000
        small_turn_delta_orientation = (2 * np.pi) / (
                ((2 * np.pi * small_radius) / current_speed) / (1 / self.refresh_rate)) if current_speed > 0 else 0

        medium_radius = 168 / 1000
        medium_turn_delta_orientation = (2 * np.pi) / (
                ((2 * np.pi * medium_radius) / current_speed) / (1 / self.refresh_rate)) if current_speed > 0 else 0

        big_radius = 166 / 1000
        big_turn_delta_orientation = (2 * np.pi) / (
                ((2 * np.pi * big_radius) / current_speed) / (1 / self.refresh_rate)) if current_speed > 0 else 0

        # depending on which sensor is on, the orientation is going to be updated
        print(self.sensor_state)
        if self.sensor_state[2] == 1:
            # you're good
            if self.sensor_state[1] == 1:
                orientation += big_turn_delta_orientation
                current_radius = big_radius * 100
            elif self.sensor_state[3] == 1:
                orientation -= big_turn_delta_orientation
                current_radius = big_radius * 100
            else:
                orientation = orientation
                self.last_turn_direction = None
        elif self.sensor_state[4] == 1:
            # tourne beaucoup à gauche
            orientation -= small_turn_delta_orientation
            current_radius = small_radius * 100
        elif self.sensor_state[0] == 1:
            # tourne beaucoup à droite
            orientation += small_turn_delta_orientation
            current_radius = small_radius * 100
        elif self.sensor_state[3] == 1:
            # tourne à gauche
            orientation -= medium_turn_delta_orientation
            current_radius = medium_radius * 100
        elif self.sensor_state[1] == 1:
            # tourne à droite
            orientation += medium_turn_delta_orientation
            current_radius = medium_radius * 100
        else:
            # defines what to do when the line follower doesn't see anything
            if self.last_turn_direction == 'gauche':
                orientation -= small_turn_delta_orientation
                current_radius = small_radius
            elif self.last_turn_direction == 'droite':
                orientation += small_turn_delta_orientation
                current_radius = small_radius

        if orientation > 2 * np.pi:
            orientation -= 2 * np.pi
        if orientation < 0:
            orientation += 2 * np.pi

        if temp > orientation:
            self.last_turn_direction = 'gauche'
        elif temp < orientation:
            self.last_turn_direction = 'droite'

        return round(orientation, 4), current_radius


class DistanceSensor:
    distance = 10  # temporaire -> va être initialisé à 0 et updaté dans get_distance()
    slowing_distance = 1  # doit être changé par le bonne valeur
    stopping_distance = 0.1  # doit être changé par la bonne valeur

    def __init__(self, position):
        self.position = position

    def get_distance(self):
        pass

    def update_speed_factor(self, speed_factor):
        if self.distance < self.slowing_distance:
            # ralenti
            speed_factor -= 0.1
            pass
        if self.distance < self.stopping_distance:
            # arret
            speed_factor = 0
            pass
        if self.distance > self.slowing_distance:
            if speed_factor < 1:
                speed_factor += 0.1

        return round(speed_factor, 4)
