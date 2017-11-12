#!/usr/bin/env python2

from time import sleep
import animation
from random import *

class rand(animation.animation):
    def __init__(self, led):
        super(rand, self).__init__(led)
    def run(self):
        while self.enabled:
            i = randint(0,80)
            self.led.set_led_value(i, self.led.CONST_MAX_INTENSITY)
            sleep(0.05)
