#!/usr/bin/env python2

import smbus

bus = smbus.SMBus(1)
for i in [0x0b, 0x0c, 0x0d]:
    try:
        bus.write_byte_data(i, 0xff, 0xff)
    except:
        print str(i)+" unavailable"
bus.close()
