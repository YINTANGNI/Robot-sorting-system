#! /usr/bin/env python
import rospy
import time
import serial
from std_msgs.msg import String

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)

rospy.init_node('Roboarm_node')
def callback(msg):
	ser.write(msg.data)
sub = rospy.Subscriber('Roboarm/position',String,callback)
rospy.spin()






