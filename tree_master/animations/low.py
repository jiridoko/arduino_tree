#!/usr/bin/env python3

from time import sleep
from . import __animation

class low(__animation.animation):
    def __init__(self, led, storage):
        super(low, self).__init__(led, storage, "low", blank_args=True)
        self.initialize_argument("sleep", "Sleep time: ", default_value=1)
    def run(self):
        while self.enabled:
            for i in range(8):
                self.led.set_led_value(i, self.led.CONST_MAX_INTENSITY)
                sleep(int(self.get_argument("sleep")))
                if not self.enabled:
                    break
