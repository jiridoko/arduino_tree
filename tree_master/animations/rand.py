#!/usr/bin/env python3

from time import sleep
from . import __animation
from random import *

class rand(__animation.animation):
    def __init__(self, led):
        super(rand, self).__init__(led, "rand")
    def run(self):
        while self.enabled:
            i = randint(0,119)
            self.led.set_led_value(i, self.led.CONST_MAX_INTENSITY)
            sleep(0.05)
