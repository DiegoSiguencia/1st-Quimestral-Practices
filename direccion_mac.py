import network
red = network.WLAN(network.STA_IF)
red.active(True)
Mac = red.config('mac')
Mc_E32= ':'.join(['{:02x}'.format(b) for b in Mac])
Mc_ENow= ''.join([r'\x{:02x}'.format(b) for b in Mac])
print(f"Direccion MAC Esp32: '{Mc_E32}'")
print(f"Direccion MAC en formato EspNow: b'{Mc_ENow}'")
