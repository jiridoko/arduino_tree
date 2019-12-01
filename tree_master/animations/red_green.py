#!/usr/bin/env python3

from time import sleep
import time
from . import __animation

class red_green(__animation.animation):
    def __init__(self, led):
        super(red_green, self).__init__(led, "red_green")
        self.initialize_argument("speed_red_green", "Speed: ", default_value=20)
        self.initialize_argument("transition_red_green", "Transition time: ", default_value=30)
        self.initialize_argument("length_red_green", "Length: ", default_value=30)
        self.initialize_argument("direction_red_green", "Direction: ", default_value=0)
        self.position=0
    def run(self):
        while self.enabled:
            for i in range(self.led.CONST_LED_COUNT):
                p=self.position
                l=int(self.get_argument("length_red_green"))
                if (i >= p and i <= p+l) or (i < p and i < ((p+l)%self.led.CONST_LED_COUNT) and (p+l)>self.led.CONST_LED_COUNT):
                    self.led.get_diode(i).set_soft(red=255, green=0, blue=0, steps=int(self.get_argument("transition_red_green")), intensity=self.led.get_brightness())
                else:
                    self.led.get_diode(i).set_soft(red=0, green=255, blue=0, steps=int(self.get_argument("transition_red_green")), intensity=self.led.get_brightness())
            sleep_length = 1.00 / int(self.get_argument("speed_red_green"))
            sleep(sleep_length)
            if not self.enabled:
                break
            if int(self.get_argument("direction_red_green"))%2:
                self.position+=1
            else:
                self.position-=1
            self.position%=self.led.CONST_LED_COUNT
