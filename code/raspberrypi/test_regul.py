import time
import timeit

from motors import Motors

def wait_motors(motors):
    while not motors.is_done():
        time.sleep(0.1)

def test_regul():
    """
    Make a square with the robot and at the end make it turn the
    other direction  (just for fun).
    """
    DISTANCE = 50
    ANGLE = 90

    motors = Motors(5)
    motors.forward(DISTANCE)
    wait_motors(motors)
    motors.turn_left(ANGLE)
    wait_motors(motors)
    motors.forward(DISTANCE)
    wait_motors(motors)
    motors.turn_left(ANGLE)
    wait_motors(motors)
    motors.forward(DISTANCE)
    wait_motors(motors)
    motors.turn_left(ANGLE)
    wait_motors(motors)
    motors.forward(DISTANCE)
    wait_motors(motors)
    # We can't turn more than 255 degrees because
    # the data send to the Arduino is a 8bits value.
    motors.turn_right(180)
    wait_motors(motors)
    motors.turn_right(90)
    wait_motors(motors)


if __name__ == '__main__':
    # Display the time that the regulation has taken.
    # Could be used to improve the regulation parameter.
    t = timeit.timeit('test_regul()', setup='from __main__ import test_regul')

    # Cleaner but this API is only valid for > python3.5
    # t = timeit.timeit('test_regul()', globals=globals(), number=1)

    print(t)
