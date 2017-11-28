#!/usr/bin/env python3
import spidev
from threading import Thread
from threading import Semaphore
import time

class led_master(Thread):
    CONST_LED_COUNT = 120
    CONST_CONTROLLER1_ID = 11
    CONST_CONTROLLER2_ID = 12
    CONST_CONTROLLER3_ID = 13
    CONST_MAX_INTENSITY = 63

    def __init__(self, ramp_up_speed=20, calm_down_speed=2, retention=0):
        super(led_master, self).__init__()
        self.bus = spidev.SpiDev()
        self.bus.open(0, 0)
        self.bus.max_speed_hz = 150000
        self.bus.writebytes([0xFF, 0xFF, 0xFF])
        self.ramp_up_speed = ramp_up_speed
        self.calm_down_speed = calm_down_speed
        self.retention = retention
        self.current_array = [0] * self.CONST_LED_COUNT
        self.buffer_array = [0] * self.CONST_LED_COUNT
        self.retention_array = [0] * self.CONST_LED_COUNT
        self.direct_array = [0] * self.CONST_LED_COUNT
        self.direct = False
        self.semaphore_array = []
        self._initialize_semaphore_array()
        self.updating = True
        self.array = range(0,40)
        self.sum = 0.00
        self.count = 0

    def _add_sample(self, sample):
        self.sum += sample
        self.count += 1

    def _show_avg(self):
        if self.count > 0 and self.count % 100 == 0:
            print("avg: "+str(self.sum/self.count)+"s")

    def set_updating(self, value):
        self.updating = value

    def set_ramp_up_speed(self, value):
        self.ramp_up_speed = int(value)

    def set_calm_down_speed(self, value):
        self.calm_down_speed = int(value)

    def set_retention(self, value):
        self.retention = int(value)

    def set_led_value(self, led_id, intensity, retention=-1):
        self.direct = False
        if led_id < self.CONST_LED_COUNT:
            self.semaphore_array[led_id].acquire()
            self.buffer_array[led_id] = self._safe_intensity(intensity)
            if retention == -1:
                self.retention_array[led_id] = self.retention
            else:
                self.retention_array[led_id] = retention
            self.semaphore_array[led_id].release()

    def set_unbuffered(self, led_id, intensity):
        self.direct = True
        if led_id < self.CONST_LED_COUNT:
            self.semaphore_array[led_id].acquire()
            self.direct_array[led_id] = self._safe_intensity(intensity)
            self.semaphore_array[led_id].release()

    def _initialize_semaphore_array(self):
        for i in range(0, self.CONST_LED_COUNT):
            self.semaphore_array.append(Semaphore())

    def _safe_intensity(self, intensity):
        if intensity > self.CONST_MAX_INTENSITY:
            return self.CONST_MAX_INTENSITY
        elif intensity < 0:
            return 0;
        else:
            return intensity

    def _get_controller_id(self, seq_num):
        if seq_num == 0:
            return self.CONST_CONTROLLER1_ID
        elif seq_num == 1:
            return self.CONST_CONTROLLER2_ID
        elif seq_num == 2:
            return self.CONST_CONTROLLER3_ID

    def _write_spi_data(self, diode_id, intensity):
        self.bus.writebytes([diode_id, intensity, 0xFF])

    def run(self):
        while self.updating:
            for i in range(0,120):
                update = False
                self.semaphore_array[i].acquire()
                if self.direct:
                    # Direct buffer access
                    if self.current_array[i] != self.direct_array[i]:
                        update = True
                        self.current_array[i] = self.direct_array[i]
                else:
                    # Easy buffer access
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
                    self._write_spi_data(i, self.current_array[i])
                self.semaphore_array[i].release()

if __name__ == "__main__":
    from time import sleep

    l = led_master(ramp_up_speed=20, calm_down_speed=1, retention=50)

    #a = [80, 83, 86, 89, 92, 95, 98, 40, 43, 46, 49, 52, 55, 58, 0, 3, 6, 9, 12, 15, 18, 38, 35, 32, 29, 26, 23, 20, 78, 75, 72, 69, 66, 63, 60, 118, 115, 112, 109, 106, 103, 100] 
    #a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39] 

    try:
        l.start()

        sleep(1)

        for i in range(0, 20):
            for j in range(0, 80):
                l.set_led_value(j, l.CONST_MAX_INTENSITY)
                sleep(0.05)
        sleep(2)
        l.set_updating(False)
    except KeyboardInterrupt:
        l.set_updating(False)

