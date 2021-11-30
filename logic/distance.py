import numpy as np

a = """
0000000000000000000000000000
0000000000000000000000000000
0000000000000000000000000000
0000000000000001000000000000
0000000000000000000000000000
000000000000001X100010000000
0000000000000001000000000000
0000000000000001000000000000
0000000000000001000000000000
"""

a = np.array([[int(i) for i in row] for row in a.strip().replace('X', '2').split()], dtype=np.uint8)

x = np.argwhere(a == 2)[0]
y = np.argwhere(a == 1)
d = y - x

min = 9999999999
coord = []

# print(y[0], y[1], y[2])

angle = 180  # 255 has no solutions

vals = []
for phi in range(90, angle+1):
    yy = y
    for val in yy:
        val = list(val)
        if 0 < phi < 90:
            if (val[0] < x[0]) and (val[1] > x[1]):
                if val not in vals:
                    vals += [val]

        if 90 < phi < 180:
            if val[0] > x[0] and val[1] < x[1]:
                if val not in vals:
                    vals += [val]

        if 180 < phi < 270:
            if val[0] > x[0] and val[1] > x[1]:
                if val not in vals:
                    vals += [val]

        if 180 < phi < 270:
            if val[0] < x[0] and val[1] > x[1]:
                if val not in vals:
                    vals += [val]

        if phi == 0 or phi == 360:
            if val[0] == x[0] and val[1] > x[1]:
                if val not in vals:
                    vals += [val]
        if phi == 90:
            if val[1] == x[1] and val[0] < x[0]:
                if val not in vals:
                    vals += [val]

        if phi == 180:
            if val[0] == x[0] and val[1] < x[1]:
                if val not in vals:
                    vals += [val]
        if phi == 270:
            if val[1] == x[1] and val[0] > x[0]:
                if val not in vals:
                    vals += [val]


dd = np.array(vals) - x

for phi in range(0, angle):
    on_ray = np.abs(dd @ (np.sin(np.deg2rad(-phi - 90)), np.cos(np.deg2rad(-phi - 90)))) < np.sqrt(0.5)
    if any(on_ray):
        vals = np.array(vals)
        ymin = vals[on_ray][np.argmin(np.einsum('ij,ij->i', dd[on_ray], dd[on_ray]))]
        dist = np.sqrt((x[0] - ymin[0]) ** 2 + (x[1] - ymin[1]) ** 2)
        if min > dist:
            coord = ymin
            min = dist
print(coord)
