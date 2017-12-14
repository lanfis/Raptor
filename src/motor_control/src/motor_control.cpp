#include <ros/ros.h>
#include <ros/spinner.h>
#include <nodelet/loader.h>
#include <string>
#include <cstring>

#include "motion/motor_control_node.h"

using namespace std;


int main(int argc, char** argv)
{
  string nodeName = "motor_control";
  ROS_INFO("Initializing %s ...", nodeName.c_str());
  ros::init(argc, argv, nodeName.c_str());
  ros::NodeHandle n;

  ROS_INFO("%s activating ok !", nodeName.c_str());
  Motor_Control_Node motor_control_node(n, 0);
  
  
  while (ros::ok()) 
  {
    motor_control_node.run();
  }
  //ros::spin();
  
  ros::shutdown();
  return 0;
}
