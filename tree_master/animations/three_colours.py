#!/usr/bin/env python3

from . import __animation
from random import *
from time import sleep

class three_colours(__animation.animation):
    def __init__(self, led):
        super(three_colours, self).__init__(led, "three_colours")
        self.initialize_argument("cp_three_colours_1", "Colour 1", default_value="ff0000")
        self.initialize_argument("cp_three_colours_2", "Colour 2", default_value="0000ff")
        self.initialize_argument("cp_three_colours_3", "Colour 3", default_value="ffffff")
        self.initialize_argument("three_colours_direction", "Direction: ", default_value="0")
        self.initialize_argument("three_colours_transition", "Transition: ", default_value="10")
        self.initialize_argument("three_colours_speed", "Speed: ", default_value="10")
        self.reset()
        self.position = 0
    def reset(self):
        for i in range(self.led.CONST_LED_COUNT):
            self.led.get_diode(i).set_soft(red=0, green=0, blue=0, steps=5, intensity=self.led.get_brightness())
    def run(self):
        while self.enabled:
            third = round(self.led.CONST_LED_COUNT/3)
            r1, g1, b1 = self.parse_colour(str(self.get_argument("cp_three_colours_1")))
            r2, g2, b2 = self.parse_colour(str(self.get_argument("cp_three_colours_2")))
            r3, g3, b3 = self.parse_colour(str(self.get_argument("cp_three_colours_3")))
            transition = int(self.get_argument("three_colours_transition"))
            direction = int(self.get_argument("three_colours_direction"))
            for i in range(self.led.CONST_LED_COUNT):
                x = (i+self.position)%self.led.CONST_LED_COUNT
                if i < third:
                    self.led.get_diode(x).set_soft(red=r1, green=g1, blue=b1, steps=transition, intensity=self.led.get_brightness())
                elif i < (2*third):
                    self.led.get_diode(x).set_soft(red=r2, green=g2, blue=b2, steps=transition, intensity=self.led.get_brightness())
                else:
                    self.led.get_diode(x).set_soft(red=r3, green=g3, blue=b3, steps=transition, intensity=self.led.get_brightness())

            if direction%2:
                self.position+=1
                if self.position >= self.led.CONST_LED_COUNT:
                    self.position = 0
            else:
                self.position-=1
                if self.position <= 0:
                    self.position = self.led.CONST_LED_COUNT
            sleep(1.00/int(self.get_argument("three_colours_speed")))
