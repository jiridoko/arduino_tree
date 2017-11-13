#!/usr/bin/env python2

import __animation

class direct(__animation.animation):
    def __init__(self, led, storage):
        super(direct, self).__init__(led, storage, "direct", blank_args=True)
    def run(self):
        pass
    def direct_call(self, data):
        print "got a direct dall with data:\""+str(data)+"\""
        pass
