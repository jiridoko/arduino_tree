#!/usr/bin/env python2

from time import sleep
import animation

class snake(animation.animation):
    def __init__(self, led):
        super(snake, self).__init__(led)
    def run(self):
        while self.enabled:
            for i in xrange(0,80):
                self.led.set_led_value(i, self.led.CONST_MAX_INTENSITY)
                sleep(0.05)
