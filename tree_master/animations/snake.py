#!/usr/bin/env python2

from time import sleep
import __animation

class snake(__animation.animation):
    def __init__(self, led, storage):
        super(snake, self).__init__(led, storage, "snake")
    def run(self):
        while self.enabled:
            for i in xrange(0,80):
                self.led.set_led_value(i, self.led.CONST_MAX_INTENSITY)
                sleep(0.05)
                if not self.enabled:
                    break
