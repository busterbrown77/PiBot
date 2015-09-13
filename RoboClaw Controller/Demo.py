import roboclaw
import time

#This is just a small bit of code to test the RoboClaw python library. 

print "5"
time.sleep(1)
print "4"
time.sleep(1)
print "3"
time.sleep(1)
print "2"
time.sleep(1)
print "1"
time.sleep(1)

#Linux comport name
roboclaw.Open("/dev/ttyACM0",115200)


#Get version string
version = roboclaw.ReadVersion()
if version[0]:
	print repr(version[1])
	#Version check succeeded, so controller is connected. 
	#So now commands can be sent.

	#Drive Both Motors at Speed 250
	print "Drive M1 200"
	roboclaw.M1Forward(250)
	print "Drive M2 200"
	roboclaw.M2Forward(250)

	#Read Speed to a String, then print it
	a = roboclaw.ReadM1Speed()
	b = roboclaw.ReadM2Speed()
	print a,b

	#Python Sleep to let motors run for 5 seconds before stopping
	print "Sleeping 5 Seconds"
	time.sleep(5)

	#Stop Motors
	print "Stopping Motors"
	roboclaw.M1Backward(0)
	roboclaw.M2Backward(0)

	print "Sleeping 5 Seconds"
	time.sleep(5)

	#Turn by running the motors in opposite directions.
	#This is rudimentary and will be improved.
	print "Turn Left"
	roboclaw.M1Forward(50)
	roboclaw.M2Backward(50)

	print "Sleeping 5 Seconds"
	time.sleep(5)

	print "Stopping Motors"
	roboclaw.M1Backward(0)
	roboclaw.M2Backward(0)

	print "Sleeping 5 Seconds"
	time.sleep(5)

	print "Turn Right"
	roboclaw.M1Backward(50)
	roboclaw.M2Forward(50)

	print "Sleeping 5 Seconds"
	time.sleep(5)

	print "Stopping Motors"
	roboclaw.M1Backward(0)
	roboclaw.M2Backward(0)

else:
	print "GETVERSION Failed"
	
		
