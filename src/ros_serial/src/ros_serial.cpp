#include <ros/ros.h>
#include <ros/spinner.h>
#include <nodelet/loader.h>
#include <string>
#include <cstring>

#include "ros_serial/ros_serial_node.h"

using namespace std;


int main(int argc, char** argv)
{
  string nodeName = "ros_serial";
  ROS_INFO("Initializing %s ...", nodeName.c_str());
  ros::init(argc, argv, nodeName.c_str());
  ros::NodeHandle n;

  ROS_INFO("%s activating ok !", nodeName.c_str());
  ROS_Serial_Node ros_serial_node(n, 0);
  
  
  while (ros::ok()) 
  {
    ros_serial_node.run();
  }
  //ros::spin();
  
  ros::shutdown();
  return 0;
}
