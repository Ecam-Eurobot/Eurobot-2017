import logging
import math
import time

from graphmap.map_generator import build_graph
from kinematics import Kinematics
from motors import Motors
from range_sensors import RangeSensor



class Robot:
    _DELAY_OPEN_ClOSE_CLAMP = 0.7
    _DELAY_UP_DOWN_CLAMP = 2.5
    _DELAY_IN_OUT_BLOCK = 3

    # US sensors constants.
    US_SENSORS = [
        {'name': 'front', 'trigger_limit': 10, 'sensors': [0, 1]},
        {'name': 'left', 'trigger_limit': 10, 'sensors': [2]},
        {'name': 'right', 'trigger_limit': 10, 'sensors': [3]},
        {'name': 'back', 'trigger_limit': 5, 'sensors': [4]}
    ]

    DIMENSION = {
        'length': 32.5,
        'width': 19.2
    }

    # Take in count the obstacle dimension (assuming another robot)
    # + the robot size.
    OBSTACLES_DIMENSION = 50

    def __init__(self, position):
        """
        position: init position dict with keys:
            - "angle": a X-axis relative angle.
            - "point": the first position.
        """
        self._position = position

        self._us_sensors = RangeSensor(4)
        self._motors = Motors(5)
        self._kinematic = Kinematics(6)

        logging.info('Building the graph map.')
        robot_diagonal = math.sqrt(self.DIMENSION['length'] + self.DIMENSION['width']**2)
        self._graph = build_graph(robot_diagonal)
        logging.info('Finished to build the graph map.')

    def take_modules(self, number=1, distance=0):
        for i in range(number):
            self._kinematic.release_block()
            self._kinematic.down_clamp()
            time.sleep(self._DELAY_UP_DOWN_CLAMP)
            self._motors.forward(distance)
            while not self._motors.is_done(self.__done_callback):
                time.sleep(0.5)
            self._kinematic.close_clamp()
            time.sleep(self._DELAY_OPEN_CLOSE_CLAMP)
            self._motors.backward(distance)
            while not self._motors.is_done(self.__done_callback):
                time.sleep(0.5)
            self._kinematic.up_clamp()
            time.sleep(self._DELAY_UP_DOWN_CLAMP)
            self._kinematic.open_clamp()

    def eject_modules(self, number=1):
        for i in range(number):
            self._kinematic.push_out()
            time.sleep(self._DELAY_IN_OUT_BLOCK)
            self._kinematic.push_back()
            time.sleep(self._DELAY_IN_OUT_BLOCK)

    def move_to(self, target):
        """
        target: a dict with keys:
            - "angle": a X-axis relative constrain target angle.
            - "point": position of the target.
        """
        while True:
            instructions = self._graph.get_path(self._position, target)
            status = self._motors.move_with_instructions(instructions, self.__move_callback)
            if status == 'ok':
                break

    def __move_callback(self):
        """
        Return a string giving the state if we need to stop or not the regulation because of
        an obstacle.
        """
        ranges = self._us_sensors.get_ranges()

        for us_data in self.US_SENSORS:
            for i, sensor in enumerate(us_data['sensors']):
                if ranges[sensor] == 0:
                    # Zero value means that we are too far from obstacles.
                    continue
                if ranges[sensor] < us_data['trigger_limit']:
                    logging.warn('Motors stopped becauce of the %s%i US sensors at %i cm',
                                 us_data['name'], i, ranges[sensor])
                    self._motors.stop()
                    # TODO: avoid recalculation if we have the near same position.
                    self._graph.reset_obstacles()
                    self._graph.add_obstacle(
                        self._position,
                        self.DIMENSION,
                        self.OBSTACLES_DIMENSION,
                        us_data['name'],
                        ranges[sensor]
                    )
                    return 'obstacle'
        return 'continue'

    def __done_callback(self, distance_travelled, status='ok'):
        """
        Update the position and angle informations of the robots.
        """
        self._move_target = None

        logging.info('Regulation is done!')
        self.__update_robot_position(distance_travelled)

        return status

    def __update_robot_position(self, distance_travelled):
        left = distance_travelled['left']
        right = distance_travelled['right']

        if self.__opposite_sign(left, right):
            # We finished a rotation regulation.
            angle = ((left - right) / 2) / Motors.ANGLE_CORRECTION
            self._position['angle'] = angle
            logging.info('Robot turned with an angle of %i', angle)
        else:
            # We finished a lead regulation.
            angle = self._position['angle']
            distance = (left + right) / 2

            self._position['point'][0] += distance * math.cos(math.radians(angle))
            self._position['point'][1] += distance * math.sin(math.radians(angle))

    def __is_opposite_sign(n, m):
        if n > 0 and m > 0:
            return False
        elif n < 0 and m < 0:
            return False
        return True
