keithley1="com3"
keithley2="com4"


from mathtools import *
import vme as vme
import keithleyV4 as k
import time

k1=k.initialize_Keithley2401(keithley2)
#k2=k.initialize_Keithley2401(keithley2)

Vsrc='0V'
k.outputOFF(k1)
k.source_V(k1,Vsrc,0.4)
k.outputOFF(k1)

time.sleep(0.1)
k.source_V(k1,"0.1",0.4)
k.outputON(k1)

k.measure_V(k1)
k.measure_I(k1)

time.sleep(1)
