from trajectoire import *
from car import Car


class Simulation:
    def __init__(self):
        self.trajectoire = Trajectoire(m=100, n=100, segments=[Droite((0, 0), (99, 99))])
        self.car = Car(self.trajectoire.map)
