# -------------------- TRAJECTOIRE --------------------
# V_0
# ---- TODO ----
# - Orientation obstacle
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
            coords_to_activate, valeur = seg.generate_path()
            seg.draw()
            myMap.activate_segment(coords_to_activate, valeur)
        return myMap

    def peek(self, x, y):
        return self.map.peek(x, y)

    def show(self):
        return self.map.show()


class Map:

    def __init__(self, m, n):
        self._map = np.zeros(shape=(m, n), dtype=int)

    def activate_segment(self, coords_to_activate, valeur):
        for x, y in coords_to_activate:
            self._map[int(x)][int(y)] = valeur

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
        self.longueur = (np.sqrt( (self.x_end - self.x_start)**2 + (self.y_end - self.y_start)**2 )/100)
    
    def slope(self):
        if self.x_end != self.x_start:
            slope = (self.y_end - self.y_start) / (self.x_end - self.x_start)
        else:
            slope = 1000
        return slope
    
    def angle(self):
        angle = np.arctan(self.slope())
        return angle

    def slope(self):
        if self.x_end != self.x_start:
            slope = (self.y_end - self.y_start) / (self.x_end - self.x_start)
        else:
            slope = 1000
        return slope

    def angle(self):
        angle = np.arctan(self.slope())
        return angle

    def generate_path(self):
        slope = self.slope()
        path_coords = list()
        if slope == 1000:
            if self.y_start < self.y_end:
                for i in range(self.y_start, self.y_end):
                    path_coords.append((self.x_start, self.y_start + i))
            else:
                for i in range(self.y_end, self.y_start):
                    path_coords.append((self.x_start, self.y_end + i))
        else:
            b = self.y_start - self.x_start * slope
            for i, x in enumerate(range(self.x_start, self.x_end + 1, 1)):
                y = slope * x + b
                path_coords.append((x, y))
        return path_coords, 1
    
    def draw(self):
        # Division par 100 pour mettre en cm
        bpy.ops.mesh.primitive_plane_add(size=1.0, calc_uvs=True, enter_editmode=False, 
            align='WORLD', location=((self.x_start+self.deltaX/2)/100, (self.y_start+self.deltaY/2)/100, 0.0), 
            rotation=(0.0, 0.0, self.angle()), scale=(1.0, 1.0, 1.0))
        
        bpy.context.active_object.dimensions = (self.longueur, 0.018, 0)
        

class Courbe:

    def __init__(self, center_coord, radius, start_angle, end_angle):
        self.center_x, self.center_y = center_coord
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        #self.deltaX = self.x_end - self.x_start
        #self.deltaY = self.y_end - self.y_start
        #self.longueur = np.sqrt( (self.x_end - self.x_start)**2 + (self.y_end - self.y_start)**2 )

    def generate_path(self, float=0):
        path_coords = list()
        if self.start_angle > self.end_angle:
            raise ValueError('Start angle of curve must be smaller than end angle')

        for theta in np.arange(self.start_angle, self.end_angle, 0.05):
            x = self.radius * math.cos(theta)
            y = self.radius * math.sin(theta)
            if float == 0:
                path_coords.append((self.center_x + int(x), self.center_y + int(y)))
        
            else:
                path_coords.append((self.center_x + x, self.center_y + y))
                
        return path_coords, 1

    def draw(self):
        path_coords = self.generate_path(1)[0]
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        
        for i, c in enumerate(path_coords):
            # Division par 100 pour mettre en cm
            print(i)
            if c != (path_coords[-1]):
                x1 = (path_coords[i][0])/100
                x2 = (path_coords[i+1][0])/100
                y1 = (path_coords[i][1])/100
                y2 = (path_coords[i+1][1])/100
            
            longueur = np.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
            slope = (y2 - y1) / (x2 - x1)
            angle = np.arctan(slope)
            print(c[0])
            print(c[1])
            
            bpy.ops.mesh.primitive_plane_add(size=0.5, calc_uvs=True, enter_editmode=False, 
            align='WORLD', location=(c[0]/100, c[1]/100, 0.0), 
            rotation=(0.0, 0.0, angle), scale=(1.0, 1.0, 1.0))
            
            bpy.context.active_object.dimensions = (longueur, 0.018, 0)
            

class Obstacle:
    
    def __init__(self, start_coord, angle):
        self.x, self.y = start_coord
        self.angle = angle * math.pi
        self.size = 0.01
        self.hauteur = 0.115
        self.largeur = 0.075
        self.profondeur = 0.064
        
    def generate_path(self):
        path_coords = list()
        path_coords.append((self.x, self.y ))
        return path_coords, 2
    
    def draw(self):
        bpy.ops.mesh.primitive_cube_add(size=self.size, calc_uvs=True, enter_editmode=False, 
        align='WORLD', location=((self.x)/100, (self.y)/100, self.hauteur/2), 
        rotation=(0.0, 0.0, self.angle), scale=(1.0, 1.0, 1.0))
        
        bpy.context.active_object.dimensions = (self.profondeur, self.largeur, self.hauteur)
    
   
if __name__ == '__main__':
    segs = list()
    #segs.append(Droite((0, 0), (10, 0)))
    #segs.append(Droite((0, 0), (10, 0)))
    #segs.append(Courbe((10, 12), 12, math.pi*3/2, math.pi*8/4))
    #segs.append(Obstacle((10, 0), 0))
    #segs.append(Courbe((5, 5), 12, math.pi*3/2, math.pi*7/4))
    #segs.append(Droite((8, 1), (14, 7)))
    #segs.append(Courbe((11.7, 9), 3 ,math.pi*7/4, math.pi/2+2*math.pi))
    #segs.append(Droite((12, 12), (4, 12)))
    #segs.append(Courbe((4, 11), 1 , math.pi/2, math.pi*3/2))
    #segs.append(Droite((4, 10), (8, 10)))
    
    t = Trajectoire(segs, 40, 40)
    t.show()

