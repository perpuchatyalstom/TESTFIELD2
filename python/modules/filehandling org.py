import os
import sys
import datetime

global pcb
pcb=''
global logfile
logfile=''

global timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
global today
today = datetime.datetime.now().strftime("%Y-%m-%d")

def Modify_global_pcb(inp):
    global pcb
    pcb=inp

def Modify_global_logfile(inp):
    global logfile
    logfile=pcb + '_results.csv'

def logresults(logfile,message):
    logline = "{},{}".format(timestamp,message)
    return today,timestamp,logline

def definepcb():
    cwd = os.getcwd()
    pcb = cwd.split('\\')[2]
    Modify_global_pcb(pcb)

def startlogging(logfile):
    cwd = os.getcwd()
    line_count=0
    if os.path.exists(logfile):
        with open(logfile, 'r') as file:
            lines=file.readlines()
        if len(lines) == 1:
            lines=lines[0].replace('"','')
            res = pcbINFO(logfile)
            with open(logfile, 'w') as file:
                file.write(lines)
                file.write('timestamp result file: ' + timestamp + '\n')
                file.write('user: ' + os.environ['USERNAME'] + '\n')
                file.write('pcb: ' + pcb+ '\n')
                file.write('Serial: ' + res[0] + '\n')
                file.write('Version: ' + res[1] + '\n')
    else:
        print ('file {} does not exist'.format(logfile))
    return


def pcbINFO(logfile):
    try:
        serialNr = raw_input("Serial number: ")
        print "\nYou entered: " + serialNr

        VersionNr = raw_input("Version: ")
        print "\nYou entered: " + VersionNr
    except EOFError:
        print "\nYou pressed cancel"
    return serialNr,VersionNr



