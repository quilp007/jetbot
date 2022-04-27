import atexit
import traitlets
from traitlets.config.configurable import Configurable
import RPi.GPIO as GPIO

class Motor(Configurable):

    value = traitlets.Float()

    # config
    alpha = traitlets.Float(default_value=1.0).tag(config=True)
    beta = traitlets.Float(default_value=0.0).tag(config=True)

    def __init__(self, pin1, pin2, freq=50, *args, **kwargs):
        super(Motor, self).__init__(*args, **kwargs)  # initializes traitlets
        self.pins = {'out1' : pin1, 'out2' : pin2}
        self.PWMs = []
        atexit.register(self._release)
        for out, pin in self.pins.items():
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
            self.PWMs.append(GPIO.PWM(pin, freq))
        self.PWMs[0].start(0)
        self.PWMs[1].start(0)

    @traitlets.observe('value')
    def _observe_value(self, change):
        self._write_value(change['new'])

    def _write_value(self, value):
        """Sets motor value between [-1, 1]"""
        mapped_value = int(100.0 * (self.alpha * value + self.beta))
        speed = min(max(abs(mapped_value), 0), 100)
        self.PWMs[0].changeDutyCycle(speed)
        self.PWMs[1].changeDutyCycle(speed)
        if mapped_value < 0:
            self.PWMs[0].changeDutyCycle(0)
        else:
            self.PWMs[1].changeDutyCycle(0)

    def _release(self):
        """Stops motor by releasing control"""
        self.PWMs[0].stop()
        self.PWMs[1].stop()
