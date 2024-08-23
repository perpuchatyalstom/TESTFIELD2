import serial
import csv
from mathtools import *

def initialize_Keithley2401(port_name,baudrate=9600):
	try:
		ser = serial.Serial(port_name, baudrate=baudrate, timeout=1)
		return ser
	except serial.SerialException as e:
		#print("Error:", e)
		return "Error:", e

def device_info(ser):
    ser.write(b'*IDN?\r\n')
    resp = ser.readline().decode().strip()
    if resp == '':
        resp = 'port -> {} <- not connected to a device'.format(ser.port.upper())
    else:
        if 'KEITHLEY' in resp[:8]:
            tmp=resp.split(',')
            resp='KEITHLEY\n{}\nserienr: {}'.format(tmp[1],tmp[2])
    return resp

def send_beep_on(ser):
    ser.write(b':SYSTEM:BEEP:STATE ON\n')
    ser.write(b':system:KEY 23\r')

def beep_off(ser):
    ser.write(b':SYSTEM:BEEP:STATE OFF\n')
    ser.write(b':system:KEY 23\r')

def remoteOFF(ser):
    ser.write(b':system:KEY 23\r')

def outputON(ser):
    ser.write(b':OUTP ON\n')
    ser.write(b':system:KEY 23\r')

def outputOFF(ser):
    ser.write(b':OUTP OFF\n')
    ser.write(b':system:KEY 23\r')

def checkOutput(ser):
    ser.write(b':OUTPut?\r')
    ser.write(b':system:KEY 23\r')
    return ser.readline().decode().strip()
        
def send_command_and_read_response(ser,command):
    try:
        ser.write(command.encode())
        response = ser.readline().decode().strip()
        return response
    except serial.SerialException as e:
        print("Error:", e)
        return None

def send_command(ser,command):
    ser.write(command)
    return 

def source_I(ser,Iin,Vrng):
    outState='off'
    if checkOutput(ser) != 0:
        outState='on'
    Iin=unit2number(Iin)
    Vrng=unit2number(Vrng)

    Vprot = Vrng * 1.5
    Vrng = Vrng * 1.1

    ser.write(b':SOURCE:FUNC CURR\n')
    outputON(ser)
    if outState=='on':
        outputON(ser)
    ser.write(b':SOURCE:CURR:MODE FIX\n') 
    ser.write(b':SOURCE:CURR:RANGE:AUTO ON\n')    
    ser.write(':SOURCE:CURR:LEV {}\n'.format(Iin))
    ser.write(b':SENSE:FUNC "VOLT"\n' ) 
    ser.write(b':SENSE:VOLT:PROT {}\n'.format(Vprot))
    ser.write(b':SENSE:VOLT:RANGE {}\n'.format(Vrng))
    ser.write(':SENS:VOLT:DC:RANGE?\r\n')
    rng = float(ser.readline().decode().strip())
    ser.write(':SENS:VOLT:DC:prot?\n')
    prt = float(ser.readline().decode().strip())
    remoteOFF(ser)
    return rng,prt

def set_I(ser,inp):
    Iin=unit2number(inp)
    ser.write(':SOURCE:CURR:LEV {}\r\n'.format(Iin))
    remoteOFF(ser)

def source_V(ser,Vin,Irng):
    outState = 'off' if checkOutput(ser) != 0 else 'on'

    ser.write(b':source:func:mode?\r\n')
    resp = ser.readline().decode().strip()
    if resp == 'CURR':
        # output is switched from current to voltage mode
        outState='off'
    Vin=unit2number(Vin)
    Irng=unit2number(Irng)
    Iprot = Irng * 1.5
    Irng = Irng * 1.1
    ser.write(b':SOURCE:FUNC VOLT\n')
    ser.write(b':SOURCE:VOLT:MODE FIX\r\n')
    ser.write(b':SOURCE:VOLT:RANGE:AUTO ON\r\n')
    ser.write(b':SOURCE:VOLT:LEV {}\r\n'.format(Vin))
    ser.write(b':SENSE:FUNC "CURR"\r\n')
    ser.write(b':SENSE:CURR:PROT {}\r\n'.format(Iprot))
    ser.write(b':SENSE:CURR:RANGE {}\r\n'.format(Irng))
    ser.write(b':SENSE:CURR:DC:RANGE?\r\n')
    rng = float(ser.readline().decode().strip())
    if outState=='on':
        outputON(ser)  
    remoteOFF(ser)

def set_V(ser,inp):
    Iin=unit2number(inp)
    ser.write(':SOURCE:VOLT:LEV {}\r\n'.format(Iin))
    remoteOFF(ser)

def measure_V(ser):
    if checkOutput(ser) == '0':
        return
    ser.write(b':OUTPut?\r\n')
    resp = float(ser.readline().decode().strip())
    if resp == '0':
        return 'Can only measure with OUTPUT swiched on'
    ser.write(b':SENSE:FUNC "VOLT"\r\n')
    ser.write(':READ?\r\n')
    response = ser.readline().decode().strip()
    values = response.split(",")
    response = number2unit(values[0],v)
    remoteOFF(ser)
    return response

def measure_I(ser):
    if checkOutput(ser) == '0':
        return
    ser.write( b':OUTPut?\r\n')
    resp = float(ser.readline().decode().strip())
    if resp == '0':
        return 'Can only measure with OUTPUT swiched on'
    ser.write(':SENSE:FUNC "CURR"\r\n')
    ser.write(':READ?\r\n')
    response = ser.readline().decode().strip()
    values = response.split(",")
    response = number2unit(values[1],A)
    remoteOFF(ser)
    return response

def helpFunctions():
    print ("#####################################################")
    print ("Functioncalls available in module keithley.py" )
    print ("modify_portname(com)")
    print ("modify_baudrate(speed)")
    print ("device_info()")
    print ("send_command(command)")
    print ("send_command_and_read_response(command)")
    print ("send_beep_on()")
    print ("send_beep_off()")
    print ("def measure_V()")
    print ("source_I_measure_V(Iin,Vrng,power=\'OFF\')")
    print ("source_V_measure_I(Vin,Irng,Iprot=1.05,power=\'off\')")

