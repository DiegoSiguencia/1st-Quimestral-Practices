import network
import espnow
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
import time

EN = espnow.ESPNow()
EN.active(True)

EN.add_peer(b'\x24\x6F\x28\xA2\x15\x9C')

I2C_ADDR = 0x27
totalRows = 4
totalColums = 20
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=4000000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColums)

lcd.backlight_off()

while True:
    host, message = EN.recv()
    mensaje_deco = message.decode('utf-8')
    if mensaje_deco == 'ON':
        lcd.backlight_on()
    elif mensaje_deco == 'OFF':
        lcd.backlight_off()