#!/usr/bin/env python3

from time import sleep
from . import __animation
from random import *

class yellow(__animation.animation):
    def __init__(self, led):
        super(yellow, self).__init__(led, "yellow")
        self.initialize_argument("cp_yellow_colour", "Colour: ", default_value="ffff00")
        self.reset()

    def reset(self):
        c=str(self.get_argument("cp_yellow_colour"))
        red, green, blue = self.parse_colour(c)
        for i in range(self.led.CONST_LED_COUNT):
            self.led.get_diode(i).set_soft(red=red, green=green, blue=blue, intensity=self.led.get_brightness(), steps=20)

    def run(self):
        while self.enabled:
            self.reset()
