#!/usr/bin/env python
import rospy
from time import sleep
from std_msgs.msg import String,Bool
from ar_track_alvar_msgs.msg import AlvarMarkers
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
import actionlib
import serial
import time

def goal_pose(pose):
	goal_pose = MoveBaseGoal()
	goal_pose.target_pose.header.frame_id='map'
	goal_pose.target_pose.pose.position.x = pose[0][0]
	goal_pose.target_pose.pose.position.y = pose[0][1]
	goal_pose.target_pose.pose.position.z = pose[0][2]
	goal_pose.target_pose.pose.orientation.x = pose[1][0]
	goal_pose.target_pose.pose.orientation.y = pose[1][1]
	goal_pose.target_pose.pose.orientation.z = pose[1][2]
	goal_pose.target_pose.pose.orientation.w = pose[1][3]
	return goal_pose

def Deliveryinfo_callback(Deliveryinfo):
	#print Deliveryinfo.data
	global aimed_object
	global aimed_place
	aimed_object = int(Deliveryinfo.data[0])
	aimed_place = int(Deliveryinfo.data[2])
	#print aimed_object,aimed_place

def wait_to_check():
	while (1):
		if 'a' == ser.read():
			break

def pickup(msg):
	global aimed_object
	global aimed_place
	marker_coordinate = []
	for i in xrange(1,5):
		object_id = msg.markers[i].id
		print object_id
		marker_x = int(msg.markers[i].pose.pose.position.x*1000)
		marker_y = int(msg.markers[i].pose.pose.position.y*1000)
		marker_z = int(msg.markers[i].pose.pose.position.z*1000)
		print marker_x,marker_y,marker_z
		marker_coordinate.append(marker_x)
		marker_coordinate.append(marker_y)
		marker_coordinate.append(marker_z)
	aimed_marker_x = marker_coordinate[(aimed_object-1)*3]
	aimed_marker_y = marker_coordinate[(aimed_object-1)*3+1]
	aimed_marker_z = marker_coordinate[(aimed_object-1)*3+2]
	platform_x = marker_coordinate[9]
	platform_y = marker_coordinate[10]
	platform_z = marker_coordinate[11]
	ser.write('0 160 150 0 0 0')
	wait()
	ser.write(str(aimed_marker_x)+' '+str(aimed_marker_y)+' '+str(aimed_marker_z+80)+' 0 0 0')
	wait()
	for x in xrange(aimed_marker_z+80,aimed_marker_z,stepsize*(-1)):
		ser.write(str(aimed_marker_x)+' '+str(aimed_marker_y)+' '+str(x)+' 0 0 0')
		wait()
		time.sleep(0.001)
	time.sleep(1)
	ser.write(str(aimed_marker_x)+' '+str(aimed_marker_y)+' '+str(aimed_marker_z)+' 0 1 0')
	wait()
	for x in xrange(aimed_marker_z,aimed_marker_z+80,stepsize):
		ser.write(str(aimed_marker_x)+' '+str(aimed_marker_y)+' '+str(x)+' 0 0 0')
		wait()
		time.sleep(0.001)
	for x in xrange(aimed_marker_x,0,stepsize*(-1)):
		ser.write(str(x)+' '+str(aimed_marker_y)+' '+str(aimed_marker_z+80)+' 0 0 0')
		wait()
		time.sleep(0.001)
	for x in xrange(0,platform_x,stepsize*(-1)):
		ser.write(str(x)+' '+str(aimed_marker_y)+' '+str(aimed_marker_z+80)+' 1 0 0')
		wait()
		time.sleep(0.001)
	if aimed_marker_y >= platform_y:
		for x in xrange(aimed_marker_y,platform_y,stepsize*(-1)):
			ser.write(platform_x+' '+str(x)+' '+str(aimed_marker_z+80)+' 1 0 0')
			wait()
			time.sleep(0.001)
	else:
		for x in xrange(aimed_marker_y,platform_y,stepsize):
			ser.write(str(platform_x)+' '+str(x)+' '+str(aimed_marker_z+80)+' 1 0 0')
			wait()
			time.sleep(0.001)
	for x in xrange(aimed_marker_z+80,0,stepsize*(-1)):
		ser.write(str(platform_x)+' '+str(platform_y)+' '+str(x)+' 1 0 0')
		wait()
		time.sleep(0.001)
	for x in xrange(0,platform_z+aimed_marker_z,stepsize*(-1)):
		ser.write(str(platform_x)+' '+str(platform_y)+' '+str(x)+' 13 0 0')
		wait()
		time.sleep(0.001)
	time.sleep(1)
	ser.write(str(platform_x)+' '+str(platform_y)+' '+str(platform_z)+' 13 2 0')
	time.sleep(1)
	for x in xrange(platform_z+aimed_marker_z,0,stepsize):
		ser.write(str(platform_x)+' '+str(platform_y)+' '+str(x)+' 13 0 0')
		wait()
		time.sleep(0.001)
	for x in xrange(0. aimed_marker_z+80,stepsize):
		ser.write(str(platform_x)+' '+str(platform_y)+' '+str(x)+' 1 0 0')
		wait()
		time.sleep(0.001)
	ser.write('0 160 150 0 0 0')
	marker_coordinate = []


if __name__ == '__main__':
	ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)
	aimed_object = 0
	aimed_place = 0
	stepsize = 5
	wayspoints = [[(18.0,6.1,0.0),(0.0,0.0,-0.6,0.8)],
			  [(15.4,6.1,0.0),(0.0,0.0,-0.6,0.8)],
			  [(12.8,6.1,0.0),(0.0,0.0,-0.6,0.8)]]
	rospy.init_node('Robotarm_transport')
	rospy.wait_for_message('/DeliveryGoal',String)
	delivery_goal_sub = rospy.Subscriber('/DeliveryGoal',String,Deliveryinfo_callback)
	coordinate_execute = rospy.Subscriber('/ar_pose_marker',AlvarMarkers,pickup)
	client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
	client.wait_for_server()
	goal = goal_pose(aimed_place-1)
	client.send_goal(goal)
	client.wait_for_result()