# ----------------------- BILLE -----------------------


class Bille:

    def __init__(self, theta=0, x=0, y=0):
        self.mass = 0.005
        self.radius_bille = 0.016
        self.radius_pendule = 0.14
        self.position = Position(x, y)
        self.theta = theta

    def calculate_next_pos(self):
        # TO-DO
        return 0

    def blender_init(self):
        return 0

    def blender_update(self, x, y):
        return 0

# ------------------------ CAR ------------------------
import numpy as np


class Car:
    orientation = 0
    speed_factor = 0

    def __init__(self, map, x=0, y=0):
        self.position = Position(x, y)
        self.line_follower = LineFollower(self.position, map)
        self.distance_sensor = DistanceSensor(self.position, map)

    def calculate_next_pos(self):
        self.orientation = self.line_follower.update_orientation(self.orientation)
        self.speed_factor = self.distance_sensor.update_speed_factor(self.speed_factor)

        self.position.x += self.speed_factor*np.cos(self.orientation)
        self.position.y += self.speed_factor*np.sin(self.orientation)

    def draw(self):
        pass


class LineFollower:
    sensor_state = [False]*5

    def __init__(self, position, map):
        self.position = position
        self.map = map

    def get_state(self):
        for i in range(len(self.sensor_state)):
            self.sensor_state[i] = simulation.trajectoire.peak(self.position)

    def update_orientation(self, orientation):
        if self.sensor_state[0]:
            # tourne beaucoup à gauche
            orientation -= 0.2
        elif self.sensor_state[4]:
            # tourne beaucoup à droite
            orientation += 0.2
        elif self.sensor_state[1]:
            # tourne à gauche
            orientation -= 0.1
        elif self.sensor_state[3]:
            # tourne à droite
            orientation += 0.1
        elif self.sensor_state[2]:
            # you're good
            orientation = orientation
        else:
            orientation -= 0

        return round(orientation, 4)


class DistanceSensor:
    distance = 10
    slowing_distance = 1
    stopping_distance = 0.1

    def __init__(self, position, map):
        self.position = position
        self.map = map

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

# -------------------- POSITION --------------------
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
# -------------------- TRAJECTOIRE --------------------
import numpy as np
import math


class Trajectoire:

    def __init__(self, segments, m, n):
        self.segments = segments
        self.map = self.generate_map(self.segments, m, n)

    def generate_map(self, segments, m, n):
        myMap = Map(m, n)
        for seg in segments:
            coords_to_activate = seg.generate_path()
            myMap.activate_segment(coords_to_activate)
        return myMap

    def peek(self, x, y):
        return self.map.peek(x, y)

    def show(self):
        return self.map.show()


class Map:

    def __init__(self, m, n):
        self._map = np.zeros(shape=(m, n), dtype=int)

    def activate_segment(self, coords_to_activate):
        for x, y in coords_to_activate:
            self._map[x][y] = 1

    def peek(self, x, y):
        return self._map[x][y]

    def show(self):
        # matrix coordinates are [i][j], but we've stored data as if it were [x][y]
        rotated = [[self._map[j][i] for j in range(len(self._map))] for i in range(len(self._map[0]) - 1, -1, -1)]
        print('\n'.join([' '.join([f'{item}' for item in row])
                         for row in rotated]))


class Droite:

    def __init__(self, start_coord, end_coord):
        self.x_start, self.y_start = start_coord
        self.x_end, self.y_end = end_coord

    def generate_path(self):
        slope = (self.y_end - self.y_start) / (self.x_end - self.x_start)  # slope of segment
        b = self.y_start - self.x_start * slope

        path_coords = list()
        for x in range(self.x_start, self.x_end + 1, 1):
            y = slope * x + b
            path_coords.append((x, int(y)))

        return path_coords


class Courbe:

    def __init__(self, center_coord, radius, start_angle, end_angle):
        self.center_x, self.center_y = center_coord
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle

    def generate_path(self):
        path_coords = list()
        if self.start_angle > self.end_angle:
            raise ValueError('Start angle of curve must be smaller than end angle')

        for theta in np.arange(self.start_angle, self.end_angle, 0.1):
            x = self.radius * math.cos(theta)
            y = self.radius * math.sin(theta)
            path_coords.append((self.center_x + int(x), self.center_y + int(y)))

        return path_coords


if __name__ == '__main__':
    segs = list()
    segs.append(Droite((0, 0), (5, 5)))
    segs.append(Courbe((10, 5), 5, math.pi, math.pi * 2))
    t = Trajectoire(segs, 20, 20)
    t.show()

class Simulation(object):
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.__init__(*args, **kwds)
        return it

    def __init__(self, *args, **kwds):
        if 'car' in kwds:
            self.car = kwds['car']
        if 'trajet' in kwds:
            self.trajectoire = kwds['trajectoire']
        if 'bille' in kwds:
            self.bille = kwds['bille']
