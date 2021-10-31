import numpy as np

from simulation import Simulation
from position import Position


class Car:
    orientation = 0
    speed_factor = 0

    def __init__(self, x=0, y=0):
        self.position = Position(x, y)
        self.line_follower = LineFollower(self.position)
        self.distance_sensor = DistanceSensor(self.position)

    def calculate_next_pos(self):
        self.orientation = self.line_follower.update_orientation(self.orientation)
        self.speed_factor = self.distance_sensor.update_speed_factor(self.speed_factor)

        self.position.x += self.speed_factor*np.cos(self.orientation)
        self.position.y += self.speed_factor*np.sin(self.orientation)

    def draw(self):
        pass


class LineFollower:
    sensor_state = [False]*5

    def __init__(self, position):
        self.position = position

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


simulation = Simulation(car=Car())
