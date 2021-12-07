import numpy as np

class error_generator:
    mean = dict([
        (10,9.16),
        (20,19.06),
        (30,29.07),
        (40,38.53),
        (50,48.36),
        (60,58.31),
        (70,69.22),
        (80,79.29)
    ])
    std_dev = dict([
        (10, 0.32),
        (20, 0.06),
        (30, 0.09),
        (40, 0.12),
        (50, 0.27),
        (60, 0.34),
        (70, 0.25),
        (80, 0.31)
    ])
    def add_error(self, distance):
        distance = np.round(distance/10, 0)*10
        np.random.normal(mean[distance], std_dev[distance]**2)
        ##yooooo fuck ça on fait une regression lineaire
