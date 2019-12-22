#!/usr/bin/env python3

from time import sleep
import time
from . import __animation

class two_colours(__animation.animation):
    def __init__(self, led):
        super(two_colours, self).__init__(led, "two_colours")
        self.initialize_argument("speed_two_colours", "Speed: ", default_value=20)
        self.initialize_argument("transition_two_colours", "Transition time: ", default_value=30)
        self.initialize_argument("length_two_colours", "Length: ", default_value=30)
        self.initialize_argument("direction_two_colours", "Direction: ", default_value=0)
        self.initialize_argument("cp_two_colours_1", "Colour 1", default_value="00ff00")
        self.initialize_argument("cp_two_colours_2", "Colour 2", default_value="ff0000")
        self.position=0
    def run(self):
        while self.enabled:
            c1=self.get_argument("cp_two_colours_1")
            c2=self.get_argument("cp_two_colours_2")
            r1, g1, b1 = self.parse_colour(c1)
            r2, g2, b2 = self.parse_colour(c2)
            for i in range(self.led.CONST_LED_COUNT):
                p=self.position
                l=int(self.get_argument("length_two_colours"))
                if (i >= p and i <= p+l) or (i < p and i < ((p+l)%self.led.CONST_LED_COUNT) and (p+l)>self.led.CONST_LED_COUNT):
                    self.led.get_diode(i).set_soft(red=r1, green=g1, blue=b1, steps=int(self.get_argument("transition_two_colours")), intensity=self.led.get_brightness())
                else:
                    self.led.get_diode(i).set_soft(red=r2, green=g2, blue=b2, steps=int(self.get_argument("transition_two_colours")), intensity=self.led.get_brightness())
            sleep_length = 1.00 / int(self.get_argument("speed_two_colours"))
            sleep(sleep_length)
            if not self.enabled:
                break
            if int(self.get_argument("direction_two_colours"))%2:
                self.position+=1
            else:
                self.position-=1
            self.position%=self.led.CONST_LED_COUNT
