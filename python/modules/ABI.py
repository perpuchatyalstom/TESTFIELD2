import csv
import os
import sys
import subprocess
import webbrowser
from mathtools import *
from datetime import datetime as dt

global todayABI
global today
todayABI = dt.now().strftime('%d/%m/%Y')
today=todayABI.replace('/','-')
global PCB
PCB=''
global cwd
cwd=''
global operator
operator=''
global testflow
testflow='Xe-xxxx'
global sernr
sernr='0'
global testname
global instrument
global USR
global message


def modifyGlobal(inp):
# modifyGlobal(['cwd',cwd])
	global PCB
	global cwd
	global todayABI
	global today
	global operator
	global testflow
	global sernr
	global testname
	global message
	global instrument
	global USR
	if inp[0]=='PCB':
		PCB=inp[1]
	if inp[0]=='cwd':
		cwd=inp[1]
	if inp[0]=='todayABI':
		todayABI=inp[1]
		today=todayABI.replace('/','-')
	if inp[0]=='operator':
		operator=inp[1]
	if inp[0]=='testflow':
		testflow=inp[1]
	if inp[0]=='sernr':
		sernr=inp[1]
	if inp[0]=='testname':
		testname=inp[1]
	if inp[0]=='message':
		testname=inp[1]
	if inp[0]=='instrument':
		instrument=inp[1]
	if inp[0]=='USR':
		USR=inp[1]

def checkCWD(inp=''):
	if inp =='': inp=cwd 
	if inp != os.getcwd(): 
		print (os.getcwd() + ' changed to ' + inp)
		os.chdir(inp)

def checkLIMITS(inp,llim='',hlim=''):
	pf = True
	if llim == hlim == '':
		if inp != 1: pf = False
	if llim != '':
		if unit2number(inp) < unit2number(llim): pf = False
	if hlim != '':
		if unit2number(inp) > unit2number(hlim): pf = pf & False
	pf = 'PASS' if pf  else 'FAIL'
	return inp, pf

def boardID(pcbID,uio=1):
	uio = 'I/O1' if uio == 1 else 'I/O2'
	result2={'pcb':'none','margin':'none'}
	boardIDfile='c:\\ABI\\Board ID.csv'
	with open(boardIDfile, 'r') as file:
		# Read the first few bytes to check for BOM
		first_bytes = file.read(3)
        # If BOM is present, strip it
		if first_bytes == b'\xef\xbb\xbf':
            # Open the file in text mode skipping the BOM
			file.seek(3)
		else:
            # Seek back to the start of the file if no BOM
			file.seek(0)
		reader = csv.DictReader(file)
		for row in reader:
			if row['PIN'] == uio: 
				dbCur=unit2number(row['Current'])
				dev=abs(round((dbCur-pcbID)/dbCur*100,2))
				if dev<4:
					result2['pcb']=row['ABI test folder']
					result2['margin']=dev
					break
	return result2

def inputData(txt,resp):
    while True:
        #enter serial number of PCB, cancel returns debug
        try:
            UserEntry = raw_input("Please enter " + txt + resp)
        except EOFError:
            if resp == '': resp = 'xxxx'
            UserEntry = resp
        if UserEntry != '':
            print ('\n' + txt + UserEntry)
            return UserEntry

		
def writelog(txt,script=''):
	checkCWD()
	if script == '':
		pyt='"PYT","    "'
	else:
		if script == 0:
			pyt='"PYT","TFL "'
		else:
			pyt='"PYT","USR{}"'.format(script)
	time = dt.now().strftime('%H:%M:%S') 
	strttime = '"' + todayABI + '"' + ',' + '"' + time + '",' + pyt + ','
	nextline = strttime+txt+'\n'
	#print nextline
	with open('results.csv','a') as res:
		res.write(nextline)


def hourstamp():
	tim=dt.now().strftime('%H%M%S')
	return tim

def createRESULTfile_V1():
	checkCWD()
	time = dt.now().strftime('%H:%M:%S')
	strttime = 'Date' + todayABI + '"' + ',' + '"' + time + '"'
	#firstline = strttime+',"PYT",START of '+ PCB +' testprogram='+ testflow +',operator='+operator+'\n'
	firstline = strttime+',"PYT","START of PCB:",'+ PCB +'," testflowname:",'+ testflow +',"operator=",'+operator+'\n'
	firstline 
	#print firstline
	with open('results.csv','w') as res:
		res.write(firstline)
	

def getTestname():
	with open("testname.log",'r') as f:
		testname=f.readline()[1:-2]
	os.remove("testname.log")
	return testname

def check_file_in_folder(folder_path, file_name):
    # Construct the full path of the file
    file_path = os.path.join(folder_path, file_name)

     # Check if the file exists
    if os.path.isfile(file_path):
        #print("File '{}' exists in folder '{}'.".format(file_name, folder_path))
        return True
    else:
        #print("File '{}' does not exist in folder '{}'.".format(file_name, folder_path))
        return False

def getTestFlowName():
    command = "Get-Process -name system8 | Format-List *"
    # Construct the full PowerShell command
    full_command = ["powershell", "-Command", command]
    process = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if output:
	    for line in output.splitlines():
                if 'MainWindowTitle' in line:
                    testflow = line.rsplit(" - ", 1)[-1]
                    testflowpath = testflow.rsplit("\\", 1)[0]
                    testflowname = testflow.rsplit("\\", 1)[-1]
                    return testflowpath,testflowname
    if error:
        return "Error","Error: " + error.decode('utf-8')
    return "Error",'Error: testflow Not Found'

def testflowExist():
	return os.path.isfile(os.path.join(cwd,testflow))

def createRESULTfile():
	if os.path.exists('results.csv'):
		with open('results.csv','r') as f:
			csv_file = csv.reader(f)
			try:
				firstline=next(csv_file)
			except:
				print 'fail'
				firstline = ''
		createdate=''
		createtime=''
		for i in range(len(firstline)):
			if firstline[i].strip() == 'Date':
				createdate = firstline[i+1]
			if firstline[i].strip() == 'Time':
				createtime = firstline[i+1].replace(':','')
			if (createdate != '') and (createtime != ''):
				break
		if todayABI != createdate:
			if createdate == '':
				createdate=today
				createtime=hourstamp()
			dest = createdate.replace('/','-')  + '_' + createtime + '_results.csv'
			if os.path.exists(dest):
				dest2=dest.replace('.csv','-1.csv')
				if os.path.exists(dest2):
					os.remove(dest2)
				os.rename(dest,dest2)
			os.rename('results.csv',dest)
			createRESULTfile()
	else:
		firstline=[]
		firstline.extend(['Testflow Name', testflow])
		firstline.extend(['Operator Name', operator])
		firstline.extend(['Date', todayABI])
		firstline.extend(['Time', dt.now().strftime('%H:%M:%S')])
		firstline.extend(['Board Name', PCB])
		firstline.extend(['Board Serial Number', sernr])
		secondline='"Date","Time","Src","Script",Status,"Test Name","Instrument","Low limit","Value","Top limit"\n'
		with open('results.csv','w') as f:
			f.write(','.join(firstline) + '\n')
			f.writelines(secondline)

def createHTMLReport():
	# Path to the CSV file
	csv_path = 'results.csv'
	# Path to the generated HTML file
	html_path = 'C:\\testfield\\results.html'
	# Path to the HTML template
	template_path = 'C:\\testfield\\ReportTemplate.html'

	# Read the CSV file
	with open(csv_path, 'r') as csvfile:
		reader = csv.reader(csvfile)
		rows = list(reader)

	# Extract header information from the first row
	header_info = [(rows[0][i].strip(), rows[0][i + 1].strip()) for i in range(0, len(rows[0]), 2)]

	# Read the HTML template
	with open(template_path, 'r') as templatefile:
		html_template = templatefile.read()

	# Generate the header section dynamically
	header_section = ''
	for key, value in header_info:
		header_section += '<div>{}: {}</div>'.format(key, value)

	# Replace the header placeholder with the generated header section
	html_template = html_template.replace('<!--HEADER_SECTION-->', header_section)

	# Generate table headers
	table_headers = ''.join(['<th>{}</th>'.format(header) for header in rows[1]])
	html_template = html_template.replace('<!--TABLE_HEADERS-->', table_headers)

	# Generate table rows and count pass/fail
	table_rows = ''
	test_passed = 0
	test_failed = 0
	total_steps = 0

	# Extract start and end times
	start_time_str = "{} {}".format(rows[2][0], rows[2][1])
	end_time_str = "{} {}".format(rows[-1][0], rows[-1][1])

	# Parse the start and end times
	start_time = dt.strptime(start_time_str, '%d/%m/%Y %H:%M:%S')
	end_time = dt.strptime(end_time_str, '%d/%m/%Y %H:%M:%S')

	# Calculate test duration
	test_duration = end_time - start_time

	# Break down the test duration into days, hours, and minutes
	days = test_duration.days
	hours, remainder = divmod(test_duration.seconds, 3600)
	minutes, _ = divmod(remainder, 60)

	# Format the test duration string
	test_duration_str = "{} day{}, {} hour{}, {} minute{}".format(
		days, 's' if days != 1 else '',
		hours, 's' if hours != 1 else '',
		minutes, 's' if minutes != 1 else ''
	)

	# Generate table rows
	for row in rows[2:]:
		total_steps += 1
		status = 'PASS' if 'PASS' in row else 'FAIL'
		if status == 'PASS':
			test_passed += 1
			row_class = ''
		else:
			test_failed += 1
			row_class = ' class="failed-row"'
		table_row = '<tr{} data-status="{}">'.format(row_class, status)
		for i in range(len(row)):
			if i == len(row) - 1 and len(row) < len(rows[1]):  # If we're at the last entry and the number of cells in the row is less than the number of headers
				table_row += '<td colspan="{}"><b>Message: </b>{}</td>'.format(len(rows[1]) - i, row[i])  # Add the colspan attribute to the last cell
			else:
				table_row += '<td>{}</td>'.format(row[i])  # Add <td> tags to each cell
		table_row += '</tr>'
		table_rows += table_row

	# Replace placeholders in the HTML template
	html_template = html_template.replace('<!--TABLE_ROWS-->', table_rows)
	html_template = html_template.replace('<!--TEST_PASSED-->', str(test_passed))
	html_template = html_template.replace('<!--TEST_FAILED-->', str(test_failed))
	html_template = html_template.replace('<!--TOTAL_STEPS-->', str(total_steps))
	html_template = html_template.replace('<!--TEST_DURATION-->', test_duration_str)

	# Determine test status
	if test_failed > 0:
		test_status_class = 'test-failed'
		test_status_message = 'Failed'
	else:
		test_status_class = 'test-passed'
		test_status_message = 'Passed'

	html_template = html_template.replace('<!--TEST_STATUS_CLASS-->', test_status_class)
	html_template = html_template.replace('<!--TEST_STATUS_MESSAGE-->', test_status_message)

	# Save the generated HTML report
	with open(html_path, 'w') as outputfile:
		outputfile.write(html_template)

	# Optionally open the generated HTML file in the default web browser
	webbrowser.open('file://' + os.path.realpath(html_path))


def checkLIMITSLog(inp,llim='',hlim=''):
	llim=str(llim)
	hlim=str(hlim)
	if inp == 'help'or inp == 'h':
		print 'Usage: ',
		print 'checkLIMITSLog(test value,low limit,high limit,userscript#)'
		print '\n\ttestname\tdefine:\t(abi.testname)'
		print '\tinstrument\tdefine:\t(abi.instrument)'
		print '\tmessage  \tdefine:\t(abi.message)'
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
			loglim.append('"{}"'.format(message))
	if llim != '':
		if unit2number(inp) < unit2number(llim): pf = False
		loglim[1] = llim
	if hlim != '':
		if unit2number(inp) > unit2number(hlim): pf = pf & False
		loglim[3] = hlim
	loglim = ','.join(loglim)
	pf = 'PASS' if pf else 'FAIL'
	stat = 1 if pf else 2

	time = dt.now().strftime('%H:%M:%S')
	todayABI = '19/08/2024'
	logline = '{},{},{}'.format(pf,testname,loglim)
	print logline
	logline = '"{}","{}","PYT","USR{}",{}{}'.format(todayABI,time,USR,logline,'\n')
	with open('results.csv','a') as res:
		res.write(logline)

	return stat, pf