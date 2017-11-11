#!/usr/bin/env python2.7
from smbus import SMBus
from threading import Thread
from threading import Semaphore

class led_master(Thread):
    CONST_LED_COUNT = 120
    CONST_CONTROLLER1_ID = 11
    CONST_CONTROLLER2_ID = 12
    CONST_CONTROLLER3_ID = 13
    CONST_MAX_INTENSITY = 63

    def __init__(self, bus_id=1, ramp_up_speed=20, calm_down_speed=2, retention=0):
        super(led_master, self).__init__()
        self.bus = SMBus(bus_id)
        self.ramp_up_speed = ramp_up_speed
        self.calm_down_speed = calm_down_speed
        self.retention = retention
        self.current_array = [0] * self.CONST_LED_COUNT
        self.buffer_array = [0] * self.CONST_LED_COUNT
        self.retention_array = [0] * self.CONST_LED_COUNT
        self.semaphore_array = []
        self._initialize_semaphore_array()
        self.updating = True

    def set_updating(self, value):
        self.updating = value

    def set_ramp_up_speed(self, value):
        self.ramp_up_speed = value

    def set_calm_down_speed(self, value):
        self.calm_down_speed = value

    def set_retention(self, value):
        self.retention = value

    def set_led_value(self, led_id, intensity, retention=-1):
        if led_id < self.CONST_LED_COUNT:
            self.semaphore_array[led_id].acquire()
            self.buffer_array[led_id] = self._safe_intensity(intensity)
            if retention == -1:
                self.retention_array[led_id] = self.retention
            else:
                self.retention_array[led_id] = retention
            self.semaphore_array[led_id].release()

    def _initialize_semaphore_array(self):
        for i in xrange(0, self.CONST_LED_COUNT):
            self.semaphore_array.append(Semaphore())

    def _safe_intensity(self, intensity):
        if intensity > self.CONST_MAX_INTENSITY:
            return self.CONST_MAX_INTENSITY
        elif intensity < 0:
            return 0;
        else:
            return intensity

    def _i2c_signal(self, address, cmd, value):
        tries=3
        while tries > 0:
            try:
                self.bus.write_byte_data(address, cmd, value)
                tries = 0
            except IOError:
                tries-=1;
        if tries < 0:
            print "[i2c] address "+str(address)+" unreachable"

    def _signal_led(self, led_id, intensity):
        if led_id < 40:
            self._i2c_signal(self.CONST_CONTROLLER1_ID, led_id, self._safe_intensity(intensity))
        elif led_id < 80:
            self._i2c_signal(self.CONST_CONTROLLER2_ID, led_id-40, self._safe_intensity(intensity))
        elif led_id < 120:
            self._i2c_signal(self.CONST_CONTROLLER3_ID, led_id-80, self._safe_intensity(intensity))

    def run(self):
        while self.updating:
            for i in xrange(0, self.CONST_LED_COUNT):
                update = False
                self.semaphore_array[i].acquire()
                if self.buffer_array[i] > 0: # we're ramping up
                    self.current_array[i] = self._safe_intensity(self.current_array[i] + self.ramp_up_speed)
                    self.buffer_array[i] = self._safe_intensity(self.buffer_array[i] - self.ramp_up_speed)
                    update = True # we need to update this LED
                elif self.retention_array[i] > 0:
                    self.retention_array[i]-=1
                elif self.calm_down_speed > 0 and self.buffer_array[i] == 0 and self.current_array[i] > 0: # we're calming down
                    self.current_array[i] = self._safe_intensity(self.current_array[i] - self.calm_down_speed)
                    update = True

                if update:
                    self._signal_led(i, self.current_array[i])
                self.semaphore_array[i].release()

if __name__ == "__main__":
    from time import sleep

    l = led_master(ramp_up_speed=20, calm_down_speed=1, retention=50)

    #a = [80, 83, 86, 89, 92, 95, 98, 40, 43, 46, 49, 52, 55, 58, 0, 3, 6, 9, 12, 15, 18, 38, 35, 32, 29, 26, 23, 20, 78, 75, 72, 69, 66, 63, 60, 118, 115, 112, 109, 106, 103, 100] 
    #a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39] 

    try:
        l.start()

        sleep(1)

        for i in xrange(0, 20):
            for j in xrange(0, 80):
                l.set_led_value(j, l.CONST_MAX_INTENSITY)
                sleep(0.05)
        sleep(2)
        l.set_updating(False)
    except KeyboardInterrupt:
        l.set_updating(False)

