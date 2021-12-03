m, n = 300, 300
segs = []

# Test 1 -> ligne droite
#segs.append(Droite((0, 0), (200, 0)))
#sim = Simulation(m, n, segs)
#sim.trajectoire.map.print_map_to_file()
#car = sim.car
#car.position.x = 0
#car.position.y = 0
#car.blender_init()

# Test 2 -> cercle
#segs.append(Courbe((13.8, 13.8), 13.8, 0, math.pi * 2))
#sim = Simulation(m, n, segs)
#sim.trajectoire.map.print_map_to_file()
#car = sim.car
#car.position.x = 0.138
#car.position.y = 0
#car.blender_init()

# Test 3 -> angle droit
#segs.append(Droite((0, 0), (100, 0)))
#segs.append(Droite((100, 0), (100, 100)))
#sim = Simulation(m, n, segs)
#sim.trajectoire.map.print_map_to_file()
#car = sim.car
#car.position.x = 0
#car.position.y = 0
#car.blender_init()

# Test 4 -> cercle serré
#segs.append(Courbe((12, 12), 12, 0, math.pi * 2))
#sim = Simulation(m, n, segs)
#sim.trajectoire.map.print_map_to_file()
#car = sim.car
#car.position.x = 0.12
#car.position.y = 0
#car.blender_init()

# Test 5 -> ligne droite en reculant
#segs.append(Droite((0, 0), (200, 0)))
#sim = Simulation(m, n, segs)
#sim.trajectoire.map.print_map_to_file()
#car = sim.car
#car.position.x = 0
#car.position.y = 0
#car.blender_init()

# Test 6 -> ligne droite avec obstacle
#segs.append(Droite((0, 0), (200, 0)))
#segs.append(Obstacle((100,0), 0))
#sim = Simulation(m, n, segs)
#sim.trajectoire.map.print_map_to_file()
#car = sim.car
#car.position.x = 0
#car.position.y = 0
#car.blender_init()

# Test 7 -> Cercle avec obstacle
#segs.append(Courbe((13.8, 13.8), 13.8, 0, math.pi * 2))
#segs.append(Obstacle((27.6,13.8), 90))
#sim = Simulation(m, n, segs)
#sim.trajectoire.map.print_map_to_file()
#car = sim.car
#car.position.x = 13.8
#car.position.y = 0
#car.blender_init()

# Test 8 -> cercle serré avec obstacle
#segs.append(Courbe((12, 12), 12, 0, math.pi * 2))
#segs.append(Obstacle((24,12), 90))
#sim = Simulation(m, n, segs)
#sim.trajectoire.map.print_map_to_file()
#car = sim.car
#car.position.x = 12
#car.position.y = 0
#car.blender_init()

# Test 9 -> angle droit
#segs.append(Droite((0, 0), (100, 0)))
#segs.append(Droite((100, 0), (100, 100)))
#segs.append(Obstacle((100, 0), 0))
#sim = Simulation(m, n, segs)
#sim.trajectoire.map.print_map_to_file()
#car = sim.car
#car.position.x = 0
#car.position.y = 0
#car.blender_init()