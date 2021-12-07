# -------------------- TRAJECTORY --------------------
# Commented version
# v2.0

class Trajectory:

    def __init__(self, segments, m, n):
        """
        :param segments: Segments of track
        :param m: number of column for map 2D
        :param n: number of row for map 2D
        """
        self.segments = segments
        self.map = self.generate_map(self.segments, m, n)

    def generate_map(self, segments, m, n):
        """
        Generates a 2D map containing track segments and obstacles
        :param segments: Segments of track
        :param m: number of column for map 2D
        :param n: number of row for map 2D
        :return: map 2D (m x n) containing: 0 -> nothing; 1 -> track segment; 2 -> obstacle
        """
        myMap = Map(m, n)
        for seg in segments:
            coords_to_activate, value = seg.generate_path()
            seg.draw()
            myMap.activate_segment(coords_to_activate, value)
        return myMap

    def peek(self, x, y):
        """
        Check coordinate's value
        :param x: column value
        :param y: row value
        :return: number of 0 to 2
        """
        return self.map.peek(x, y)

    def show(self):
        """
        Show's the map
        :return: Print the map in console
        """
        return self.map.show()


class Map:

    def __init__(self, m, n):
        self._map = np.zeros(shape=(m, n), dtype=int)

    def activate_segment(self, coords_to_activate, value):
        """
        Adds 1 or 2 to coordinate
        :param coords_to_activate: (x, y) to activate
        :param value: 1 -> for track ; 2 -> for obstacles;
        :return: adds value to the precise coordinate
        """
        for x, y in coords_to_activate:
            self._map[int(x)][int(y)] = value

    def peek(self, x, y):
        """
        Checks value at the coordinate x, y
        :param x: column value
        :param y: row value
        :return: value of the (x, y) coordinate
        """
        return self._map[x][y]

    def show(self):
        """
        Show the map in console
        :return: map in console
        """
        # matrix coordinates are [i][j], but we've stored data as if it were [x][y]
        rotated = [[self._map[j][i] for j in range(len(self._map))] for i in range(len(self._map[0]) - 1, -1, -1)]
        print('\n'.join([' '.join([f'{item}' for item in row])
                         for row in rotated]))

    def print_map_to_file(self):
        """
        Print map in file
        :return: Map printed
        """
        rotated = [[self._map[j][i] for j in range(len(self._map))] for i in range(len(self._map[0]) - 1, -1, -1)]
        my_track = open("output.txt", "w")
        for row in [' '.join([f'{item}' for item in row]) for row in rotated]:
            my_track.write(f'{row}\n')
        my_track.close()


class Line:

    def __init__(self, start_coord, end_coord):
        self.x_start, self.y_start = start_coord
        self.x_end, self.y_end = end_coord
        self.deltaX = self.x_end - self.x_start
        self.deltaY = self.y_end - self.y_start
        self.longueur = (np.sqrt((self.x_end - self.x_start) ** 2 + (self.y_end - self.y_start) ** 2) / 100)

    def slope(self):
        """
        Determinate the slope between two coordinate
        Slope value is 1000 when line is straight in y
        To dodge the division 0
        :return: slope
        """
        if self.x_end != self.x_start:
            slope = (self.y_end - self.y_start) / (self.x_end - self.x_start)
        else:
            slope = 1000
        return slope

    def angle(self):
        """
        Return angle of slope
        :return: angle
        """
        angle = np.arctan(self.slope())
        return angle

    def generate_path(self):
        """
        Generate coordinates of the line
        :return: path(coordinate) of line
        """
        slope = self.slope()
        path_coords = list()
        if slope == 1000:
            if self.y_start < self.y_end:
                for i in range(0, self.y_end - self.y_start):
                    path_coords.append((self.x_start, self.y_start + i))
                    path_coords.append((self.x_start + 1, self.y_start + i))
            else:
                for i in range(0, self.y_start - self.y_end):
                    path_coords.append((self.x_start, self.y_end + i))
                    path_coords.append((self.x_start + 1, self.y_end + i))
        else:
            b = self.y_start - self.x_start * slope
            if self.x_start < self.x_end:
                for i, x in enumerate(range(self.x_start, self.x_end + 1, 1)):
                    y = slope * x + b
                    path_coords.append((x, y))
                    path_coords.append((x, y + 1))
            else:
                for i, x in enumerate(range(self.x_end, self.x_start + 1, 1)):
                    y = slope * x + b
                    path_coords.append((x, y))
                    path_coords.append((x, y + 1))
        return path_coords, 1

    def draw(self):
        """
        Renders the line in 3D
        Division by 100 to render in cm
        :return: 3D rendered line
        """
        bpy.ops.mesh.primitive_plane_add(size=1.0, calc_uvs=True, enter_editmode=False,
                                         align='WORLD', location=(
            (self.x_start + self.deltaX / 2) / 100, (self.y_start + self.deltaY / 2) / 100, 0.0),
                                         rotation=(0.0, 0.0, self.angle()), scale=(1.0, 1.0, 1.0))

        bpy.context.active_object.dimensions = (self.longueur, 0.018, 0)


class Curve:

    def __init__(self, center_coord, radius, start_angle, end_angle):
        self.center_x, self.center_y = center_coord
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle

    def generate_path(self, float=0):
        """
        Generate coordinates of the curve
        :param float: bool that give the option to cast in int or not
        :return: coordinates of the path
        """
        path_coords = list()
        if self.start_angle > self.end_angle:
            raise ValueError('Start angle of curve must be smaller than end angle')

        for theta in np.arange(self.start_angle, self.end_angle, 0.05):
            x = self.radius * math.cos(theta)
            x_doublon = (self.radius + 1) * math.cos(theta)
            y = self.radius * math.sin(theta)
            y_doublon = (self.radius + 1) * math.sin(theta)

            if float == 0:
                path_coords.append((self.center_x + int(x), self.center_y + int(y)))
                path_coords.append((self.center_x + int(x_doublon), self.center_y + int(y_doublon)))

            else:
                path_coords.append((self.center_x + x, self.center_y + y))

        return path_coords, 1

    def draw(self):
        """
        Renders the curve in 3D
        Renders a multitude of small lines with angles simulating a curve
        Division by 100 to render in cm
        :return: 3D rendered curve
        """
        path_coords = self.generate_path(1)[0]
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0

        for i, c in enumerate(path_coords):
            if c != (path_coords[-1]):
                x1 = (path_coords[i][0]) / 100
                x2 = (path_coords[i + 1][0]) / 100
                y1 = (path_coords[i][1]) / 100
                y2 = (path_coords[i + 1][1]) / 100

            longueur = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            slope = (y2 - y1) / (x2 - x1)
            angle = np.arctan(slope)

            bpy.ops.mesh.primitive_plane_add(size=0.5, calc_uvs=True, enter_editmode=False,
                                             align='WORLD', location=(c[0] / 100, c[1] / 100, 0.0),
                                             rotation=(0.0, 0.0, angle), scale=(1.0, 1.0, 1.0))

            bpy.context.active_object.dimensions = (longueur, 0.018, 0)


class Obstacle:

    def __init__(self, start_coord, angle):
        self.x, self.y = start_coord
        self.angle = angle * math.pi
        self.size = 0.01
        self.height = 0.115
        self.width = 0.075
        self.depth = 0.064

    def generate_path(self):
        """
        Generate coordinates of the obstacle simulating the real dimensions
        :return: coordinates of the obstacle
        """
        path_coords = list()
        path_coords.append((self.x, self.y))
        if self.angle == 0:
            for y in range(self.y - 3, self.y + 3):
                path_coords.append((self.x, y))
        if self.angle == (90 * math.pi):
            for x in range(self.x - 3, self.x + 3):
                path_coords.append((x, self.y))
        return path_coords, 2

    def draw(self):
        """
        Renders the obstacle in 3D
        Division by 100 to render in cm
        :return: 3D rendered obstacle
        """
        bpy.ops.mesh.primitive_cube_add(size=self.size, calc_uvs=True, enter_editmode=False,
                                        align='WORLD', location=((self.x) / 100, (self.y) / 100, self.height / 2),
                                        rotation=(0.0, 0.0, self.angle), scale=(1.0, 1.0, 1.0))

        bpy.context.active_object.dimensions = (self.depth, self.width, self.height)
