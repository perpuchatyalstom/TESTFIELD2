
import pygetwindow as gw
import subprocess

def get_window_titles():
    titles = []
    for window in gw.getAllWindows():
        titles.append(window.title)
    #look for system 8 window
    for title in titles:
        if "ABI SYSTEM 8" in title:
            testflowpath = title.strip().rsplit("\\", 1)[0].rsplit(" - ",1)[1]
            testflowname = title.strip().rsplit("\\", 1)[-1]          
            return testflowpath, testflowname
    return 0

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


path, testflow = get_window_titles()
print path
print testflow
  
path, testflow =  getTestFlowName()
print path
print testflow