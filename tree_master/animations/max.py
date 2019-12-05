#!/usr/bin/env python3

from . import __animation

class max(__animation.animation):
    def __init__(self, led):
        super(max, self).__init__(led, "max")
        for i in range(self.led.CONST_LED_COUNT):
            self.led.get_diode(i).set_soft(red=255, green=255, blue=255, steps=50, intensity=self.led.get_brightness())
    def run(self):
        pass
