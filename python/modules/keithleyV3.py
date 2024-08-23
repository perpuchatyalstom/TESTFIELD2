import serial
from mathtools import *

global ser1
global ser2
ser1=''
ser2=''

def initialize_Keithley2401(port,baudrate=9600):
    global ser1
    global ser2

    if port == 'com3':        
        if ser1 != '':            
            ser1.close()
            ser1=''
    if port == 'com4':
        if ser2 != '':
            ser2.close()
            ser2=''
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=1)
    except serial.SerialException as e:
        ser="Error:, {}".format(e)

    if port == 'com3':
        ser1=ser
    if port == 'com4':
        ser2=ser
    if 'Access is denied' in str(ser):
         return'Error: Access is denied, release serial port: ' + port
    if not 'KEITHLEY' in device_info(ser):
        return 'Error: No Keitley 2401 found'
        

    return ser

def device_info(ser):
    ser.write(b'*IDN?\r\n')
    #ptint information about serial port:
    resp = ser.readline().decode().strip()
    if resp == '':
        resp = 'port -> {} <- no Keithley'.format(ser.port.upper())
    else:
        if 'KEITHLEY' in resp[:8]:
            print "this is response from device info: ",resp
            tmp=resp.split(',')
            resp='KEITHLEY\n{}\nserienr: {}'.format(tmp[1],tmp[2])
        else:
             resp= 'Fail'
    return resp

def outputON(ser):
    ser.write(b':OUTP ON\n')
    ser.write(b':system:KEY 23\r')

def outputOFF(ser):
    ser.write(b':OUTP OFF\n')
    ser.write(b':system:KEY 23\r')

def remoteOFF(ser):
    ser.write(b':system:KEY 23\r')

def send_beep_on(ser):
    ser.write(b':SYSTEM:BEEP:STATE ON\n')
    ser.write(b':system:KEY 23\r')

def beep_off(ser):
    ser.write(b':SYSTEM:BEEP:STATE OFF\n')
    ser.write(b':system:KEY 23\r')

def checkOutput(ser):
    resp =  ser.readline().decode().strip()
    ser.write(b':OUTPut?\r')
    resp =  ser.readline().decode().strip()
    ser.write(b':system:KEY 23\r')
    return resp

def source_I(ser,Iin,Vrng):
    Iin=unit2number(Iin)
    Vrng=unit2number(Vrng)

    Vprot = Vrng * 1.5
    Vrng = Vrng * 1.1

    ser.write(b':SOURCE:FUNC CURR\n')
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
    remoteOFF(ser)

def set_V(ser,inp):
    Iin=unit2number(inp)
    ser.write(':SOURCE:VOLT:LEV {}\r\n'.format(Iin))
    remoteOFF(ser)

def measure_V(ser):
    if checkOutput(ser) == '0':
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
        return 'Can only measure with OUTPUT swiched on'
    ser.write(':SENSE:FUNC "CURR"\r\n')
    ser.write(':READ?\r\n')
    response = ser.readline().decode().strip()
    values = response.split(",")
    response = number2unit(values[1],'A')
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


