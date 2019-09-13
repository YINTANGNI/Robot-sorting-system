# Robot-sorting-system
Here are the codes for my MSc project.<br>
The package Servo_Control_Arduino is the servo drive for the manipulator, which runs on Arduino UNO.<br>
The packge alvar_test contains the main programe running on Manipulator's control unit and two tranfer programes for manual control mode.<br>
The package usb_cam is the package used to publish raw images of the camera and astra_launch is the package used to publish depth image of the RGB-D camera.<br>
The package corvin_manipulator is used to display interface in remote control terminal.<br>
The package p3dx_navigation contains the configuration files for mobile robot.<br>

To run the robot system, the steps are following:<br>
Mobile robot:<br>
    $ roscore<br>
    $ roslaunch p3dx_navigation pioneer.launch<br>
    $ roslaunch p3dx_navigation rviz.launch<br>
    $ roslaunch p3dx_navigation move_base_rosaria.launch<br>
Manipulator:<br>
    $ roslaunch usb_cam astra.launch<br>
    $ roslaunch astra_launch astra.launch<br>
    $ roslaunch roboarm_alvar roboarm_alvar.launch<br>
    $ roslaunch test_alvar main.py<br>
    $ rosrun test_alvar manual_manipulator.py<br>
    $ rosrun test_alvar manual_mobilerobot.py<br>
Remote control terminal:<br>
    $ rosrun corvin_manipulator manipulator.py<br>
