import time
import RPi.GPIO as GPIO
import multiprocessing

from robot import Robot
from map_points import Assets


def run(robot, assets):
    robot = Robot(assets.get_point('start'))
    robot.move_to(assets.get_point('rocket'))
    robot.take_modules(4,5)
    robot.move_to(assets.get_point('remove'))
    robot._motors.forward(40)
    while not robot._motors.is_done(robot.__done_callback):
        time.sleep(0.5)
    robot.move_to(assets.get_point('discharge'))
    robot.eject_modules(4)
    robot.move_to(assets.get_point('mono2'))
    robot.take_modules(1,0)
    robot.move_to(assets.get_point('discharge'))
    robot.eject_modules(1)


if __name__ == '__main__':
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)

    assets = Assets('yellow')
    if GPIO.output(11) == 1:
        assets = Assets('blue')
    robot = Robot(assets.get_point('start'))

    while GPIO.output(13) == 0:
        time.sleep(0.2)

    pool = multiprocessing.Pool(processes=1)
    pool.map(run, args=(robot, assets))

    time.sleep(90)
    pool.terminate()

    robot.finalize()
