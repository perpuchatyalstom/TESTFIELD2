import visa
import time
from mathtools import *

#instr_resource = "USB0::0x1AB1::0x0515::MS5A250801032::INSTR"
#instr_resource = "USB0::0x1AB1::0x0644::DG2P214600230::INSTR"
#instr_resource = "USB0::0x1AB1::0x0515::MS5A251102184::INSTR"
rm = visa.ResourceManager()
#print (rm.list_resources())
#instr = rm.open_resource(instr_resource)

def initialize_mso5204():
    #rm = visa.ResourceManager()
    #print(rm.list_resources())
    resource_name = "USB0::0x1AB1::0x0515::MS5A251102184::INSTR"
    # Establish connection
    mso5204 = rm.open_resource(resource_name)
    return mso5204

def initialize_dg2052():
    #rm = visa.ResourceManager()
    #print(rm.list_resources())
    resource_name = "USB0::0x1AB1::0x0644::DG2P214600230::INSTR"
    # Establish connection
    dg2052 = rm.open_resource(resource_name)
    return dg2052


def send_command(command):
    instr.write(command)

def read_command(command):
    return instr.query(command)

def end():
    command=':MEASure:STATistic:DISPLAY OFF'
    instr.write(command)
    instr.close

def channel(ch,volt,offset=0,on=1):
    on = 1 if on == 1 else 0
    command=":CHANnel{}:DISPlay {}".format(ch,on)
    send_command ( command)
    command=":CHANnel{}:OFFSet {}".format(ch,offset)
    send_command ( command)
    command = ':CHANnel{}:SCALe {}'.format(ch,volt)
    send_command ( command)

def timebase(scale,pos=50):
    scale = unit2number(scale)
    #scale = scale[:-1] if mult == 1 else scale[:-2]
    #scale = float(scale)*mult
    command=":TIMebase:MODE MAIN"
    send_command ( command)
    command=":TIMebase:SCALE {}".format(scale)
    send_command ( command)
    command = ':TIMebase:POSition {}'.format(pos)
    send_command ( command)

def trigger(ch,level,edge='EDGE',slope='POSitive'):
    command=":TRIGger:EDGE:SOURce CHAN{}".format(ch)
    send_command ( command)
    command=":TRIGger:EDGE:MODE {}".format(edge)
    send_command ( command)
    command=":TRIGger:EDGE:SLOPe {}".format(slope)
    send_command ( command)
    command=":TRIGger:EDGE:LEV {}".format(level)
    send_command ( command)

def FG(ch,freq,level,offset=0,func='SIN',phase=0,on=1):
    on = 1 if on == 1 else 0
    if on==0:
        command=":OUTPUT {}:STATE OFF".format(ch)
        send_command ( command)
        return
    #command=":OUTPUT {}:STATE OFF".format(ch)
    #send_command ( command)
    command=":SOURce{}:APPLY:SIN {},{},{},{}".format(ch,freq,level,offset,phase)
    send_command ( command)
    command=":SOURce{}:OUTPut:STATe {}".format(ch,on)
    send_command ( command)

def counterRead(ch,wait=3,mode = 'FREQ',enable = 'ON'):
    #very slow measurement. Use measure function
    mode = 'FREQ' if mode == 'FREQ' else 'PER'
    enable = 'ON' if enable == 'ON' else 'OFF'
    command=":counter:source chan{}".format(ch)
    send_command (command)
    if enable == 'ON':
        command=":counter:mode {}".format(mode)
        send_command (command)
        command=":counter:enable {}".format(enable)
        send_command (command)
        time.sleep(wait)
        command=":counter:current?"
        result = instr.query(command) 
    else:
        command=":counter:enable {}".format(enable)
        send_command (command) 
        result = 'channel{} switched off'.format(ch)
    return result

def measure(ch,item='FREQ',stat = 'none',aver=3):
    items=['FREQ','PER','VRMS','VAMP']
    unit=['Hz','s','Vrms','V']

    #print unit[items.index(item)]
    if item.upper() not in items:
        result = 'item [{}] not in list:{}'.format(item,items)
        return number2unit(result,unit[items.index(item)])
    #command=':ACQuire:AVERages 4'
    #send_command(command)
    #command=':ACQuire:AVERages?'
    #print instr.query(command)
    command=':MEASure:source CHAN{}'.format(ch)
    instr.write(command)
    if stat == 'STAT':
        cnt=0
        while cnt < aver:
            command=':MEASure:STATistic:ITEM? cnt,{}'.format(item.upper())
            cnt=float(instr.query(command))
        #print float(aver)
        command=':MEASure:STATistic:ITEM {},CHAN{}'.format(item,ch)
        instr.write(command)
        #time.sleep(1)
        command=':MEASure:STATistic:ITEM? AVER,{}'.format(item.upper())
        instr.write(command)
    else:
        command=':MEASure:ITEM {},CHAN{}'.format(item,ch)
        instr.write(command)
        command=':MEASure:ITEM? {},CHAN{}'.format(item,ch)

    result = number2unit(instr.query(command),unit[items.index(item.upper())])

    # command=':MEASure:STATistic:DISPLAY OFF'
    # instr.write(command)
    return result

def timing(ch1,ch2,ch1Edge='UP',ch1Lev=0,ch2Edge='UP',ch2Lev=0):
    #to be figures out

    command = ':MEASure:SOURce channel1'
    send_command(command)
    command = ':MEASure:SETup:PSA CHANnel{}'.format(ch1)
    send_command(command)
    command = ':MEASure:SETup:DSA CHANnel{}'.format(ch1)
    send_command(command)

    command = ':MEASure:SETup:PSB CHANnel{}'.format(ch2)
    send_command(command)
    command = ':MEASure:SETup:PSB?'
    send_command(command)
    command = ':MEASure:SETup:DSB CHANnel{}'.format(ch2)
    send_command(command)
    command = ':MEASure:SETup:DSB?'
    send_command(command)

    # command = ':MEASure:SETup:DSA?'
    # print read_command(command)
    # command = ':MEASure:SETup:PSA?'
    # print read_command(command)
    # time.sleep(5)
    # command = ':MEASure:SOURce?'
    # return read_command(command)


def timeDelayCh1Ch2(ch1,ch2,mode='EDGE',slope='POS'):
    command = ':SEARch:STATe 1'    
    send_command(command)
    command = ':SEARch:MODE EDGE'
    send_command(command)
    command = ':SEARch:EDGE:slope pos'
    send_command(command)
    command = ':SEARch:EDGE:source 1'
    send_command(command)
    command = ':SEARch:EDGE:THReshold 0.5'
    send_command(command)
    command = ':SEARch:event 1'
    send_command(command)

    command = 'SINGLE' 
    send_command(command)
    command = '*OPC?' 
    send_command(command)

    command = ':SEARch:event?'
    printcommand(command)
    print ('\n#################')
    command = ':SEARch:value?'
    val = read_command(command)
    return val

def printcommand(command):
    print (read_command(command))

def simpletiming(ch1,ch2):

    command = ':MEASurement:IMMed:SOUrce1 CHAN{}'.format(ch1)
    send_command(command)
    command = ':MEASurement:IMMed:SOUrce2 CHAN{}'.format(ch2)
    send_command(command)
    command = ':MEASurement:IMMed:TYPe DELAY' 
    send_command(command)

    command = 'SINGLE' 
    send_command(command)
    command = '*OPC?' 
    send_command(command)

    command = ':MEASUREMENT:MEAS1:VALue?'
    return read_command(command)

# RIGOL DG2052 generator 

def setup_waveform(generator,source,frequency=1e3, amplitude=1.0, waveform='SIN',offset=0,phase=0,on=1):
#    on = 1 if on == 1 else 0
#    if on==0:
#        generator.write(':SOUR{}:OUTput:state off'.format(source))
    generator.write(':SOUR{}:APPL:{} {},{},{},{}'.format(source,waveform, frequency, amplitude,offset,phase))
#    if on==0:
#        generator.write(':SOUR{}:OUTput:state off'.format(source))

def outputOFF(INSTR,source=1):
    source = 1 if source == 1 else 2
    if 'DG2' in str(INSTR):
        INSTR.write(':OUTput{}:state off'.format(source))
    else:
        INSTR.write(':SOUR{}:OUTput:state off'.format(source))

def outputON(INSTR,source=1):
    source = 1 if source == 1 else 2
    if 'DG2' in str(INSTR):
        INSTR.write(':OUTput{}:state on'.format(source))
    else:
        INSTR.write(':SOUR{}:OUTput:state on'.format(source))