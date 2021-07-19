from max6675 import MAX6675
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
import time

width = 128
height = 64

i2c = I2C(0, scl = Pin(22), sda = Pin(21))
oled = SSD1306_I2C(width, height, i2c)

def main():
    sck = 15
    cs = 2    
    so = 4
    unit = 1

    thermocuple = MAX6675(cs, sck, so, unit) # [unit : 0 - raw, 1 - Celsius, 2 - Fahrenheit]
    
    while True:
        #clear the screen
        oled.fill(0)
        
        # read temperature connected at CS 22
        temp = float(thermocuple.read_temp())
        
        text = "T = {}C".format(temp)
        
        # show temperature
        oled.text(text, 0, 10)
        print(text)
        oled.show()

        # when there are some errors with sensor, it return "-" sign and CS pin number
        # in this case it returns "-22"    
        time.sleep(1)

if __name__ == "__main__":
    main()
