from machine import I2C, PWM, Pin
import network, time, urequests
from max6675 import MAX6675
from ssd1306 import SSD1306_I2C
from oled_image import find_image
from api import api

def connect_wifi(connection, password) -> boolean:
      global my_network
      my_network = network.WLAN(network.STA_IF)
      if not my_network.isconnected(): # if it is not connected
          my_network.active(True) # activate interface
          my_network.connect(connection, password) # try to connect to network
          print('Connecting to Wifi', connection +"…")
          timeout = time.time()
          while not my_network.isconnected(): #while it's not connected
              if (time.ticks_diff(time.time(), timeout) > 10):
                  return False
      return True
    
wifi_connection = "Claro_61039A"
password = "M5C9A3W7P3W8"

# setup the oled
width = 128 # oled width
height = 64 # oled height
i2c = I2C(0, scl = Pin(22), sda = Pin(21))
oled = SSD1306_I2C(width, height, i2c)

# setup the buzzer
buzzer = PWM(Pin(32), freq = 500)
buzzer.duty(0) # don't produce a sound

# setup the blue and red leds
blue_led = Pin(18, Pin.OUT)
red_led = Pin(19, Pin.OUT)

# setup the thermocuple with MAX6675 module
sck = 15
cs = 2
so = 4
thermocouple = MAX6675(cs, sck, so)

#shows a welcome message
oled.fill(0)  #limpiar
oled.blit(find_image("images/welcome.pbm"), 0, 0)
oled.show()  #mostrar
time.sleep(2)

api = api() # starts api

# image paths
normal_temp_path = "images/temperature.pbm"
warning_temp_path = "images/warning.pbm"
high_temp_path = "images/fire.pbm"

# the method that will be executed at 
def main():
    if connect_wifi(wifi_connection, password): # connect to wifi
        oled.fill(0)
        oled.blit(find_image("images/check.pbm"), 0, 0)
        oled.text("Connected", 55, 20)
        oled.show()
        
        print ("Conexión exitosa!")
        print('Datos de la red (IP/netmask/gw/DNS):', my_network.ifconfig())
        
        time.sleep(1.5)
        
        while True:
            #clear the screen
            oled.fill(0)
            
            # read temperature
            # when there are some errors with sensor, it return "-" sign and CS pin number
            # in this case it returns "-22"
            temp = thermocouple.read_temp()
            
            # format the temperature
            text = "{:.2f} C".format(temp)                      
            
            if (temp >= 90): # if temperature is 90 or greater, turn on red led and play a sound for half second
                red_led.on()
                blue_led.off()
                buzzer.duty(5)
                time.sleep(.5)
                buzzer.duty(0)
                red_led.off()
                oled.blit(find_image(high_temp_path), 0, 0)
            elif (temp > 75): # if temperature is greater than 75, turn on blue led
                red_led.off()
                blue_led.on()
                if (buzzer.duty() != 0):
                    buzzer.duty(0)
                oled.blit(find_image(warning_temp_path), 0, 0)
            else: # temperature is normal
                blue_led.off()
                red_led.off()
                if (buzzer.duty() != 0):
                    buzzer.duty(0)
                oled.blit(find_image(normal_temp_path), 0, 0)
                
            oled.text(text, 55, 20) 
            oled.show()
            print("Temperature", text)
            api.graph_temp(temp)
            
            if (temp >= 90): # send an alert if temperature is more than 90°C
                api.send_email(temp)
                
            time.sleep(1)
    else: # if it is not connected
        oled.fill(0)
        oled.blit(find_image("images/error.pbm"), 0, 0)
        oled.text("Can't", 60, 20)
        oled.text("connect", 60, 30)
        oled.show()
        print("Can't connect :(")
        my_network.active(False)
    

if __name__ == "__main__":
    main()
