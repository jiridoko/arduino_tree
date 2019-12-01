#!/usr/bin/env python3

from time import sleep
import time
from . import __animation

class rainbow(__animation.animation):
    def __init__(self, led):
        super(rainbow, self).__init__(led, "rainbow")
        self.initialize_argument("speed_rainbow", "Speed: ", default_value=20)
        self.initialize_argument("transition_rainbow", "Transition time: ", default_value=100)
        self.initialize_argument("length_rainbow", "Length: ", default_value=30)
        self.initialize_argument("direction_rainbow", "Direction: ", default_value=0)
        self.initialize_argument("increment_rainbow", "Increment: ", default_value=10)
        self.red=255
        self.green=0
        self.blue=0
        self.position=0
        self.count = 0
        self.state = 0
        self.state_count = 6

    def _incr(self, n):
        i=int(self.get_argument("increment_rainbow"))
        return n+i if (n+i) <= 255 else 255

    def _decr(self, n):
        i=int(self.get_argument("increment_rainbow"))
        return n-i if (n-i) >= 0 else 0

    def _move_state(self):
        self.state+=1
        self.state%=self.state_count

    def new_colour(self):
        if self.state == 0:
            # red max, green up
            self.green = self._incr(self.green)
            if self.green >= 255:
                self._move_state()
        elif self.state == 1:
            # green max, red down
            self.red = self._decr(self.red)
            if self.red <= 0:
                self._move_state()
        elif self.state == 2:
            # green max, blue up
            self.blue = self._incr(self.blue)
            if self.blue >= 255:
                self._move_state()
        elif self.state == 3:
            # blue max, green down
            self.green = self._decr(self.green)
            if self.green <= 0:
                self._move_state()
        elif self.state == 4:
            # blue max, red up
            self.red = self._incr(self.red)
            if self.red >= 255:
                self._move_state()
        elif self.state == 5:
            # red max, blue down
            self.blue = self._decr(self.blue)
            if self.blue <= 0:
                self._move_state()

    def run(self):
        while self.enabled:
            for i in range(self.led.CONST_LED_COUNT):
                p=self.position
                l=int(self.get_argument("length_rainbow"))
                self.count+=1
                self.count=self.count%int(self.get_argument("length_rainbow"))
                if self.count == 0:
                    self.new_colour()
                self.led.get_diode(i).set_soft(red=self.red, green=self.green, blue=self.blue, steps=int(self.get_argument("transition_rainbow")), intensity=self.led.get_brightness())
                sleep_length = 1.00 / int(self.get_argument("speed_rainbow"))
                sleep(sleep_length)
                if not self.enabled:
                    break
                if int(self.get_argument("direction_rainbow"))%2:
                    self.position+=1
                else:
                    self.position-=1
                self.position%=self.led.CONST_LED_COUNT
