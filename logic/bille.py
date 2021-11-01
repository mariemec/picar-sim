# ----------------------- BILLE -----------------------
from position import Position


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

