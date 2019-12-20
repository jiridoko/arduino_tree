#!/usr/bin/env python3

from time import sleep
from . import __animation
from random import *

class red(__animation.animation):
    def __init__(self, led):
        super(red, self).__init__(led, "red")
        self.initialize_argument("red_red", "Red: ", default_value=255)
        self.initialize_argument("red_green", "Green: ", default_value=0)
        self.initialize_argument("red_blue", "Blue: ", default_value=0)
        self.reset()

    def bytesafe(self, number):
        if int(number) > 255:
            return 255
        elif int(number) < 0:
            return 0
        else:
            return int(number)

    def reset(self):
        red  =self.bytesafe(self.get_argument("red_red"))
        green=self.bytesafe(self.get_argument("red_green"))
        blue =self.bytesafe(self.get_argument("red_blue"))
        for i in range(self.led.CONST_LED_COUNT):
            self.led.get_diode(i).set_soft(red=red, green=green, blue=blue, intensity=self.led.get_brightness(), steps=20)

    def run(self):
        while self.enabled:
            self.reset()
