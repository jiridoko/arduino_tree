#!/usr/bin/env python3

from time import sleep
from . import __animation

class snake(__animation.animation):
    def __init__(self, led, storage):
        super(snake, self).__init__(led, storage, "snake")
        self.initialize_argument("speed", "Speed: ", default_value=20)
    def run(self):
        while self.enabled:
            for i in range(120):
                self.led.set_led_value(i, self.led.CONST_MAX_INTENSITY)
                sleep_length = 1.00 / int(self.get_argument("speed"))
                sleep(sleep_length)
                if not self.enabled:
                    break
