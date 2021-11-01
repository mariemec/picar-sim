import logging

from simulation import Simulation


"""
To run test use 
>>> pytest --log-cli-level=DEBUG
"""


def test_line_follower():
    car = Simulation().car
    orientation = car.orientation
    logging.info(f'orientation début: {car.orientation}')

    car.line_follower.sensor_state[2] = True
    car.orientation = car.line_follower.update_orientation(car.orientation)
    car.line_follower.sensor_state[2] = False
    logging.info(f'orientation update: {car.orientation}')

    car.line_follower.sensor_state[0] = True
    car.orientation = car.line_follower.update_orientation(car.orientation)
    car.line_follower.sensor_state[0] = False
    logging.info(f'orientation update: {car.orientation}')

    car.line_follower.sensor_state[1] = True
    car.orientation = car.line_follower.update_orientation(car.orientation)
    car.line_follower.sensor_state[1] = False
    logging.info(f'orientation update: {car.orientation}')

    car.line_follower.sensor_state[3] = True
    car.orientation = car.line_follower.update_orientation(car.orientation)
    car.line_follower.sensor_state[3] = False
    logging.info(f'orientation update: {car.orientation}')

    car.line_follower.sensor_state[4] = True
    car.orientation = car.line_follower.update_orientation(car.orientation)
    car.line_follower.sensor_state[4] = False

    logging.info(f'sensor_state: {car.line_follower.sensor_state}')
    assert(orientation == round(car.orientation, 4))


def test_distance_sensor():
    car = Simulation().car
    for i in range(12):
        car.speed_factor = car.distance_sensor.update_speed_factor(car.speed_factor)
        logging.info(car.speed_factor)






