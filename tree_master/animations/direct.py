#!/usr/bin/env python3

import base64
from . import __animation

class direct(__animation.animation):
    def __init__(self, led):
        super(direct, self).__init__(led, "direct")
        for i in range(self.led.CONST_LED_COUNT):
            self.led.get_diode(i).set_soft(red=0, green=0, blue=0, steps=50, intensity=self.led.get_brightness())
    def run(self):
        pass
    def direct_call(self, data):
        # format: base64_encode("<led_id>;<r>;<g>;<b>|<led_id>;<r>;<g>;<b>| ... ")
        decoded = base64.standard_b64decode(data)
        array = map(lambda x: x.split(";"), str(decoded, encoding='utf-8', errors='strict').split("|"))
        for led_id, r, g, b in array:
            diode=self.led.get_diode(int(led_id))
            if diode is not None:
                diode.set(red=int(r), green=int(g), blue=int(b), intensity=self.led.get_brightness())
