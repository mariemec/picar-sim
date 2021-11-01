from trajectoire import *
from car import Car


class Simulation:
    def __init__(self, m, n, segments):
        self.trajectoire = Trajectoire(m=m, n=n, segments=segments)
        self.car = Car(self.trajectoire.map)
