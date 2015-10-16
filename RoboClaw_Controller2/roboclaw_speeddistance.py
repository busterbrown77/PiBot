import time
import roboclaw

def displayspeed():
	enc1 = roboclaw.ReadEncM1(address)
	enc2 = roboclaw.ReadEncM2(address)
	speed1 = roboclaw.ReadSpeedM1(address)
	speed2 = roboclaw.ReadSpeedM2(address)

	print("Encoder1:"),
	if(enc1[0]==1):
		print enc1[1],
		print format(enc1[2],'02x'),
	else:
		print "failed",
	print "Encoder2:",
	if(enc2[0]==1):
		print enc2[1],
		print format(enc2[2],'02x'),
	else:
		print "failed " ,
	print "Speed1:",
	if(speed1[0]):
		print speed1[1],
	else:
		print "failed",
	print("Speed2:"),
	if(speed2[0]):
		print speed2[1]
	else:
		print "failed "

#Windows comport name
roboclaw.Open("COM10",38400)
#Linux comport name
#roboclaw.Open("/dev/ttyACM0",115200)

address = 0x80

version = roboclaw.ReadVersion(address)
if version[0]==False:
	print "GETVERSION Failed"
else:
	print repr(version[1])

#Velocity PID coefficients
Kp = 1.0
Ki = 0.5
Kd = 0.25
qpps = 44000

#Set PID Coefficients
roboclaw.SetM1VelocityPID(address,Kp,Kd,Ki,qpps);
roboclaw.SetM2VelocityPID(address,Kp,Kd,Ki,qpps);  

while(1):
	roboclaw.SpeedDistanceM1(address,12000,48000,1)
	roboclaw.SpeedDistanceM2(address,-12000,48000,1)
	buffers = (0,0,0)
	while(buffers[1]!=0x80 and buffers[2]!=0x80):	#Loop until distance command has completed
		displayspeed();
		buffers = roboclaw.ReadBuffers(address);
  
	time.sleep(1)

	roboclaw.SpeedDistanceM1(address,-12000,48000,1)
	roboclaw.SpeedDistanceM2(address,12000,48000,1)
	buffers = (0,0,0)
	while(buffers[1]!=0x80 and buffers[2]!=0x80):	#Loop until distance command has completed
		displayspeed()
		buffers = roboclaw.ReadBuffers(address)
  
	time.sleep(1);  #When no second command is given the motors will automatically slow down to 0 which takes 1 second

	roboclaw.SpeedDistanceM1(address,12000,48000,1)
	roboclaw.SpeedDistanceM2(address,-12000,48000,1)
	roboclaw.SpeedDistanceM1(address,-12000,48000,0)
	roboclaw.SpeedDistanceM2(address,12000,48000,0)
	roboclaw.SpeedDistanceM1(address,0,48000,0)
	roboclaw.SpeedDistanceM2(address,0,48000,0)
	buffers = (0,0,0)
	while(buffers[1]!=0x80 and buffers[2]!=0x80):	#Loop until distance command has completed
		displayspeed()
		buffers = roboclaw.ReadBuffers(address)
  
	time.sleep(1)
