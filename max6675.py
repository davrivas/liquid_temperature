# adapted from https://github.com/archemius/MAX6675-Raspberry-pi-python

from machine import Pin
import time

class MAX6675:
    # set pin number for communicate with MAX6675
    def __init__(self, CS, SCK, SO) -> None:
        self._cs_no = CS
        self._cs = Pin(CS, Pin.OUT)
        self._cs.on()
        
        self._sck = Pin(SCK, Pin.OUT)
        self._sck.off()
        
        self._so = Pin(SO, Pin.IN)
        self._so.on()

    def read_temp(self) -> float:
        self._cs.off()
        time.sleep(0.002)
        self._cs.on()
        time.sleep(0.22)

        self._cs.off()
        self._sck.on()
        time.sleep(0.001)
        self._sck.off()
        value = 0
        for i in range(11, -1, -1):
            self._sck.on()
            value = value + (self._so.value() * (2 ** i))
            self._sck.off()

        self._sck.on()
        error_tc = self._so.value()
        self._sck.off()

        for i in range(2):
            self._sck.on()
            time.sleep(0.001)
            self._sck.off()

        self._cs.on()

        temp = value * 0.25 # Celsius

        if error_tc != 0:
            return float(str(self._cs_no))
        else:
            return float(str(temp))