#!/usr/bin/env python
import rospy
from std_msgs.msg import String,Bool
from geometry_msgs.msg import Twist

def callback_1(msg):
	global t
	t.angular.z = msg.angular.z
	t.linear.x = msg.linear.x

def callback_2(msg):
	global sign
	sign.data = msg.data
if __name__ == '__main__':
	rospy.init_node('key_to_twist')
	rate = rospy.Rate(5)
	key_pub = rospy.Publisher('/cmd_vel',Twist,queue_size = 1)
	t = Twist()
	sign = Bool()
	while not rospy.is_shutdown():
		key_sub = rospy.Subscriber('cmd_vel/sign',Bool,callback_2)
		if sign.data == True:
			cmd_sub = rospy.Subscriber('cmd_vel/change',Twist,callback_1)
			key_pub.publish(t)
			rate.sleep()
			