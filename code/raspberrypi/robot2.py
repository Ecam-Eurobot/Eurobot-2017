import time
import logging
import math

from motors import Motors
from kinematics import Kinematics
from range_sensors import RangeSensor

DELAY_OPEN_ClOSE_CLAMP = 0.7
DELAY_UP_DOWN_CLAMP = 2.5
DELAY_IN_OUT_BLOCK = 3

class Robot:
    # US sensors constants.
    US_SENSORS = [
        {'name': 'front_bottom', 'trigger_limit': 8, 'sensors': 0},
        {'name': 'left', 'trigger_limit': 10, 'sensors': 2},
        {'name': 'back', 'trigger_limit': 8, 'sensors': 4},
        {'name': 'right', 'trigger_limit': 10, 'sensors': 3},
        {'name': 'front_top', 'trigger_limit': 8, 'sensors':  1},
    ]

    # Take in count the obstacle dimension (assuming another robot)
    # + the robot size.
    OBSTACLES_DIMENSION = 50

    def __init__(self):
        """
        position: init position dict with keys:
            - "angle": a X-axis relative angle.
            - "point": the first position.
        """
        #  self._us_sensors = RangeSensor(4)
        self._motors = Motors(5)
        self._kinematic = Kinematics(6)
        self._us = RangeSensor(4)

        logging.info('Building the graph map.')
        #  self._graph = build_graph(robot_diagonal)
        logging.info('Finished to build the graph map.')
        self._blocking_servo = -1

    def reset_kinematics(self):
        self._kinematic.up_clamp()
        time.sleep(0.2)
        self._kinematic.open_clamp()
        time.sleep(0.2)
        self._kinematic.reset_funny()
        time.sleep(0.2)
        self._kinematic.push_back()
        time.sleep(1)

    def wait_motors(self, enable=True, timeout=0):
        first_time = time.time()
        while not self._motors.is_done():
            if enable:
                if self._blocking_servo != -1:
                    i = self._blocking_servo
                    test = self._us.get_range(i)
                    print(test)
                    if test > self.US_SENSORS[i]['trigger_limit']:
                        self._motors.restart()
                        self._blocking_servo = -1
                    else:
                        continue
                us_sensors = self._us.get_ranges()
                print(us_sensors)
                for i, us in enumerate(us_sensors):
                    if 'front' in self.US_SENSORS[i]['name'] or 'back' in self.US_SENSORS[i]['name']:
                            if us < self.US_SENSORS[i]['trigger_limit']:
                                self._motors.stop()
                                self._blocking_servo = i
                                break
            if (time.time() - first_time) > timeout and timeout != 0:
                break
            time.sleep(0.1)


    def take_modules(self, number=1):
        for i in range(number):
            self._kinematic.open_clamp()
            self._kinematic.down_clamp()
            time.sleep(DELAY_UP_DOWN_CLAMP)
            self._motors.forward(9)
            self.wait_motors(enable=False, timeout=2)

            self._kinematic.close_clamp()
            time.sleep(1)
            #  self._motors.set_speed(40)
            self._motors.backward(7)
            if number == 1:
                self._motors.forward(6)
                self.wait_motors(enable=False, timeout=2)
                self._motors.backward(6)
                self.wait_motors(enable=False, timeout=2)
            self.wait_motors(enable=False)
            self._motors.backward(8)
            self.wait_motors(enable=False)

            #SEULEMENT SI ON DECIDE DE RECULER POUR MIEUX PRENDRE LE MODULE ---
            self._kinematic.open_clamp()
            time.sleep(0.5)
            self._motors.forward(3)
            self.wait_motors(enable=False, timeout=2)
            self._kinematic.close_clamp()
            time.sleep(1)
            #---

            self._motors.forward(3)
            self._kinematic.up_clamp()
            self.wait_motors(enable=False, timeout=3)
            time.sleep(0.5)
            self._kinematic.open_clamp()
            time.sleep(1)
        self._kinematic.down_clamp()
        time.sleep(0.5)
        self._kinematic.up_clamp()

    def eject_modules(self, number=1):
        for i in range(number):
            self._kinematic.push_out()
            time.sleep(1.5)
            self._kinematic.push_back()
            time.sleep(1.5)
        self._motors.forward(2)
        self.wait_motors(timeout=2)
        self._motors.backward(8)
        self.wait_motors(timeout=2)


    def get_kin(self):
        return self._kinematic

    def get_motors(self):
        return self._motors

    def finalize(self):
        self._motors.stop()

        self._kinematic.launch_funny()
        time.sleep(0.8)
        self._kinematic.reset_funny()
