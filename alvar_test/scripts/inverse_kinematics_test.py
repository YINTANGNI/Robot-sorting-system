#! /usr/bin/env python
import rospy
import time
import serial
from std_msgs.msg import String

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)


for x in range(200,99,-1):
	a = '0 '+str(x)+' 30 0 0 0'
	print(a)
	ser.write(a)
	while (1):
		if 'a' == ser.read():
			break
for x in range(0,151,1):
	a = str(x)+' 100 30 0 0 0'
	print(a)
	ser.write(a)
	while (1):
		if 'a' == ser.read():
			break
for x in range(150,-1,-1):
	a = str(x)+' 100 30 0 0 0'
	print(a)
	ser.write(a)
	while (1):
		if 'a' == ser.read():
			break
for x in range(100,201,1):
	a = '0 '+str(x)+' 30 0 0 0'
	print(a)
	ser.write(a)
	while (1):
		if 'a' == ser.read():
			break

	

ser.close()





