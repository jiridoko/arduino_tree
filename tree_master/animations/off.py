#!/usr/bin/env python2

import __animation

class off(__animation.animation):
    def __init__(self, led, storage):
        super(off, self).__init__(led, storage, "off", blank_args=True)
    def run(self):
        #for i in xrange(0, self.led.CONST_LED_COUNT):
        #    self.led.set_unbuffered(i, 0)
        pass
