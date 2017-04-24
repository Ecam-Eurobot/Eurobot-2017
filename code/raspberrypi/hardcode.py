import time
import RPi.GPIO as GPIO
import multiprocessing

from motors import Motors
from range_sensors import RangeSensor
from robot2 import Robot

def yellow_go_to_distrib(r, m):
    m.forward(10)
    r.wait_motors()
    m.turn_right(60)
    r.wait_motors()
    m.forward(65)
    r.wait_motors()
    m.turn_right(30)
    r.wait_motors()
    m.backward(50)
    r.wait_motors()
    m.forward(12)
    r.wait_motors()
    m.turn_right(90)
    r.wait_motors()
    m.forward(5)
    r.wait_motors()

    #  m.forward(23)
    #  r.wait_motors()
    #  m.turn_right(35)
    #  r.wait_motors(enable=False)
    #  m.forward(39)
    #  r.wait_motors(enable=False)
    #  m.turn_right(145)
    #  r.wait_motors()
    #  m.forward(6)
    #  r.wait_motors()

def yellow_go_to_empty(r, m, k):
    m.backward(10)
    r.wait_motors()
    m.turn_right(135)
    r.wait_motors()
    m.forward(79)
    r.wait_motors()
    m.turn_right(90)
    r.wait_motors()
    m.forward(7)
    r.wait_motors()
    k.middle_clamp()
    time.sleep(1.5)
    m.turn_right(60)
    r.wait_motors()
    k.up_clamp()
    m.turn_left(60)
    r.wait_motors()
    m.forward(12)
    r.wait_motors(timeout=3)

def blue_go_to_distrib(r, m):
    m.forward(10)
    r.wait_motors()
    m.turn_left(60)
    r.wait_motors()
    m.forward(65)
    r.wait_motors()
    m.turn_left(30)
    r.wait_motors()
    m.backward(55)
    r.wait_motors()
    m.forward(29)
    r.wait_motors()
    m.turn_left(86)
    r.wait_motors()
    m.forward(9)
    r.wait_motors()
    #  m.forward(10)
    #  r.wait_motors()
    #  m.turn_right(60)
    #  r.wait_motors()
    #  m.forward(65)
    #  r.wait_motors()
    #  m.turn_right(30)
    #  r.wait_motors()
    #  m.backward(70)
    #  r.wait_motors()
    #  m.forward(23)
    #  r.wait_motors()
    #  m.turn_left(45)
    #  r.wait_motors()
    #  m.forward(49)
    #  r.wait_motors()
    #  m.turn_left(135)
    #  r.wait_motors()
    #  m.forward(17)
    #  r.wait_motors()

def blue_go_to_empty(r, m, k):
    m.turn_left(135)
    r.wait_motors()
    m.forward(78)
    r.wait_motors()
    m.turn_left(90)
    r.wait_motors(enable=False)
    #  m.forward(13)
    #  r.wait_motors(enable=False, timeout=4)
    k.middle_clamp()
    time.sleep(1.5)
    m.turn_right(60)
    r.wait_motors()
    k.up_clamp()
    m.turn_left(60)
    r.wait_motors()
    m.forward(12)
    r.wait_motors(timeout=3)


def launch_yellow():
    print('yellow')
    r = Robot()
    #  r.reset_kinematics()

    m = r.get_motors()
    yellow_go_to_distrib(r, m)
    r.take_modules(number=3)
    yellow_go_to_empty(r, m, r.get_kin())
    r.eject_modules(number=3)

def launch_blue():
    print('blue')
    r = Robot()
    #  r.reset_kinematics()

    m = r.get_motors()
    blue_go_to_distrib(r, m)
    r.take_modules(number=3)
    blue_go_to_empty(r, m, r.get_kin())
    r.eject_modules(number=3)

def test():
    r = Robot()
    r.reset_kinematics()
    r.eject_modules(number=3)


#  if __name__ == '__main__':
    #  m = Motors(5)
    #  r = Robot()
    #  r.reset_kinematics()
    #  yellow_go_to_distrib(m)
    #  r.take_modules(number=4)
    #  yellow_go_to_empty(m, r.get_kin())
    #  r.eject_modules(number=4)

# vert => GPIO4 (couleur) GPIO4
# brun => GPIO14 (tirette) GPIO15
# jaune => GPIO15 (strategie) GPIO16

#  def test():
    #  print('ok')
    #  r = Robot()
    #  r.reset_kinematics()

    #  m = r.get_motors()
    #  m.forward(100)
    #  r.wait_motors()

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.IN)
    GPIO.setup(8, GPIO.IN)
    GPIO.setup(10, GPIO.IN)

    while GPIO.input(8) == 1:
        time.sleep(0.2)

    action = None
    if GPIO.input(7) == 1:
        # blue
        action = launch_blue
    else:
        action = launch_yellow

    process = multiprocessing.Process(target=action)
    process.start()
    time.sleep(90)
    process.terminate()
    r = Robot()

    r.finalize()
    #  pool.map(run, args=(robot, assets))

    #  r.reset_kinematics()
    #  blue_go_to_distrib(m)
    #  r.take_modules(number=4)
    #  blue_go_to_empty(m, r.get_kin())
    #  r.eject_modules(number=4)
