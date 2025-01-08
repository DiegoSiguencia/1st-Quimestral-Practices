import network
import espnow
from machine import Pin
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

EN = espnow.ESPNow()
EN.active(True)

mac = b'\x24\xdc\xc3\x46\xac\x5c'  # Cambia por la MAC del receptor

EN.add_peer(mac)

b1 = Pin(12, Pin.IN, Pin.PULL_UP)
b2 = Pin(14, Pin.IN, Pin.PULL_UP)

def send_message(text):
    try:
        mensaje = text
        mensaje_bytes = mensaje.encode('utf-8')
        EN.send(mac, mensaje_bytes)
    except Exception as e:
        print("Error al enviar mensaje:", e)
while True:
    if b1.value() == 0:
        print("1")
        send_message('ON') 
        time.sleep(1)  
    if b2.value() == 0:
        print("0")
        send_message('OFF') 
        time.sleep(1)