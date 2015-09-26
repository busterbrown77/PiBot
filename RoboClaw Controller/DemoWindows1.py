import roboclaw
import time
import subprocess
import platform

def clear():
	"Functions need to be at the top & this works cross platform"
	#time.sleep(.8)
	subprocess.Popen("cls"if platform.system()=="Windows" else "clear", shell=True)
	#subprocess.call(["printf","'\033c'"])

def getDetailedStatus():
	"This clears the screen and updates the values"
	clear()
	time.sleep(.5)
	#Read Speed/Encoder to a String, then print it
	a = roboclaw.ReadM1Speed()
	b = roboclaw.ReadM2Speed()
	c = roboclaw.ReadM1Encoder()
	d = roboclaw.ReadM2Encoder()
	print "SPD1 ",a,"\nSPD2 ",b,"\nENC1",c,"\nENC2", d

	status = roboclaw.ReadStatus()
	if status[0]:
		print "Error State: ",status[1]
	else:
		print "GETERROR Failed"

	temp = roboclaw.ReadTemperature()
	if temp[0]:
		print "Temperature: ",temp[1]/10.0
	else:
		print "GETTEMP Failed"

	mbat = roboclaw.ReadMainBattery()
	if mbat[0]:
		print "Main Battery: ",mbat[1]/10.0
	else:
		print "GETMBAT Failed"

	lbat = roboclaw.ReadLogicBattery()
	if mbat[0]:
		print "Logic Battery: ",lbat[1]/10.0
	else:
		print "GETLBAT Failed"

	current = roboclaw.ReadCurrents();
	if current[0]:
		print "Current M1: ",current[1]/100.0
		print "Current M2: ",current[2]/100.0

	batt  = roboclaw.ReadLogicBatterySettings()
	if batt[0]:
		print "Logic Battery Min: ",batt[1]/10.0," Max: ",batt[2]/10.0

	batt = roboclaw.ReadMainBatterySettings()
	if batt[0]:
		print "Main Battery Min: ",batt[1]/10.0," Max: ",batt[2]/10.0

	pid = roboclaw.ReadM1VelocityConstants()
	if pid[0]:
		print "M1 P: %.2f" % pid[1]
		print "M1 I: %.2f" % pid[2]
		print "M1 D: %.2f" % pid[3]
		print "M1 QPPS: ",pid[4]

	pid = roboclaw.ReadM2VelocityConstants()
	if pid[0]:
		print "M2 P: %.2f" % pid[1]
		print "M2 I: %.2f" % pid[2]
		print "M2 D: %.2f" % pid[3]
		print "M2 QPPS: ",pid[4]

	pid = roboclaw.ReadM1PositionConstants()
	if pid[0]:
		print "M1 P: %.2f" % pid[1]
		print "M1 I: %.2f" % pid[2]
		print "M1 D: %.2f" % pid[3]
		print "M1 IMax: ",pid[4]
		print "M1 Deadzone: ",pid[5]
		print "M1 MinPos: ",pid[6]
		print "M1 MaxPos: ",pid[7]

	pid = roboclaw.ReadM2PositionConstants()
	if pid[0]:
		print "M2 P: %.2f" % pid[1]
		print "M2 I: %.2f" % pid[2]
		print "M2 D: %.2f" % pid[3]
		print "M2 IMax: ",pid[4]
		print "M2 Deadzone: ",pid[5]
		print "M2 MinPos: ",pid[6]
		print "M2 MaxPos: ",pid[7]

	# val = roboclaw.ReadPWMMode()
	# if val[0]:
	# 	print "PWMMode: ",val[1]
	# else:
	# 	print "GET PWM Mode Failed"

	# cur = roboclaw.ReadM1MaxCurrent()
	# if cur[0]:
	# 	print "M1 Max Current: ",cur[1]/100.0
	# cur = roboclaw.ReadM2MaxCurrent()
	# if cur[0]:
	# 	print "M2 Max Current: ",cur[1]/100.0

def getStatus():
	#Read Speed/Encoder to a String, then print it
	clear()
	time.sleep(.5)
	a = roboclaw.ReadM1Speed()
	b = roboclaw.ReadM2Speed()
	c = roboclaw.ReadM1Encoder()
	d = roboclaw.ReadM2Encoder()
	#print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
	print "SPD1 ",a,"\nSPD2 ",b,"\nENC1",c,"\nENC2", d

def intro():
	print "Make sure the thing's plugged in and turned on"
	print "3"
	time.sleep(1)
	print "2"
	time.sleep(1)
	print "1"
	time.sleep(1)

def drive():
	#Drive Both Motors max 255
	print "Drive M1 200"
	#roboclaw.M1Forward(255)
	roboclaw.M1Forward(255)
	print "Drive M2 100"
	roboclaw.M2Forward(255)

#This is just a small bit of code to test the RoboClaw python library.

#Windows comport name
roboclaw.Open("COM3",115200)
#Pi comport name
#roboclaw.Open("/dev/ttyACM0",115200)
#OSX comport name
#roboclaw.Open("/dev/tty.usbmodem1411",115200)
#roboclaw.Open("/dev/tty.usbmodem1451",115200)

version = roboclaw.ReadVersion()#Get version string
if version[0]:
	print repr(version[1])#Version check succeeded, so controller is connected.
	#So now commands can be sent.

	roboclaw.ResetEncoders()#Reset Encoders to Prevent Crash (Investigate)
	intro()
	drive()

	while 1:#clear wait time .5 crashes after 3min 40sec
		getDetailedStatus()
		time.sleep(1)

	#the error codes for unplugging and reading too quickly are the same

else:
	print "GETVERSION Failed"
