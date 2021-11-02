# ------------------------ CAR ------------------------
import bpy
import numpy as np
from position import Position


class Car:
    speed_factor = 0
    car_obj = None

    def __init__(self, _map, x=0, y=0, orientation=0, v_max=0.1, refresh_rate=24):
        self.position = Position(x, y)
        self.orientation = orientation
        self.line_follower = LineFollower(self.position, _map, v_max, refresh_rate)
        self.distance_sensor = DistanceSensor(self.position)

    def calculate_next_pos(self):
        orientation = self.line_follower.update_orientation(self.orientation)
        speed_factor = self.distance_sensor.update_speed_factor(self.speed_factor)

        return speed_factor * np.cos(orientation), speed_factor*np.sin(orientation), orientation, speed_factor

    def blender_init(self):
        bpy.ops.mesh.primitive_cube_add(location=(self.position.x, self.position.y, 0), rotation=(0, 0, self.orientation))
        bpy.context.active_object.name = 'Car'
        self.car_obj = bpy.data.objects['Car']

    def blender_update(self):
        self.position.x, self.position.y, self.orientation, self.speed_factor = self.calculate_next_pos()
        self.car_obj.location = self.position
        self.car_obj.rotation_euler = self.orientation


class LineFollower:
    sensor_state = [False]*5

    def __init__(self, position, _map, v_max, refresh_rate):
        self.position = position
        self._map = _map
        self.v_max = v_max
        self.refresh_rate = refresh_rate

    def get_state(self, orientation):
        for i in range(len(self.sensor_state)):
            offset_x = round((2*i) * np.cos(orientation), 0)
            offset_y = round((2*i) * np.sin(orientation), 0)
            self.sensor_state[i] = self._map.peek(self.position.x + offset_x, self.position.y + offset_y)

    def update_orientation(self, orientation):
        # changement d'orientation selon la (vitesse max * le temps d'un frame) / le rayon du cercle que la voiture va effectuer
        if self.sensor_state[0]:
            # tourne beaucoup à gauche
            orientation -= (self.v_max * (1 / self.refresh_rate))/0.012
        elif self.sensor_state[4]:
            # tourne beaucoup à droite
            orientation += (self.v_max * (1 / self.refresh_rate))/0.012
        elif self.sensor_state[1]:
            # tourne à gauche
            orientation -= (self.v_max * (1 / self.refresh_rate))/0.015
        elif self.sensor_state[3]:
            # tourne à droite
            orientation += (self.v_max * (1 / self.refresh_rate))/0.015
        elif self.sensor_state[2]:
            # you're good
            orientation = orientation
        else:
            orientation -= (self.v_max * (1 / self.refresh_rate))/0.012

        return round(orientation, 4)


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

