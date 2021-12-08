class Car:
    car_obj = None
    acceleration = 0
    current_radius = 0
    obstacle_bypass = None

    def __init__(self, map, x=0, y=0, orientation=0, speed_factor=0, refresh_rate=24, length=0.267, width=0.1,
                 height=0.1):
        """
        :param map: Map object containing a 2d map of the trajectory
        :param x: initial x position of the car
        :param y: initial y position of the car
        :param orientation: initial orientation of the car in radiant
        :param speed_factor: initial speed of the car in cm/s
        :param refresh_rate: blender's refresh rate
        :param length: car's length
        :param width: car's width
        :param height: car's height
        """
        self.position = Position(x, y)
        self.orientation = orientation
        self.speed_factor = speed_factor
        self.refresh_rate = refresh_rate
        self.length = length
        self.width = width
        self.height = height
        self.speed = (self.speed_factor / 100) / (1 / self.refresh_rate)
        self.line_follower = LineFollower(self.position, map, self.length / 2 * 100 + 2)
        self.distance_sensor = DistanceSensor(self.position, map)

    def update_position(self):
        """
        Updates the car position for each frame.
        """
        self.line_follower.check_sensors(self.orientation)
        self.distance_sensor.check_sensor(self.orientation)

        # check the line followers sensor to see if it's the end of the track
        num_on_sensors = np.sum(self.line_follower.sensor_state)
        if num_on_sensors <= 3:
            # used in the bypassing sequence
            overridden_speed_factor = None

            if self.obstacle_bypass is None:
                self.check_bypass()
                next_orientation = self.get_next_orientation()
            else:
                overridden_speed_factor, next_orientation = self.obstacle_bypass.sequence(self.position, self.orientation,
                                                                                          self.speed_factor,
                                                                                          self.distance_sensor.distance)
                # if the line follower see a line and it's the final bypass stage, the sequence is finished
                if self.obstacle_bypass.stage == 7 and 1 in self.line_follower.sensor_state:
                    self.obstacle_bypass = None

            if overridden_speed_factor is None:
                self.update_speed_factor()
            else:
                self.speed_factor = overridden_speed_factor

            self.current_radius = self.get_turn_radius(next_orientation)
        else:
            self.speed_factor = 0
            next_orientation = self.orientation

        self.orientation = self.normalize_angle(next_orientation)
        self.position.x = self.position.x + self.speed_factor * np.cos(self.orientation)
        self.position.y = self.position.y + self.speed_factor * np.sin(self.orientation)

    def check_bypass(self):
        """
        Creates a ObstacleBypass object if the car needs to bypass an obstacle.
        :return:
        """
        if self.distance_sensor.distance <= self.distance_sensor.stopping_distance:
            self.obstacle_bypass = ObstacleBypass(self.position, self.orientation, self.refresh_rate)

    def get_next_orientation(self):
        """
        Computes the next orientation depending on the line follower sensors reading.
        :return: next car's orientation
        """
        # ss -> sensor_state
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
            # since there is not any active sensor, last_sensor has to stay the same
            pass

        return round(next_orientation, 4)

    def update_speed_factor(self):
        """
        Updates the car's speed_factor depending on the distance sensor reading.

        The car will accelerate until it reaches its top speed or the
        distance until the next obstacle is under the stopping distance.
        """
        dist = self.distance_sensor.distance
        stop_dist = self.distance_sensor.stopping_distance

        if dist < stop_dist:
            # stop
            self.speed_factor = 0
        elif stop_dist < dist < 1.2*stop_dist:
            # slow down
            if (self.speed_factor-0.05) > 0:
                self.speed_factor -= 0.05
        elif dist > stop_dist:
            # accelerate to max speed
            if self.speed_factor < 0.70: # 70% of max speed
                self.speed_factor += 0.1

        self.speed_factor = round(self.speed_factor, 4)

    def get_turn_radius(self, next_orientation):
        """
        Computes the car's current turning radius based on previous orientation, next orientation and position.
        :param next_orientation: car's next orientation
        :return: car's current turning radius
        """
        x1 = self.position.x
        x2 = self.position.x + self.speed_factor * np.cos(next_orientation)
        y1 = self.position.y
        y2 = self.position.y + self.speed_factor * np.sin(next_orientation)

        delta_s = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        delta_theta = np.abs(self.orientation - next_orientation)
        return (delta_s / delta_theta) / 100

    def normalize_angle(self, angle):
        """
        Keeps the car's orientation between 0 and 2pi.
        :param angle: angle in rad
        :return: normalized angle in rad
        """
        if angle > 2 * np.pi:
            angle -= 2 * np.pi
        if angle < 0:
            angle += 2 * np.pi
        return angle

    def blender_init(self):
        """
        Creates the car object and sensors in blender.
        """
        try:
            self.car_obj = bpy.data.objects['Car']
        except:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(self.position.x, self.position.y, self.height / 2),
                                            rotation=(0, 0, self.orientation),
                                            scale=(self.length, self.width, self.height))
            bpy.context.active_object.name = 'Car'
            self.car_obj = bpy.data.objects['Car']

        self.line_follower.blender_init()

    def blender_update(self):
        """
        Updates the car's object and sensors in blender with the updated position and orientation.

        Also computes the car's speed and acceleration.
        """
        self.update_position()
        self.car_obj.location[0] = self.position.x / 100
        self.car_obj.location[1] = self.position.y / 100
        self.car_obj.rotation_euler[2] = self.orientation
        old_speed = self.speed
        self.speed = (self.speed_factor / 100) / (1 / self.refresh_rate)
        self.acceleration = (self.speed - old_speed) / (1 / self.refresh_rate)

        self.line_follower.blender_update()


class LineFollower:
    line_follower_obj = []
    sensor_state = [0] * 5
    x_pos = [0] * 5
    y_pos = [0] * 5
    last_sensor = None

    def __init__(self, position, map, position_offset=0.0):
        """
        :param position: Position object containg the coordinates of the car
        :param map: Map object containing a 2d map of the trajectory
        :param position_offset: position offset for the line follower sensors (offset from the car)
        """
        self.position = position
        self.map = map
        self.position_offset = position_offset

    def blender_init(self):
        """
        Initialise the line follower sensors in blender
        """
        for i in range(5):
            bpy.ops.mesh.primitive_cube_add(size=0.01, location=(self.position.x, self.position.y + (i - 2) / 100, 0),
                                            rotation=(0, 0, 0))
            bpy.context.active_object.name = f'suiveur_ligne{i}'
            self.line_follower_obj += [bpy.data.objects[f'suiveur_ligne{i}']]

    def blender_update(self):
        """
        Updates the sensor's position in blender
        :return:
        """
        for i in range(5):
            self.line_follower_obj[i].location[0] = self.x_pos[i] / 100
            self.line_follower_obj[i].location[1] = self.y_pos[i] / 100

    def check_sensors(self, orientation):
        """
        Gets the line follower sensor's state
        :param orientation: current car orientation
        :return: list containing the 5 sensor's state
        """

        #  phi is the angle between the current quadrant right most border and the car orientation
        if 0 <= orientation < np.pi / 2:
            phi = orientation
        elif np.pi / 2 <= orientation < np.pi:
            phi = np.pi - orientation
        elif np.pi <= orientation < 3 * np.pi / 2:
            phi = orientation - np.pi
        elif 3 * np.pi / 2 <= orientation < 2 * np.pi:
            phi = -orientation
        else:
            print(f'orientation should never be this value: {orientation}')

        # position of every sensor
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

            # peeks the map at the current sensor's position. If the map contains a 1, there's a line under the sensor.
            self.sensor_state[i] = self.map.peek(int(round(x)), int(round(y)))
            self.x_pos[i] = x
            self.y_pos[i] = y


class DistanceSensor:
    distance = 9999999
    #(car+ obstacle)/2 +10cm because the positions are in the middle
    stopping_distance = 27

    def __init__(self, position, map):
        self.position = position
        self.map = map

    def check_sensor(self, orientation):
        #car position
        x = np.array([self.position.x, self.position.y])
        #obstacles positions
        y = np.argwhere(self.map._map == 2)

        #reset of the last seen distance
        distance_min = 9999999
        if y.any():
            vals = []
            angle = int(np.rad2deg(orientation))

            #sensor looks in a ray of 30 degrees
            min_angle = angle - 15
            max_angle = angle + 16

            for phi in range(min_angle, max_angle):
                yy = y
                for val in yy:
                    val = list(val)
                    #conditions to exclude obstacles behind the car
                    if 0 < phi < 90:
                        if (val[0] > x[0]) and (val[1] > x[1]):
                            if val not in vals:
                                vals += [val]

                    if 90 < phi < 180:
                        if val[0] < x[0] and val[1] > x[1]:
                            if val not in vals:
                                vals += [val]

                    if 180 < phi < 270:
                        if val[0] < x[0] and val[1] < x[1]:
                            if val not in vals:
                                vals += [val]

                    if 270 < phi < 360:
                        if val[0] > x[0] and val[1] < x[1]:
                            if val not in vals:
                                vals += [val]

                    if phi == 0 or phi == 360:
                        if val[1] == x[1] and val[0] > x[0]:
                            if val not in vals:
                                vals += [val]
                    if phi == 90:
                        if val[1] > x[1] and val[0] == x[0]:
                            if val not in vals:
                                vals += [val]

                    if phi == 180:
                        if val[0] < x[0] and val[1] == x[1]:
                            if val not in vals:
                                vals += [val]
                    if phi == 270:
                        if val[1] < x[1] and val[0] == x[0]:
                            if val not in vals:
                                vals += [val]

            if np.array(vals).any():
                dd = np.array(vals) - x
                for phi in range(min_angle, max_angle):
                    #find obstacles on the ray with normal vectors
                    on_ray = np.abs(dd @ (np.sin(np.deg2rad(-phi)), np.cos(np.deg2rad(-phi)))) < np.sqrt(0.5)

                    if any(on_ray):
                        vals = np.array(vals)
                        #coordinates of the nearest obstacle on the ray
                        ymin = vals[on_ray][np.argmin(np.einsum('ij,ij->i', dd[on_ray], dd[on_ray]))]
                        dist = np.sqrt((x[0] - ymin[0]) ** 2 + (x[1] - ymin[1]) ** 2)
                        if distance_min >= dist:
                            distance_min = dist
        #add errors of the real sensor - equation found with excel and distribution values
        if distance_min is not 9999999:
            distance_min = 0.9974*distance_min-0.9919
        self.distance = distance_min


class ObstacleBypass:
    stage = 1
    next_stage_orientation = 0
    wait_counter = 0
    next_stage_orientation_start = 0

    def __init__(self, starting_position, starting_orientation, refresh_rate):
        """
        :param starting_position: car's starting position
        :param starting_orientation: car's startgin orientation
        :param refresh_rate: blender's refresh rate
        """
        self.starting_orientation = starting_orientation
        self.refresh_rate = refresh_rate
        self.next_stage_position_x = starting_position.x - 20 * np.cos(starting_orientation)
        self.next_stage_position_y = starting_position.y - 20 * np.sin(starting_orientation)

    def sequence(self, position, orientation, speed_factor, next_obstacle_distance):
        """
        There's a total of 7 stage. Each stages correspond to a bypass step.
        :param position: current car's position
        :param orientation: current car's orientation
        :param speed_factor: current car's speed factor
        :param next_obstacle_distance: current distance sensor's reading
        :return: overridden_speed (if any), next car's orientation
        """
        overridden_speed_factor = None
        if self.stage == 1:
            self.wait_counter += 1
            overridden_speed_factor = 0
            if self.wait_counter > 5 / (1 / self.refresh_rate):
                overridden_speed_factor = -0.3
                self.stage += 1

        elif self.stage == 2:
            if self.next_stage_position_x - 2 < position.x < self.next_stage_position_x + 2 and self.next_stage_position_y - 2 < position.y < self.next_stage_position_y + 2:
                self.stage += 1
            else:
                overridden_speed_factor = -0.3

        elif self.stage == 3:
            self.next_stage_orientation_start = orientation
            self.stage += 1

        elif self.stage == 4:
            if speed_factor > 0:
                orientation += 0.04
            if next_obstacle_distance > 99999:
                hypotenus = 30 / np.cos(orientation - self.next_stage_orientation_start)
                self.next_stage_position_x = position.x + hypotenus * np.cos(orientation)
                self.next_stage_position_y = position.y + hypotenus * np.sin(orientation)
                self.stage += 1

        elif self.stage == 5:
            if self.next_stage_position_x - 0.5 < position.x < self.next_stage_position_x + 0.5 or self.next_stage_position_y - 0.5 < position.y < self.next_stage_position_y + 0.5:
                self.next_stage_orientation = orientation - 0.707
                self.stage += 1

        elif self.stage == 6:
            orientation -= 0.04
            if orientation < self.next_stage_orientation:
                self.stage += 1

        elif self.stage == 7:
            pass

        return overridden_speed_factor, orientation