#!/usr/bin/env python3

from time import sleep
import time
from . import __animation

class snake(__animation.animation):
    def __init__(self, led, storage):
        super(snake, self).__init__(led, storage, "snake")
        self.initialize_argument("speed", "Speed: ", default_value=20)
        self.sum = 0.00
        self.count = 0
    def _add_sample(self, sample):
        self.sum += sample
        self.count += 1
    def _show_avg(self):
        if self.count > 0:
            print("avg: "+str(self.sum/self.count)+"s")
        else:
            print("avg: 0s")
    def run(self):
        while self.enabled:
            for i in range(120):
                #t1 = float(time.time())
                self.led.set_led_value(i, self.led.CONST_MAX_INTENSITY)
                #t2 = float(time.time())
                #self._add_sample(t2-t1)
                sleep_length = 1.00 / int(self.get_argument("speed"))
                sleep(sleep_length)
                if not self.enabled:
                    break
            #self._show_avg()
