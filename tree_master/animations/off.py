#!/usr/bin/env python3

from . import __animation

class off(__animation.animation):
    def __init__(self, led):
        super(off, self).__init__(led, "off")
        for i in range(self.led.CONST_LED_COUNT):
            self.led.get_diode(i).set_soft(red=0, green=0, blue=0, steps=50, intensity=self.led.get_brightness())
    def run(self):
        pass
