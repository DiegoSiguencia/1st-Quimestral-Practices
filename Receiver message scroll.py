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
red = network.WLAN(network.STA_IF)
red.active(True)
EN = espnow.ESPNow()
EN.active(True)
macemisor = b'\xc8\xf0\x9e\x25\x08\xe8'
EN.add_peer(macemisor)

a = 0
Act = 0
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
                
def mostrar(mensaje):
    a = 0
    fa = 0
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("mensaje:")
    mensaje_limpio = "\n".join(line.strip() for line in mensaje.splitlines() if line.strip())
    lcd.move_to(0, 1)
    lcd.putstr("                  ")
    sleep(0.05)
    lcd.move_to(a, 1)
    lcd.putstr(mensaje_limpio[:totalColums])  # Muestra el mensaje en la segunda fila
    sleep(0.25)
    if mensaje_limpio[:totalColums] == 'Andres Siguencia':
        while True:
            lcd.move_to(18,1)
            lcd.putstr(str(fa))
            fa += 1
            sleep(0.25)
            if fa == 11:
                lcd.clear()
                lcd.move_to(0,0)
                lcd.putstr('mensaje:')
                lcd.move_to(0,1)
                lcd.putstr('Andres Siguencia')
                break
        while True:
            while True:
                ADP(1, a, "Andres Siguencia")
                ADP(1, a+16, "   ")
                sleep(0.10)
                a -= 1
                if a == -17:
                    a = 21
                    break
            while True:
                ADP(1, a, "Ayala Carlos")
                ADP(1, a+12, " ")
                sleep(0.15)
                a -= 1
                if a == -17:
                    a = 19
                    break

def recibir():
    a = 1
    while True:
        host, mensaje = EN.recv()
        if mensaje and host == macemisor:
            mensaje_deco = mensaje.decode('utf-8')
            print(f"Mensaje {a} recibido:", mensaje_deco)  # Verificar en consola
            mostrar(mensaje_deco)  # Llama a la función para mostrar el mensaje en pantalla LCD
            a += 1
lcd.move_to(0, 0)
lcd.putstr("mensaje:")
recibir()