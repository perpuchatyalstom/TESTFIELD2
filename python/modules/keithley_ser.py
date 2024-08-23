import serial
import csv

port_name="COM3"
baudrate="9600"

def modify_portname(com):
    global port_name
    port_name = com

def modify_baudrate(speed):
    global baudrate
    baudrate = speed

def device_info():
    command = b'*IDN?\r\n'
    resp=send_command_and_read_response(command)
    if resp == '':
        resp = 'port not connected to a device'
    else:
        if 'KEITHLEY' in resp[:8]:
            tmp=resp.split(',')
            resp='KEITHLEY\n{}\nserienr: {}'.format(tmp[1],tmp[2])
    return resp


def send_beep_on():
    command = b':SYSTEM:BEEP:STATE ON\r\n'
    send_command(command)
def send_beep_off():
    command = b':SYSTEM:BEEP:STATE OFF\r\n'
    send_command(command)
   
def send_command_and_read_response(command):
    try:
        ser = serial.Serial(port_name, baudrate=baudrate, timeout=1)
        # Send the RS232 command
        ser.write(command.encode())
        # Read the response
        response = ser.readline().decode().strip()
        # Close the serial port
        ser.close()

        return response
    except serial.SerialException as e:
        print("Error:", e)
        return None

def send_command(command):
    try:
        ser = serial.Serial(port_name, baudrate=baudrate, timeout=1)
        # Send the RS232 command
        ser.write(command)
        # Close the serial port
        ser.close()
        return 
    except serial.SerialException as e:
        print("Error:", e)
        return None
    
def source_I_measure_V(Iin,Vrng,power='OFF'):
    Vprot = Vrng * 1.5
    Vrng = Vrng * 1.1
    if power.upper() != 'OFF': power='ON'
    command = b'*RST\r\n'  
    send_command(command)
    command = b':SOURCE:FUNC CURR\r\n'  
    send_command(command)
    command = b':SOURCE:CURR:MODE FIX\r\n'  
    send_command(command)
    command = b':SOURCE:CURR:RANGE:AUTO ON\r\n'    
    send_command(command)
    command = ':SOURCE:CURR:LEV {}\r\n'.format(Iin)
    send_command(command.encode())
    command = b':SENSE:FUNC "VOLT"\r\n'  
    send_command( command)
    command = b':SENSE:VOLT:PROT {}\r\n'.format(Vprot)
    send_command( command)
    command = b':SENSE:VOLT:RANGE {}\r\n'.format(Vrng)
    send_command( command)

    command = ':SENS:VOLT:DC:RANGE?\r\n'
    rng = float(send_command_and_read_response(command))
    command = ':SENS:VOLT:DC:prot?\r\n'
    prt = float(send_command_and_read_response(command))
    command = b':OUTP ON\r\n'  
    send_command(command)

    command = ':READ?\r\n'
    response = send_command_and_read_response( command)


    command = b':OUTP {}\r\n'.format(power)
    send_command(command)
    
    values = response.split(",")
    response = values[0] + ',' + values[1] + ',RANGE=' + str(rng) + ',PROT='+ str(prt)

    return response

def source_V_measure_I(Vin,Irng,Iprot=1.05,power='off'):
    command = b'*RST\r\n'  
    send_command(command)
    send_beep_off()
    command = b':SOURCE:FUNC VOLT\r\n'  
    send_command(command)
    command = b':SOURCE:VOLT:MODE FIX\r\n'  
    send_command(command)
    command = b':SOURCE:VOLT:RANGE:AUTO ON\r\n'  
    send_command(command)
    command = ':SOURCE:VOLT:LEV {}\r\n'.format(Vin)
    send_command(command.encode())
    command = b':SENSE:FUNC "CURR"\r\n'  
    send_command( command)
    command = b':SENSE:CURR:PROT {}\r\n'.format(Iprot)
    send_command( command)
    command = b':SENSE:CURR:RANGE {}\r\n'.format(Irng)
    send_command( command)
    command = ':SENSE:CURR:DC:RANGE?\r\n'
    rng = send_command_and_read_response(command)
    
    command = b':OUTP ON\r\n'  
    send_command(command)

    command = ':READ?\r\n'
    response = send_command_and_read_response(command)

    if power.lower() == 'on':
        command = b':OUTP ON\r\n'  
    else:
       command = b':OUTP OFF\r\n'
    send_command(command)
    
    values = response.split(",")
    response = values[0] + ',' + values[1] + ',Irng=' + rng

    return response
