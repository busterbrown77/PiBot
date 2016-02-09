# PiBot
Code Repo for SouthEastCon 2016 Robot
Rules - https://docs.google.com/document/d/1ITIsL9fpTk5HKEJW1NENVrkgfCgXqONWpm0sevzeYmo/edit

The robot will be using the following main components:
	Raspberry Pi 2 (Running Raspbian) - https://www.raspberrypi.org/documentation/
	CMU Camera 5 (Pixy) - http://www.cmucam.org/projects/cmucam5/wiki
	RoboClaw 2x15a Controller - https://www.servocity.com/html/roboclaw_2x15a_motor_controlle.html#.VfBm27SppJE
	MiniMaestro 24 Channel Controller - https://www.servocity.com/html/mini_maestro_24-channel_usb__6.html#.VfNKk7Spqkg
	ADAFruit LCD with Keypad - http://www.adafruit.com/products/1109

The Camera and Motor Controller both have Python Libraries, and we have verified the Motor Controller is functional.
We are still validating the CMU Camera, and whether or not it is sufficient for our needs. A revival of the RoboVision code (on this repo) may be a possibility.

The main robot code is PiBot.py which uses a threaded system to manage components seperately and to isolate potential device failures programmatically (If the screen fails for some reason, the motor controller code is not affected it is on a seperate thread, etc.). As of now all components are functional except the MiniMaestro controller, which is moreso due to it's poor Python support.


