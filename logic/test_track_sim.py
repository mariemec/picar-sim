m, n = 300, 300
segs = []

# Test 1 -> ligne droite
segs.append(Line((0, 0), (100, 0)))
segs.append(Line((100, -5), (100, 5)))

# Test 2 -> cercle
segs.append(Curve((13.8, 13.8), 13.8, 0, math.pi * 2))

# Test 3 -> angle droit
segs.append(Line((0, 0), (100, 0)))
segs.append(Line((100, 0), (100, 100)))

# Test 4 -> cercle serré
segs.append(Curve((12, 12), 12, 0, math.pi * 2))
sim = Simulation(m, n, segs)

# Test 5 -> ligne droite en reculant
segs.append(Line((0, 0), (200, 0)))

# Test 6 -> ligne droite avec obstacle
segs.append(Line((0, 0), (200, 0)))
segs.append(Obstacle((100,0), 0))

# Test 7 -> Cercle avec obstacle
segs.append(Curve((13.8, 13.8), 13.8, 0, math.pi * 2))
segs.append(Obstacle((27.6,13.8), 90))

# Test 8 -> cercle serré avec obstacle
segs.append(Curve((12, 12), 12, 0, math.pi * 2))
segs.append(Obstacle((24,12), 90))

# Test 9 -> angle droit
segs.append(Line((0, 0), (100, 0)))
segs.append(Line((100, 0), (100, 100)))
segs.append(Obstacle((100, 0), 0))

sim = Simulation(m, n, segs)
sim.trajectory.map.print_map_to_file()
sim.run()
