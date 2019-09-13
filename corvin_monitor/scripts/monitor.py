#! /usr/bin/env python
from Tkinter import *
import socket
import rospy
from std_msgs.msg import String,Bool
from geometry_msgs.msg import Twist
#ser = serial.Serial("/dev/ttyUSB1", 9600, timeout=0.5)
rospy.init_node('monitor')
root = Tk()
root.title('Robot Sorting System Information Center')
root.geometry('1024x530')
root.resizable(width=False, height=False)



place_arg1 = 30
place_arg2 = 20
place_arg3 = 30



###############################################################################################################
###########################################Robot Control#######################################################
###############################################################################################################
Robot_control = LabelFrame(root,text='Robot Control',font=(None,20),width=964,height=430)
Robot_control.place(x=place_arg2,y=0)

###############################################################################################################
aimed_place = IntVar()
aimed_object = IntVar()
goal = String()

def Send_Goal():
	global aimed_object
	global aimed_place
	global goal
	goal.data = str(aimed_object.get())+' '+str(aimed_place.get())
	print goal.data
	send_goal_pub = rospy.Publisher('DeliveryGoal',String,queue_size=1)
	send_goal_pub.publish(goal)
Place_choose = LabelFrame(Robot_control,text='Aimed Delivery Place',font=(None,15),width=250,height=130)
Place_choose.place(x=place_arg2,y=10)

Place_A = Radiobutton(Place_choose,text='Place_A',font=(None,12),variable=aimed_place, value=1)
Place_A.place(x=place_arg1,y=0)

Place_B = Radiobutton(Place_choose,text='Place_B',font=(None,12),variable=aimed_place, value=2)
Place_B.place(x=place_arg1,y=30)

Place_C = Radiobutton(Place_choose,text='Place_C',font=(None,12),variable=aimed_place, value=3)
Place_C.place(x=place_arg1,y=60)

###############################################################################################################
Object_choose = LabelFrame(Robot_control,text='Aimed Delivery Object',font=(None,15),width=250,height=130)
Object_choose.place(x=place_arg2,y=160)

Object_A = Radiobutton(Object_choose,text='Object_A',font=(None,12),variable=aimed_object, value=1)
Object_A.place(x=place_arg1,y=0)

Object_B = Radiobutton(Object_choose,text='Object_B',font=(None,12),variable=aimed_object, value=2)
Object_B.place(x=place_arg1,y=30)

Object_C = Radiobutton(Object_choose,text='Object_C',font=(None,12),variable=aimed_object, value=3)
Object_C.place(x=place_arg1,y=60)

Delivery = Button(Robot_control,text='Deliver',command=Send_Goal,font=(None,15),width=10,height=2)
Delivery.place(x=place_arg2+40,y=300)

###############################################################################################################
speed = IntVar()
direction = IntVar()
send_enable = IntVar()
speed.set(0)
direction.set(0)
send_enable.set(0)


def Pioneer_Reset():
	global speed
	global direction
	speed.set(0)
	direction.set(0)
	print speed.get(),direction.get()

def Send_Vel(aaa):
	twist = Twist()
	global speed
	global direction
	if send_enable.get() == 1:
		twist.linear.x = speed.get()*0.1
		twist.angular.z = direction.get()*(-0.1)
		print twist.linear.x,twist.angular.z
		send_vel_pub = rospy.Publisher('cmd_vel/change',Twist,queue_size=1)
		send_vel_pub.publish(twist)

def Send_Vel_Sign():
		send_vel_sign = Bool()
		send_vel_sign_pub = rospy.Publisher('cmd_vel/sign',Bool,queue_size=1)
		send_vel_sign.data = send_enable.get()
		print send_vel_sign.data
		send_vel_sign_pub.publish(send_vel_sign)



Pioneer_cmd = LabelFrame(Robot_control,text='Pionner Movement Control',font=(None,15),width=640,height=160)
Pioneer_cmd.place(x=295,y=10)

Velocity = Scale(Pioneer_cmd,label='Linear Speed',variable=speed,command=Send_Vel,font=(None,8),from_=0, to=10, orient=HORIZONTAL,length=500, showvalue=0, tickinterval=1, resolution=1)
Velocity.place(x=place_arg3,y=0)

Direction = Scale(Pioneer_cmd,label='Angular Speed',variable=direction,font=(None,8),command=Send_Vel,from_=-10, to=10, orient=HORIZONTAL,length=500, showvalue=0, tickinterval=2, resolution=1)
Direction.place(x=place_arg3,y=56)

Send_vel = Checkbutton(Pioneer_cmd,text='Enable',variable=send_enable,onvalue=1,offvalue=0,font=(None,13),width=5,height=3,command=Send_Vel_Sign)
Send_vel.place(x=530,y=0)

Pionner_reset = Button(Pioneer_cmd,text='Reset',font=(None,11),width=4,height=1,command=Pioneer_Reset)
Pionner_reset.place(x=547,y=75)

###############################################################################################################
pos1 = IntVar()
pos2 = IntVar()
pos3 = IntVar()
roboarm_pos = String()
pos1.set(90)
pos2.set(90)
pos3.set(90)

def Roboarm_Reset():
	global roboarm_pos
	global pos1
	global pos2
	global pos3
	pos1.set(90)
	pos2.set(90)
	pos3.set(90)
	roboarm_pos.data = str(pos1.get())+' '+str(pos2.get())+' '+str(pos3.get())+' 0 0 1'
	print roboarm_pos.data
	Roboarm_Reset_pub = rospy.Publisher('Roboarm/position',String,queue_size=1)
	Roboarm_Reset_pub.publish(roboarm_pos)	

def Roboarm_Move():
	global roboarm_pos
	global pos1
	global pos2
	global pos3
	roboarm_pos.data = str(pos1.get())+' '+str(pos2.get())+' '+str(pos3.get())+' 0 0 1'
	print roboarm_pos.data
	Roboarm_Reset_pub = rospy.Publisher('Roboarm/position',String,queue_size=1)
	Roboarm_Reset_pub.publish(roboarm_pos)	

def Roboarm_Pumpon():
	global roboarm_pos
	global pos1
	global pos2
	global pos3
	roboarm_pos.data = str(pos1.get())+' '+str(pos2.get())+' '+str(pos3.get())+' 0 1 1'
	print roboarm_pos.data
	Roboarm_Reset_pub = rospy.Publisher('Roboarm/position',String,queue_size=1)
	Roboarm_Reset_pub.publish(roboarm_pos)	

def Roboarm_Pumpoff():
	global roboarm_pos
	global pos1
	global pos2
	global pos3
	roboarm_pos.data = str(pos1.get())+' '+str(pos2.get())+' '+str(pos3.get())+' 0 2 1'
	print roboarm_pos.data
	Roboarm_Reset_pub = rospy.Publisher('Roboarm/position',String,queue_size=1)
	Roboarm_Reset_pub.publish(roboarm_pos)	

Roboarm_cmd = LabelFrame(Robot_control,text='Robot Arm Movement Control',font=(None,15),width=640,height=210)
Roboarm_cmd.place(x=295,y=170)

Base_pos = Scale(Roboarm_cmd, variable=pos1,label='Base', font=(None,8),from_=0, to=180, orient=HORIZONTAL,length=500, showvalue=0, tickinterval=60, resolution=1)
Base_pos.place(x=place_arg3,y=0)

Bigarm_pos = Scale(Roboarm_cmd, variable=pos2,label='Big Arm', font=(None,8),from_=0, to=180, orient=HORIZONTAL,length=500, showvalue=0, tickinterval=60, resolution=1)
Bigarm_pos.place(x=place_arg3,y=56)

Smallarm_pos = Scale(Roboarm_cmd, variable=pos3,label='Small Arm', font=(None,8),from_=0, to=180, orient=HORIZONTAL,length=500, showvalue=0, tickinterval=60, resolution=1)
Smallarm_pos.place(x=place_arg3,y=112)

Send_pos = Button(Roboarm_cmd,text='Move',font=(None,11),width=4,height=1,command=Roboarm_Move)
Send_pos.place(x=547,y=0)

Send_reset = Button(Roboarm_cmd,text='Reset',font=(None,11),width=4,height=1,command=Roboarm_Reset)
Send_reset.place(x=547,y=44)

Pump_on = Button(Roboarm_cmd,command=Roboarm_Pumpon,text='Grip',font=(None,11),width=4,height=1)
Pump_on.place(x=547,y=88)

Pump_off = Button(Roboarm_cmd,command=Roboarm_Pumpoff,text='Loosen',font=(None,11),width=4,height=1)
Pump_off.place(x=547,y=132)



###############################################################################################################
###########################################Robot Information###################################################
###############################################################################################################
ip1 = StringVar()
ip1 = 'NULL'
ip2 = StringVar()
ip2 = 'NULL'
ip3 = StringVar()
ip3 = 'NULL'

def IP1_Update():
	global ip1
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip1 = s.getsockname()[0]
		IP1.config(text='Monitor_IP:'+ip1)
	finally:
		s.close()


def Ip2_Callback(msg):
	global ip2
	ip2 = msg.data
	IP2.config(text='Pioneer_IP:'+ip2)
def IP2_Update():
	ip2_sub = rospy.Subscriber('/Data_Update/IP2',String,Ip2_Callback)

def Ip3_Callback(msg):
	global ip3
	ip3 = msg.data
	IP3.config(text='Roboarm_IP:'+ip3)
def IP3_Update():
	ip3_sub = rospy.Subscriber('/Data_Update/IP3',String,Ip3_Callback)


def Data_Update():
	IP1_Update()
	IP2_Update()
	IP3_Update()


Robot_info = LabelFrame(root, text='Robot Information',font=(None,20),width=964,height=90)
Robot_info.place(x=place_arg2,y=430)


IP1 = Label(Robot_info,text='Monitor_IP:'+ip1,font=(None,15))
IP1.place(x=10,y=0)

IP2 = Label(Robot_info,text='Pioneer_IP:'+ip2,font=(None,15))
IP2.place(x=310,y=0)

IP3 = Label(Robot_info,text='Roboarm_IP:'+ip3,font=(None,15))
IP3.place(x=620,y=0)

Update = Button(Robot_info,text='Update',font=(None,14),width=4,height=1,command=Data_Update)
Update.place(x=870,y=0)

root.mainloop()

