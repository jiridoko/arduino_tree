#!/usr/bin/env python3

from . import __animation
from random import *
from time import sleep

class fireworks(__animation.animation):
    def __init__(self, led):
        super(fireworks, self).__init__(led, "fireworks")
        self.initialize_argument("fireworks_boom_steps", "Boom Steps: ", default_value="10")
        self.initialize_argument("fireworks_launch_steps", "Launch Steps: ", default_value="10")
        self.initialize_argument("cp_fireworks_launch_colour", "Launch Colour", default_value="fff000")
        self.reset()
        self.state=0 # 0=launch, 1=end_launch, 2=boom, 3=end_boom
        self.colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 127, 0), (255, 0, 127)]
        self.launch_position = 0
    def reset(self):
        for i in range(self.led.CONST_LED_COUNT):
            self.led.get_diode(i).set_soft(red=0, green=0, blue=0, steps=5, intensity=self.led.get_brightness())
    def generate_boom_colour(self):
        return self.colours[randint(0, len(self.colours)-1)]
    def run(self):
        while self.enabled:
            if self.state == 0:
                # launch
                if self.launch_position <= self.led.CONST_LED_COUNT:
                    self.launch_position += int(self.get_argument("fireworks_launch_steps"))
                    red, green, blue = self.parse_colour(str(self.get_argument("cp_fireworks_launch_colour")))
                    for i in range (self.launch_position):
                        if i < self.led.CONST_LED_COUNT:
                            self.led.get_diode(i).set_soft(red=red, green=green, blue=blue, steps=5, intensity=self.led.get_brightness())
                    sleep(0.04)
                else:
                    self.state = 1
                    self.launch_position=0
            elif self.state == 1:
                # end launch
                sleep(0.5)
                for i in range(self.led.CONST_LED_COUNT):
                    self.led.get_diode(i).set_soft(red=0, green=0, blue=0, steps=20, intensity=self.led.get_brightness())
                sleep(1)
                self.state = 2
            elif self.state == 2:
                # boom
                r, g, b = self.generate_boom_colour()
                for i in range(self.led.CONST_LED_COUNT):
                    self.led.get_diode(i).set_soft(red=r, green=g, blue=b, steps=2, intensity=self.led.get_brightness())
                sleep(1.5)
                self.state = 3
            elif self.state == 3:
                # end boom
                for i in range(self.led.CONST_LED_COUNT):
                    self.led.get_diode(i).set_soft(red=0, green=0, blue=0, steps=150, intensity=self.led.get_brightness())
                sleep(4)
                self.state = 0
            else:
                self.state = 0
        
