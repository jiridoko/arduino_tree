#!/usr/bin/env python3

import base64
from . import __animation

class direct(__animation.animation):
    def __init__(self, led):
        super(direct, self).__init__(led, "direct", blank_args=True)
    def run(self):
        pass
    def direct_call(self, data):
        # format: base64_encode("<led_id>;<intensity>|<led_id>;<intensity>| ... ")
        decoded = base64.standard_b64decode(data)
        array = map(lambda x: x.split(";"), str(decoded, encoding='utf-8', errors='strict').split("|"))
        for led_id, intensity in array:
            self.led.set_unbuffered(int(led_id), int(intensity))
