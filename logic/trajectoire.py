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
        slope = (self.y_end-self.y_start)/(self.x_end-self.x_start) # slope of segment
        b = self.y_start-self.x_start*slope

        path_coords = list()
        for x in range(self.x_start, self.x_end+1, 1):
            y = slope*x+b
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
            x = self.radius*math.cos(theta)
            y = self.radius*math.sin(theta)
            path_coords.append((self.center_x+int(x), self.center_y+int(y)))

        return path_coords

if __name__ == '__main__':
    segs = list()
    segs.append(Droite((0, 0), (5, 5)))
    segs.append(Courbe((10, 5), 5, math.pi, math.pi*2))
    t = Trajectoire(segs, 20, 20)
    t.show()

