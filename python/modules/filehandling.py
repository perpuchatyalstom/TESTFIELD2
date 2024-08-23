import os
import sys
import datetime

def checkCWD():
	if cwd != os.getcwd(): 
		print os.getcwd() + ' changed to ' + cwd
		os.chdir(cwd)
	return cwd

def writelog(txt):
	checkCWD()
	time = dt.now().strftime('%H:%M:%S') 
	strttime = '"' + todayABI + '","' + time + '","PYT",'
	nextline = strttime+txt+'\n'
	with open('results.csv','a') as res:
		res.write(nextline)
	res.close
	
def hourstamp():
	tim=dt.now().strftime('%H%M%S')
	return tim

def createRESULTfile():
	time = dt.now().strftime('%H:%M:%S')
	strttime = '"' + todayABI + '"' + ',' + '"' + time + '"'
	firstline = strttime+',START of '+PCB+' testprogram,operator='+operator+'\n'
	print firstline
	with open('results.csv','w') as res:
		res.write(firstline)
	res.close

def inputData(txt,resp):
#enter serial number of PCB, cancel returns debug
	try:
		UserEntry = raw_input("Please enter " + txt + resp)
	except EOFError:
		if resp == '': resp = 'xxxx'
		UserEntry = resp
	print
	return UserEntry

import psutil

def list_subprocesses(pid):
	try :
		parent_process = psutil.Process(pid)
		print parent_process
		children = parent_process.children(recursive=True)
		print children
		for child in children:
			print child
			print "PID: {child.pid}, Name: {child.name()}"
	except psutil.NoSuchProcess:
		print "No process with PID {pid} found."
		print "No process with PID {pid} found."
	except psutil.AccessDenied:
		print "Access denied to process with PID {pid}."
	except Exception as e:
		print "An error occurred: {}".format(e)

if __name__ == "__main__":
    parent_pid = int(input("Enter the PID of the parent process: "))
    list_subprocesses(parent_pid)
