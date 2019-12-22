#!/usr/bin/env python3

from time import sleep
from . import __animation
from random import *

class purple(__animation.animation):
    def __init__(self, led):
        super(purple, self).__init__(led, "purple")
        self.initialize_argument("cp_purple_colour", "Colour: ", default_value="ff00ff")
        self.reset()

    def reset(self):
        c=str(self.get_argument("cp_purple_colour"))
        red, green, blue = self.parse_colour(c)
        for i in range(self.led.CONST_LED_COUNT):
            self.led.get_diode(i).set_soft(red=red, green=green, blue=blue, intensity=self.led.get_brightness(), steps=20)

    def run(self):
        while self.enabled:
            self.reset()
