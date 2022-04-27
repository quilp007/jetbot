import time
import traitlets
from traitlets.config.configurable import SingletonConfigurable
from .motor import Motor
from .vl53l1x import Vl53l1x
import RPi.GPIO as GPIO

class Robot(SingletonConfigurable):

    left_motor = traitlets.Instance(Motor)
    right_motor = traitlets.Instance(Motor)
    tof_sensor = traitlets.Instance(Vl53l1x)

    distance = traitlets.Integer(default_value=1).tag(config=True)

    # config
    i2c_bus = traitlets.Integer(default_value=1).tag(config=True)
    left_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
    right_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)

    GPIO.setmode(GPIO.BOARD)

    def __init__(self, *args, **kwargs):
        super(Robot, self).__init__(*args, **kwargs)
        self.left_motor = Motor(35, 36, freq=50, alpha=self.left_motor_alpha)
        self.right_motor = Motor(37, 38, freq=50, alpha=self.right_motor_alpha)
        # self.tof_sensor = Vl53l1x(self, i2c_bus_num=self.i2c_bus, i2c_addr=0x29)

    @observe('distance')
    def _observe_distance(self, change):
        new_distance_value = change['new']

    def set_motors(self, left_speed, right_speed):
        self.left_motor.value = left_speed
        self.right_motor.value = right_speed

    def forward(self, speed=1.0, duration=None):
        self.left_motor.value = speed
        self.right_motor.value = speed

    def backward(self, speed=1.0):
        self.left_motor.value = -speed
        self.right_motor.value = -speed

    def left(self, speed=1.0):
        self.left_motor.value = -speed
        self.right_motor.value = speed

    def right(self, speed=1.0):
        self.left_motor.value = speed
        self.right_motor.value = -speed

    def stop(self):
        self.left_motor.value = 0
        self.right_motor.value = 0
