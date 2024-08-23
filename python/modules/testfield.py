import vme
import serial
vme.set_base_address(0x0c000000)

address = 0x0800
mpr6_serial = serial.Serial('com4', 9600, timeout=1)
vme.wb2(address ,'aa',mpr6_serial)