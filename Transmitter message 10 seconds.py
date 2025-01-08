import network
import espnow
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
import time

I2C_ADDR = 0x27
totalRows = 4
totalColums = 20
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=4000000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColums)

Del = Pin(13, Pin.IN, Pin.PULL_UP)
red = network.WLAN(network.STA_IF)
red.active(True)
EN = espnow.ESPNow()
EN.active(True)
mac = b'\x24\xdc\xc3\x46\xac\x5c'
EN.add_peer(mac)
Bu = Pin(12, Pin.IN, Pin.PULL_UP)
Bd = Pin(14, Pin.IN, Pin.PULL_UP)
Br = Pin(27, Pin.IN, Pin.PULL_UP)
Bl = Pin(26, Pin.IN, Pin.PULL_UP)
Snd = Pin(25, Pin.IN, Pin.PULL_UP)
a = 0
Ord = 0
col = 0
vel = 0.009
screen_state = [[" "] * totalColums for _ in range(totalRows)]

def ADP(row, col, text):
    global vel, screen_state
    for i, char in enumerate(text):
        if col + i < totalColums:
            if screen_state[row][col + i] != char:
                lcd.move_to(col + i, row)
                lcd.putstr(char)
                screen_state[row][col + i] = char
                sleep(vel)

def Msj():
    global a
    ADP(1, col, chr(ord("a") + a))

def Lt_up():
    global Ord, a
    if Ord != 1:
        Ord = 1
    a += 1
    if a == 26:
        a = 0
    Msj()    
    sleep(0.25)
        
def Lt_down():
    global Ord, a
    if Ord != 1:
        Ord = 1
    a -= 1
    if a == -1:
        a = 25
    Msj()
    sleep(0.25)
        
lcd.move_to(0, 0)
lcd.putstr("Msj Tr #1:")
lcd.move_to(0, 1)
lcd.putstr("a")
lcd.show_cursor()

while True:
    if Bu.value() == 0:
        Lt_up()
    if Bd.value() == 0:
        Lt_down()
    if Br.value() == 0:
        col += 1
        if col == 20:
            col = 19
        lcd.move_to(col, 1)
        lcd.show_cursor()
        a = 0
        sleep(0.25)
    if Bl.value() == 0:
        col -= 1
        if col == -1:
            col = 0
        lcd.move_to(col, 1)
        lcd.show_cursor()
        a = 0
        sleep(0.25)
    if Snd.value() == 0:
        # Convierte screen_state a cadena y luego a bytes
        mensaje = '\n'.join(["".join(row) for row in screen_state])
        mensaje_bytes = mensaje.encode('utf-8')
        EN.send(mac, mensaje_bytes)
        
        # Muestra "mensaje enviado" en la primera fila
        lcd.move_to(0, 0)
        lcd.putstr("mensaje enviado   ")
        
        # Borra la segunda fila (mensaje editado)
        lcd.move_to(0, 1)
        lcd.putstr(" " * totalColums)
        
        # Espera de 3 segundos antes de restaurar el texto inicial
        sleep(3)
        
        # Restaura el texto inicial en la primera fila
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Msj Tr #1:")
        lcd.move_to(0, 1)
        lcd.putstr("            ")
        sleep(0.05)
        lcd.move_to(0, 1)
        lcd.putstr("a")
        lcd.show_cursor()