import serial
import os

# System call
os.system("")
base_address=0

#Set base address in HEX. For example 0x0c00000. You can do this only once, later when script is running it will use global variable
def set_base_address(address):
    global base_address
    base_address=address

#Send byte function. 
#vme.wb(0x810,"AA",ser)
#Address: has to be in HEX format:0x800. Base address is added to this address, if baseadres is not used, full adress need to be passed here
#Byte: Byte to send in format like this: "01" or "AB" or "12"
#Serial_port: opened serial port class.
#Return: True if sending was successful
def wb(address,byte,serial_port):
 # Ensure byte is in hexadecimal format
    if not isinstance(byte, str):
        raise ValueError("Byte should be a hexadecimal string (e.g., '12').")
    if len(byte) == 1:
        byte = '0' + byte
    full_address=base_address+address
    #Send string over serial
    serial_port.write("wb {:08X} {:02X}\r\n".format(full_address,word).encode())
    #serial_port.write(f"wb {full_address:08x} {byte}\r\n".encode())
    #Clear serial buffer
    response = serial_port.readline().decode().strip()
    response = serial_port.readline().decode().strip()
    #Look for correct string in serial buffer
    if(response!="Written: 0x{byte.upper()} at Addr 0x{full_address:08X}"):
        ret=True
    else:
        ret=False
    response = serial_port.readline().decode().strip()
    response = serial_port.readline().decode().strip()
    return ret

#Send word function. 
#vme.wb(0x810,"AA",ser)
#Address: has to be in HEX format:0x800. Base address is added to this address, if baseadres is not used, full adress need to be passed here
#Word: Byte to send in format like this: "1" or "AB" or "aa12"
#Serial_port: opened serial port class.
#Return: True if sending was successful

def ww(address,word,serial_port):
 # Ensure byte is in hexadecimal format
    if not isinstance(word, str):
        raise ValueError("Byte should be a hexadecimal string (e.g., '12').")
    if len(word) == 1:
        word = '000' + word
    full_address=base_address+address
    #Send string over serial
    serial_port.write("ww {:08x} {}\r\n".format(full_address,word).encode())
    #serial_port.write(f"ww {full_address:08x} {word}\r\n".encode())
    #Clear serial buffer
    response = serial_port.readline().decode().strip()
    response = serial_port.readline().decode().strip()
    #Look for correct string in serial buffer
    if(response!="Written: 0x{byte.upper()} at Addr 0x{full_address:08X}"):
        ret=True
    else:
        ret=False
    response = serial_port.readline().decode().strip()
    response = serial_port.readline().decode().strip()
    return ret   

#Read byte function 
#vme.rb(0x810,ser)
#Address: has to be in HEX format:0x800. Base address is added to this address, if baseadres is not used, full adress need to be passed here
#Serial_port: opened serial port class.
#Debug: if set to true, it will show all messages from serial port
#Return: Byte from address as integer

def rb(address,serial_port, debug=False):
    full_address=base_address+address
    #Send string over serial
    serial_port.write("rb {:08x}\r\n".format(full_address).encode())
    #serial_port.write(f"rb {full_address:08x}\r\n".encode())
    #Clear serial buffer
    response = serial_port.readline().decode().strip()
    if(debug==True): print(response)
    response = serial_port.readline().decode().strip()
    if(debug==True): print(response)
    response = serial_port.readline().decode().strip()
    if(debug==True): print(response)
    # Extract the byte from the second response
    byte_response = response.split(":")[1].strip()
    byte_as_int = int(byte_response, 16)
    response = serial_port.readline().decode().strip()
    if(debug==True): print(response)
    response = serial_port.readline().decode().strip()
    if(debug==True): print(response)
    if(debug==True): print("Return: {}").format(byte_as_int)
    #if(debug==True): print(f"Return: {byte_as_int}")
    # Return the byte as an integer
    return byte_response

#Read word function 
#vme.rw(0x810,ser)
#Address: has to be in HEX format:0x800. Base address is added to this address, if baseadres is not used, full adress need to be passed here
#Serial_port: opened serial port class.
#Debug: if set to true, it will show all messages from serial port
#Return: Word from address as integer
def rw(address,serial_port, debug=False):
    full_address=base_address+address
    #Send string over serial
    serial_port.write("rw {:08x}\r\n".format(full_address).encode())
    #serial_port.write(f"rw {full_address:08x}\r\n".encode())
    #Clear serial buffer
    response = serial_port.readline().decode().strip()
    if(debug==True): print(response)
    response = serial_port.readline().decode().strip()
    if(debug==True): print(response)
    response = serial_port.readline().decode().strip()
    if(debug==True): print(response)
    # Extract the byte from the second response
    if response!='':
        byte_response = response.split(":")[1].strip()
    else:
         byte_response='0x0000'
    byte_as_int = int(byte_response, 16)
    response = serial_port.readline().decode().strip()
    if(debug==True): print(response)
    response = serial_port.readline().decode().strip()
    if(debug==True): print(response)
    if(debug==True): print("Return: {}").format(byte_as_int)
    #if(debug==True): print(f"Return: {byte_as_int}")
    # Return the byte as an integer
    return byte_response

def rw1(address,serial_port, debug=False):
    response=[]
    full_address=base_address+address
    #Send string over serial
    serial_port.write("rw {:08x}\r\n".format(full_address).encode())
    #serial_port.write(f"rw {full_address:08x}\r\n".encode())
    #Clear serial buffer
    resp = serial_port.readline().decode().strip().lower()

    while resp != '>':
        response.append(resp)
        resp = serial_port.readline().decode().strip()
    if(debug==True): print(response,len(response))
    if len(response)>7:
        #print ('sysfail')
        return 'sysfail'
    if len(response)==3:
        return response[2].split(':')[1].strip()
    if len(response)==4:
        return response[3].split(':')[1].strip()

def emptyBuffer(serial_port, debug=False):
    resp=serial_port.readall()
    if debug:
        print ('emptyBuffer',resp)

#ser_mpr6 = serial.Serial('com4', 9600, timeout=1)
#set_base_address(0x0c000000)

#address = 0x0800
#ww(address ,'aaaa',ser_mpr6)
#print 'ww {:04x} {}'.format(address,'AAAA')

#print rw2(0x08480,ser_mpr6)


#ser_mpr6.close()