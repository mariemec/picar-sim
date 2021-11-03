# -------------------- TRAJECTOIRE --------------------
# V_0
# ---- TODO ----
# - Curve
# - Orientation obstacle
# - Ajouter une condition pour éviter les division par zéro dans les slopes
# - Refactoring 



import numpy as np
import math
import bpy
from bpy import context, data, ops

class Trajectoire:

    def __init__(self, segments, m, n):
        self.segments = segments
        self.map = self.generate_map(self.segments, m, n)

    def generate_map(self, segments, m, n):
        myMap = Map(m, n)
        for seg in segments:
            coords_to_activate = seg.generate_path()
            seg.draw()
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
        self.deltaX = self.x_end - self.x_start
        self.deltaY = self.y_end - self.y_start
        self.longueur = np.sqrt( (self.x_end - self.x_start)**2 + (self.y_end - self.y_start)**2 )
    
    def slope(self):
        slope = (self.y_end - self.y_start) / (self.x_end - self.x_start)
        return slope
    
    def angle(self):
        angle = np.arctan(self.slope())
        return angle

    def generate_path(self):
        slope = self.slope()
        b = self.y_start - self.x_start * slope

        path_coords = list()
        for x in range(self.x_start, self.x_end + 1, 1):
            y = slope * x + b
            path_coords.append((x, int(y)))

        return path_coords
    
    def draw(self):
        
        bpy.ops.mesh.primitive_plane_add(size=1.0, calc_uvs=True, enter_editmode=False, 
            align='WORLD', location=(self.x_start+self.deltaX/2, self.y_start+self.deltaY/2, 0.0), 
            rotation=(0.0, 0.0, self.angle()), scale=(1.0, 1.0, 1.0))
        
        bpy.context.active_object.dimensions = (self.longueur, 0.18, 0)
        



class Courbe:

    def __init__(self, center_coord, radius, start_angle, end_angle):
        self.center_x, self.center_y = center_coord
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        #self.deltaX = self.x_end - self.x_start
        #self.deltaY = self.y_end - self.y_start
        #self.longueur = np.sqrt( (self.x_end - self.x_start)**2 + (self.y_end - self.y_start)**2 )

    def generate_path(self):
        path_coords = list()
        if self.start_angle > self.end_angle:
            raise ValueError('Start angle of curve must be smaller than end angle')

        for theta in np.arange(self.start_angle, self.end_angle, 0.1):
            x = self.radius * math.cos(theta)
            y = self.radius * math.sin(theta)
            path_coords.append((self.center_x + int(x), self.center_y + int(y)))

        return path_coords
    
    def draw(self):
        bpy.ops.mesh.primitive_plane_add(size=1.0, calc_uvs=True, enter_editmode=False, 
            align='WORLD', location=(0, 0, 0.0), 
            rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
        
        bpy.context.active_object.dimensions = (1, 0.18, 0)
        
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].fit_type = 'FIT_CURVE'
        
        bpy.ops.curve.primitive_bezier_curve_add(radius=2.0, enter_editmode=False, align='WORLD', 
            location=(0.0, 0.0, 0.0), scale=(1, 1, 1))
            
        bpy.context.object.modifiers["Array"].curve = bpy.data.objects["BezierCurve"]
        


class Obstacle:
    
    def __init__(self, start_coord, end_coord):
        self.x_start, self.y_start = start_coord
        self.x_end, self.y_end = end_coord
        self.deltaX = self.x_end - self.x_start
        self.deltaY = self.y_end - self.y_start
        self.longueur = np.sqrt( (self.x_end - self.x_start)**2 + (self.y_end - self.y_start)**2 )
        self.size = 1.0
    
    def slope(self):
        slope = (self.y_end - self.y_start) / (self.x_end - self.x_start)
        return slope
    
    def angle(self):
        angle = np.arctan(self.slope())
        return angle
        
    def generate_path(self):
        slope = (self.y_end - self.y_start) / (self.x_end - self.x_start)  # slope of segment
        b = self.y_start - self.x_start * slope
        
        path_coords = list()
        for x in range(self.x_start, self.x_end + 1, 1):
            y = slope * x + b
            path_coords.append((x, int(y)))

        return path_coords
    
    def draw(self):
        bpy.ops.mesh.primitive_cube_add(size=self.size, calc_uvs=True, enter_editmode=False, 
        align='WORLD', location=(self.x_start+self.deltaX/2, self.y_start+self.deltaY/2, self.size/2), 
        rotation=(0.0, 0.0, self.angle()), scale=(1.0, 1.0, 1.0))
    
    

if __name__ == '__main__':
    segs = list()
    #segs.append(Obstacle((0, 0),(1, 1)))
    segs.append(Droite((0, 0), (5, 5)))
    segs.append(Droite((5, 5), (6, 2)))
    segs.append(Obstacle((6, 2),(7, 1)))
    #segs.append(Droite((0, 0), (5, 5)))
    #segs.append(Courbe((10, 5), 5, math.pi, math.pi * 2))
    
    t = Trajectoire(segs, 20, 20)
    t.show()

