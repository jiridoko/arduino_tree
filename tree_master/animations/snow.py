#!/usr/bin/env python3

from time import sleep
from . import __animation
from random import *

class snow(__animation.animation):
    def __init__(self, led):
        super(snow, self).__init__(led, "snow")
        self.initialize_argument("speed", "Speed: ", default_value=20)
        self.initialize_argument("count", "Count: ", default_value=10)
        self.initialize_argument("transition", "Transition time: ", default_value=30)
        self.previous_count = int(self.get_argument("count"))
        self.position = 0
        self.array = []
        self.reset()

    def reset(self):
        self.array = [-1]*int(self.get_argument("count"))
        self.previous_count = int(self.get_argument("count"))
        self.position = 0
        for i in range(self.led.CONST_LED_COUNT):
            self.led.get_diode(i).set_soft(red=0, green=0, blue=0, intensity=self.led.get_brightness(), steps=int(self.get_argument("transition")))

    def run(self):
        while self.enabled:
            if int(self.get_argument("count")) != self.previous_count:
                self.reset()
            if self.array[self.position] >= 0:
                self.led.get_diode(self.array[self.position]).set_soft(red=0, green=0, blue=0, intensity=self.led.get_brightness(), steps=int(self.get_argument("transition")))
            self.array[self.position] = randint(0, self.led.CONST_LED_COUNT-1)
            self.led.get_diode(self.array[self.position]).set_soft(red=255, green=255, blue=70, intensity=self.led.get_brightness(), steps=int(self.get_argument("transition")))
            self.position+=1
            self.position%=int(self.get_argument("count"))
            sleep(1.00/int(self.get_argument("speed")))
            if not self.enabled:
                break
