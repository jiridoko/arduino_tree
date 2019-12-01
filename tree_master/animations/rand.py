#!/usr/bin/env python3

from time import sleep
from . import __animation
from random import *

class rand(__animation.animation):
    def __init__(self, led):
        super(rand, self).__init__(led, "random")
        self.initialize_argument("speed", "Speed: ", default_value=20)
        self.initialize_argument("count", "Count: ", default_value=1)
        self.initialize_argument("transition", "Transition time: ", default_value=30)
    def run(self):
        while self.enabled:
            for x in range(int(self.get_argument("count"))):
                i = randint(0,self.led.CONST_LED_COUNT-1)
                self.led.get_diode(i).set_soft(red=randint(0,0xFF), green=randint(0,0xFF), blue=randint(0,0xFF), intensity=self.led.get_brightness(), steps=int(self.get_argument("transition")))
                sleep(1.00/int(self.get_argument("speed")))
                if not self.enabled:
                    break
