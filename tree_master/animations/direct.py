#!/usr/bin/env python2

import base64
import __animation

class direct(__animation.animation):
    def __init__(self, led, storage):
        super(direct, self).__init__(led, storage, "direct", blank_args=True)
    def run(self):
        pass
    def direct_call(self, data):
        # format: base64_encode("<led_id>;<intensity>|<led_id>;<intensity>| ... ")
        decoded = base64.standard_b64decode(data)
        array = map(lambda x: x.split(";"), decoded.split("|"))
        for led_id, intensity in array:
            self.led.set_unbuffered(int(led_id), int(intensity))
