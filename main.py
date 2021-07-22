from max6675 import MAX6675
from machine import I2C, PWM, Pin
from ssd1306 import SSD1306_I2C
import time

width = 128
height = 64

i2c = I2C(0, scl = Pin(22), sda = Pin(21))
oled = SSD1306_I2C(width, height, i2c)

buzzer = PWM(Pin(32), freq = 500)
buzzer.duty(0) # don't produce a sound

blue_led = Pin(18, Pin.OUT)
red_led = Pin(19, Pin.OUT)

sck = 15
cs = 2    
so = 4
thermocouple = MAX6675(cs, sck, so)

def main():
    
    
    while True:
        #clear the screen
        oled.fill(0)
        
        # read temperature
        temp = thermocouple.read_temp()
        
        text = "{:.2f}C".format(temp)
        
        # show temperature
        oled.text("-" * 16, 0, 10)
        oled.text("Temperature:", 0, 20)
        oled.text(text, 0, 30)
        print("Temperature", text)
        
        if (temp >= 90): # if temperature is 90 or greater, turn on red led and play a sound for half second
            red_led.on()
            blue_led.off()
            buzzer.duty(5)
            time.sleep(.5)
            buzzer.duty(0)
            red_led.off()
            oled.text("PLEASE STOP!!!", 0, 40)
        elif (temp > 75): # if temperature is greater than 75, turn on blue led
            red_led.off()
            blue_led.on()
            buzzer.duty(0)
            oled.text("HIGH TEMPERATURE", 0, 40)
        else:
            blue_led.off()
            red_led.off()
            buzzer.duty(0)
            oled.text("OK", 0, 40)
            
        oled.text("-" * 16, 0, 50)
        oled.show()

        # when there are some errors with sensor, it return "-" sign and CS pin number
        # in this case it returns "-22"    
        time.sleep(1)

if __name__ == "__main__":
    main()
