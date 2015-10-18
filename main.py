import platform
import os
import threading
import serial
import glob
import sys
import time
import RoboClaw_Controller2.roboclaw as RoboClaw


address = 0x80
#Used for OS Specific Settings
isLinux = False
isDarwin = False
isWindows = False

#RoboClaw Related Variables
serialConnRate = 0.2
serialBaudRate = 115200
RC_SPD1 = 0
RC_SPD2 = 0
RC_ENC1 = 0
RC_ENC2 = 0
RC_TEMP = 0
RC_MBAT = 0
RC_PORT = ""
RC_VER = ""

#LCD Related Variables
displayRefreshRate = 0.2
#displayBacklight = 1
#displayContrast = 1
displayIndicatorIndex = 0;
displayIndicator = "****************************"

#Shared Variables
stillRunning = True
currentTask = ""
active_serial_ports = []
fieldSide = 'S'

#Clear Console Utility Command, compatible with all platforms.
#Used for debug display and general UI.
def clearConsole():
    if isLinux:
        os.system("clear")
    elif isDarwin:
        os.system("Clear")
    elif isWindows:
        os.system("cls")

#Detects Current OS and changes the corresponding boolean.
#Used for localized console commands and serial port detection.
def osDetect():
    global isLinux
    global isDarwin
    global isWindows
    os = platform.system()

    if os == 'Linux' or os == 'Linux2' or os == 'cygwin':
        #LCD Imports only run code is running on the Pi.
        #No LCD on PCs, along with Pi Specific modifications.
        import ADAFruit_CharLCDPlate.IEEEMenu as LCD
        isLinux = True
    elif os == 'Windows':
        isWindows = True
    elif os == 'Darwin':
        isDarwin = True
    else:
        print "Unsupported Platform (" + os + "), exiting."
        raise EnvironmentError('Unsupported platform')

#Gathers Active Serial Ports on all Platforms.
#Retuns an array of all ports.
def portDetect():
    global active_serial_ports

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            active_serial_ports.append(port)
        except (OSError, serial.SerialException):
            pass

#Attempt to Connect to the RoboClaw using previously found ports.
def setupRoboClaw():
    global RC_PORT
    global RC_VER
    global currentTask
    global address

    #Loop Through all Available Ports and try to Connect to RoboClaw.
    for p in active_serial_ports:
	RC_PORT = p
	print "Attempting Connection to RoboClaw on " + RC_PORT
        RoboClaw.Open(RC_PORT, serialBaudRate)

	version = RoboClaw.ReadVersion(address)
	if version[0]:
	    RC_VER = version[1]
	    currentTask = "RoboClaw Connected"
            print "Connected to " + RC_VER + "Active Port: " + RC_PORT + "\n"
	    return
	else:
	    print "Failed\n"

    currentTask = "Conn. RoboClaw Fail"
    print "Could Not Find RoboClaw Controller on Available Ports. (Is it plugged in / on?)"
    raise SystemExit

#Method to Update the Visual Indicator in Debug Display
def displayIndicatorUpdate():
    global displayIndicator
    global displayIndicatorIndex

    if displayIndicatorIndex == 31:
        displayIndicatorIndex = 0
    else:
        displayIndicatorIndex = displayIndicatorIndex + 1

    displayIndicator = ""

    rStart = 31 - displayIndicatorIndex
    rEnd = 31 - rStart

    for i in range(rStart):
       displayIndicator += "*"

    displayIndicator += "O"

    for i in range(rEnd):
       displayIndicator += "."

def DriveMixSpeedDist(speed, distance):
    global currentTask
    global add


    currentTask = "DR S:",speed," D:",distance
    #SPD1, DST1, SPD2, DST2, buffer
    RoboClaw.SpeedDistanceM1M2(address, speed, distance, speed, distance, 0)

def TurnRight(speed):

    currentTask = "DR S:",speed," D:",distance 
    RoboClaw.TurnRightMixed(address, value)

#Threaded GetStatus Method
def thread_roboclaw_getStatus(threadName, serialLimit):
    global currentTask
    global RC_SPD1
    global RC_SPD2
    global RC_ENC1
    global RC_ENC2
    global RC_TEMP
    global RC_MBAT
    global address

    while 1:
       time.sleep(serialLimit)

       try:
           RC_SPD1 = RoboClaw.ReadSpeedM1(address)
           RC_SPD2 = RoboClaw.ReadSpeedM2(address)
       except:
           currentTask = "Failed to Read Speed"

       try:
           RC_ENC1 = RoboClaw.ReadEncM1(address)
           RC_ENC2 = RoboClaw.ReadEncM2(address)
       except:
           currentTask = "Failed to Read Encoders"

       temp = RoboClaw.ReadTemp(address)
       if temp[0]:
           RC_TEMP = temp[1]/10.0
       #else:
           #currentTask = "Failed to read Tempurature"

       mbat = RoboClaw.ReadMainBatteryVoltage(address)
       if mbat[0]:
           RC_MBAT = mbat[1]/10.0
       #else:
           #currentTask = "Failed to Read Main Battery"

#Not Final
def thread_display_statusUpdate(threadName, refreshRate):
    while 1:
        time.sleep(refreshRate)

        #battery, #field, #undef,  curent task
        screen_vars = [RC_MBAT, fieldSide, "", currentTask]
        LCD.display_menu(screen_vars)

#Threaded Debug Display Method
#Shows Various Values from the RoboClaw Controller, and other Processes for Testing.
def thread_display_debugUpdate(threadName, refreshRate):
    while 1:
        time.sleep(refreshRate)

        clearConsole()

        print "=========== RoboClaw ==========="
        print " Speed 1:       ", RC_SPD1
        print " Speed 2:       ", RC_SPD2
        print " Encoder 1:     ", RC_ENC1
        print " Encoder 2:     ", RC_ENC2
        print " Tempurature:   ", RC_TEMP
        print " Main Battery:  ", RC_MBAT
        print displayIndicator
        print ""
        print currentTask
        displayIndicatorUpdate()


#Class Handling All Threaded Tasks Related to the RoboClaw Controller
class roboclawThreader (threading.Thread):
    def __init__(self, threadID, name, task):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.task = task

    def run(self):
        if self.task == 1:
            taskdesc = "RoboClaw Status Updater"
            print "Starting " + self.name + " - Task: " + taskdesc
            thread_roboclaw_getStatus(self.name, serialConnRate)
            print "Exiting " + self.name + " - Task: " + taskdesc

#Class Handling All Threaded Tasks Related to the LCD Display
class displayThreader (threading.Thread):
    def __init__(self, threadID, name, task):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.task = task

    def run(self):
        if self.task == 1:
            taskdesc = "Status Display Updater"
            print "Starting " + self.name + " - Task: " + taskdesc
            thread_display_statusUpdate(self.name, displayRefreshRate)
            print "Exiting " + self.name + " - Task: " + taskdesc

        elif self.task == 2:
            taskdesc = "Debug Display"
            print "Starting " + self.name + " - Task: " + taskdesc
            thread_display_debugUpdate(self.name, displayRefreshRate)
            print "Exiting " + self.name + " - Task: " + taskdesc

    def stop(self):
        self._stop.set()

#=======================================================================================
#================== Main Code Begins ===================================================
#=======================================================================================
osDetect()
clearConsole()

statusThread = roboclawThreader(1, "Thread 1", 1)
statusDisplayThread = displayThreader(2, "Thread 2", 1)
debugDisplayThread = displayThreader(2, "Thread 3", 2)

if isLinux:
    statusDisplayThread.start()

print "--------------------------------------------------------------------------------"
print "------------------------------- Loading Director -------------------------------"
print "---------------- Ensure Everything is Plugged In and Powered On ----------------"
print "--------------------------------------------------------------------------------"
print "Detected OS: " + platform.system() + "..."

print "Detecting Available Serial Ports..."
currentTask = "Port Detection..."
portDetect()
currentTask = ""

print active_serial_ports,"\n"
currentTask = "RoboClaw Connect..."
setupRoboClaw()
RoboClaw.ResetEncoders(address)

print "Debug UI Starting in 3 Seconds..."
time.sleep(3)
debugDisplayThread.start()

currentTask = "Starting motors in 2 seconds..."
time.sleep(1)
currentTask = "Starting motors in 1 second..."
time.sleep(1)
#Max Speed 2300

DriveMixSpeedDist(2300,6000)
TurnRight(127)


statusThread.start()

while 1:
    time.sleep(0.1)

currentTask = "Main Thread has Closed."
