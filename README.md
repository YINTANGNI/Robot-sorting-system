# Robot-sorting-system
Here are the codes for my MSc project.
The package Servo_Control_Arduino is the servo drive for the manipulator, which runs on Arduino UNO.
The packge alvar_test contains the main programe running on Manipulator's control unit and two tranfer programes for manual control mode.
The package usb_cam is the package used to publish raw images of the camera and astra_launch is the package used to publish depth image of the RGB-D camera.
The package corvin_manipulator is used to display interface in remote control terminal.
The package p3dx_navigation contains the configuration files for mobile robot.

To run the program, the steps are following:
Mobile robot:
    $ roscore
    $ roslaunch p3dx_navigation pioneer.launch
    $ roslaunch p3dx_navigation rviz.launch
    $ roslaunch p3dx_navigation move_base_rosaria.launch
Manipulator:
    $ roslaunch usb_cam astra.launch
    $ roslaunch astra_launch astra.launch
    $ roslaunch roboarm_alvar roboarm_alvar.launch
    $ roslaunch test_alvar main.py
    $ rosrun test_alvar manual_manipulator.py
    $ rosrun test_alvar manual_mobilerobot.py
Remote control terminal:
    $ rosrun corvin_manipulator manipulator.py
