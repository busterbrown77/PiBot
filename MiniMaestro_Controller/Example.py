import time
import maestro as MiniMaestro

import subprocess
import platform

MM = MiniMaestro.Controller("/dev/tty.usbmodem00113591")

MM.setTarget(21, 1500);
print MM.getPosition(0);

while 1:
	time.sleep(1)
	print MM.getPosition(13)
	print MM.getPosition(18)
