#addlib='C:\\ABI\\python\\modules'
#if addlib not in sys.path:
#	sys.path.append('C:\ABI\python\modules')
from mathtools import *
from datetime import datetime as dt

global testname
testname = '5.2.6 UL square-wave converter'
global instrument
instrument = 'DSO1'
global message
message = '"H1,H2,H3,H5 are ON"'

def checkLIMITSLog(inp,llim='',hlim='',usr=1):
    if inp == 'help'or inp == 'h':
        print 'Usage: ',
        print 'checkLIMITSLog(test value,low limit,high limit,userscript#)'
        print '\n\ttestname\talready defined\t(abi.testname)'
        print '\tinstrument\talready defined\t(abi.instrument)'
        print '\tmessage\t\talready defined\t(abi.message)'
        return
    # check limits
    pf = True
    loglim = [instrument,' ',inp, ' ']
    if llim == hlim == '':
        loglim = []
        if inp != 1: pf = False
        if instrument != '':
            loglim.append(instrument)
        if message != '':
            loglim.append(message)
    if llim != '':
        if unit2number(inp) < unit2number(llim): pf = False
        loglim[1] = llim
    if hlim != '':
        if unit2number(inp) > unit2number(hlim): pf = pf & False
        loglim[3] = hlim
    loglim = ','.join(loglim)
    pf = 'PASS' if pf else 'FAIL'
    time = dt.now().strftime('%H:%M:%S')
    todayABI = '19/08/2024'
    logline = '{},{},"PYT","USR{}",{},{},{},{}'.format(todayABI,time,usr,pf,testname,loglim,'\n')
    print logline
    with open('results.csv','a') as res:
        res.write(logline)
    return inp, pf
    
def writelog(txt,USR=''):
	if USR == '':
		pyt='"PYT","    "'
	else:
		if USR == 0:
			pyt='"PYT","TFL "'
		else:
			pyt='"PYT","USR{}"'.format(USR)
	time = dt.now().strftime('%H:%M:%S')
	strttime = '"' + todayABI + '"' + ',' + '"' + time + '",' + pyt + ','
	nextline = strttime+txt+'\n'
	print nextline
	#with open('results.csv','a') as res:
	#	res.write(nextline)

todayABI = "19/08/2024"

val = '100mV'
llim = '50mV'
hlim = '200mV'
USR1=1
USR2=2

print checkLIMITSLog(val,llim='',hlim=hlim,usr=USR1)

print checkLIMITSLog(val,llim=llim,hlim=hlim,usr=USR1)

instrument='LEDS'
print checkLIMITSLog(val,llim='',hlim='',usr=USR2)

checkLIMITSLog('h')