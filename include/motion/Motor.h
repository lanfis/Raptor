#pragma once
#ifndef _MOTOR_DRIVER_H_
#define _MOTOR_DRIVER_H_

#include <ros/ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Float32.h>
#include <string>
#include <cstring>
#include <sstream>

//#ifdef _ROS_LINK_H_
#include "../matrix/ros_link.h"
//#endif


using namespace ros;
using namespace std;



class Motor_Driver
{
  private:
	#define HEADER		"PC"
	#define YAW 		"Y"
	#define PITCH 		"P"
	#define ANG_MS_MIN	700
	#define ANG_MS_MAX	2300
//	#define SHUTDOWN 	"SHUTDOWN"
//	#define STATUS 		"STATUS"
	

  public:
    string nodeName = "motor_driver";
    //motor
    string topic_motor_driver_motor_cmd_pub = "motor_driver/motor_driver_cmd";
    string topic_motor_driver_motor_status_sub = "motor_driver/motor_driver_status";
    //computer
    string topic_motor_driver_cmd_yaw_sub = "motor_driver/cmd_yaw";
    string topic_motor_driver_cmd_pitch_sub = "motor_driver/cmd_pitch";
//    string topic_motor_driver_cmd_status_pub = "motor_driver/cmd_status";

  private:
    float ver_ = 1.0;
	int queue_size = 4;
	#ifdef _ROS_LINK_H_
	ROS_Link *ros_link = NULL;
	#endif

  private:
    ros::NodeHandle n_;
    ros::Publisher motor_driver_motor_cmd_pub_;
    ros::Subscriber motor_driver_motor_status_sub_;
    ros::Subscriber motor_driver_cmd_yaw_sub_;
    ros::Subscriber motor_driver_cmd_pitch_sub_;

    ros::SubscriberStatusCallback connect_cb_motor_cmd;
    ros::SubscriberStatusCallback disconnect_cb_motor_cmd;
    
	void motor_driver_cmd_publish();
    void motor_driver_status_callBack(const std_msgs::String::ConstPtr& msg);
    void command_yaw_callBack(const std_msgs::Float32::ConstPtr& msg);
    void command_pitch_callBack(const std_msgs::Float32::ConstPtr& msg);

  private:
    void pub_topic_get();
    void pub_init();
    void pub_shutdown();
    void sub_topic_get();
    void sub_init();
    void sub_shutdown();
    void connectCb_motor_cmd(const ros::SingleSubscriberPublisher& ssp)
    {
        if(motor_driver_motor_cmd_pub_.getNumSubscribers() > 1) return;
        ROS_INFO("%s connected !", topic_motor_driver_motor_cmd_pub.c_str());
  	    sub_init();
		sub_topic_get();
    }
    void disconnectCb_motor_cmd(const ros::SingleSubscriberPublisher&)
    {
        if(motor_driver_motor_cmd_pub_.getNumSubscribers() > 0) return;
        ROS_WARN("%s disconnected !", topic_motor_driver_motor_cmd_pub.c_str());
        sub_shutdown();
    }

  private:
	float cmd_yaw_ = 0;
	float cmd_pitch_ = 0;
	string motor_status;

  public:
    Motor_Driver(ros::NodeHandle& nh);
    ~Motor_Driver();
    void run();

  public:
    virtual void init()
    {
      connect_cb_motor_cmd    = boost::bind(&Motor_Driver::connectCb_motor_cmd, this, _1);
      disconnect_cb_motor_cmd = boost::bind(&Motor_Driver::disconnectCb_motor_cmd, this, _1);
      pub_init();
      pub_topic_get();
      //sub_init();
      //sub_topic_get();
	  #ifdef _ROS_LINK_H_
	  ros_link = new ROS_Link(n_, nodeName);
	  ros_link -> pub_init();
	  ros_link -> sub_init();
	  ros_link -> add_cell(motor_driver_cmd_yaw_sub_, topic_motor_driver_cmd_yaw_sub);
	  ros_link -> add_cell(motor_driver_cmd_pitch_sub_, topic_motor_driver_cmd_pitch_sub);
	  #endif
    }
};

Motor_Driver::Motor_Driver(ros::NodeHandle& nh) : n_(nh)
{ 
}

Motor_Driver::~Motor_Driver()
{
	#ifdef _ROS_LINK_H_
	if(ros_link != NULL || ros_link != this) delete ros_link;
	#endif
}

void Motor_Driver::run()
{
}

void Motor_Driver::motor_driver_cmd_publish()
{
	std_msgs::String msg;
	string motor_cmd_yaw = HEADER  YAW;
	string motor_cmd_pitch = HEADER  PITCH;
	int value_yaw = cmd_yaw_ * float(ANG_MS_MAX - ANG_MS_MIN) + float(ANG_MS_MIN);
	int value_pitch = cmd_pitch_ * float(ANG_MS_MAX - ANG_MS_MIN) + float(ANG_MS_MIN);
	stringstream token;
	string str;
	token << value_yaw;
	token >> str;
	motor_cmd_yaw = motor_cmd_yaw + str;
	token.clear();
	token << value_pitch;
	token >> str;
	motor_cmd_pitch = motor_cmd_pitch + str;
	msg.data = motor_cmd_yaw + " " + motor_cmd_pitch;
	motor_driver_motor_cmd_pub_.publish(msg);
}

void Motor_Driver::motor_driver_status_callBack(const std_msgs::String::ConstPtr& msg)
{ 
}


void Motor_Driver::command_yaw_callBack(const std_msgs::Float32::ConstPtr& msg)
{ 
    cmd_yaw_ = (msg -> data > 1)? 1.0 : msg -> data;
    cmd_yaw_ = (cmd_yaw_ < 0)? 0 : cmd_yaw_;
}

void Motor_Driver::command_pitch_callBack(const std_msgs::Float32::ConstPtr& msg)
{
    cmd_pitch_ = (msg -> data > 1)? 1.0 : msg -> data;
    cmd_pitch_ = (cmd_pitch_ < 0)? 0 : cmd_pitch_;
}

void Motor_Driver::pub_topic_get()
{
    topic_motor_driver_motor_cmd_pub = motor_driver_motor_cmd_pub_.getTopic();
}

void Motor_Driver::pub_init()
{
    ROS_INFO("Publisher %s initiating !", topic_motor_driver_motor_cmd_pub.c_str());
	motor_driver_motor_cmd_pub_ = n_.advertise< std_msgs::String>(topic_motor_driver_motor_cmd_pub.c_str(), queue_size);
}

void Motor_Driver::pub_shutdown()
{
    ROS_WARN("Publisher %s shuting down !", topic_motor_driver_motor_cmd_pub.c_str());
    motor_driver_motor_cmd_pub_.shutdown();
}

void Motor_Driver::sub_topic_get()
{   
    topic_motor_driver_motor_status_sub = motor_driver_motor_status_sub_.getTopic();
    topic_motor_driver_cmd_yaw_sub = motor_driver_cmd_yaw_sub_.getTopic();
    topic_motor_driver_cmd_pitch_sub = motor_driver_cmd_pitch_sub_.getTopic();
}

void Motor_Driver::sub_init()
{
    ROS_INFO("Subscriber %s initiating !", topic_motor_driver_motor_status_sub.c_str());
	motor_driver_motor_status_sub_ = n_.subscribe(topic_motor_driver_motor_status_sub.c_str(), queue_size, &Motor_Driver::motor_driver_status_callBack, this);
    ROS_INFO("Subscriber %s initiating !", topic_motor_driver_cmd_yaw_sub.c_str());
	motor_driver_cmd_yaw_sub_ = n_.subscribe(topic_motor_driver_cmd_yaw_sub.c_str(), queue_size, &Motor_Driver::command_yaw_callBack, this);
    ROS_INFO("Subscriber %s initiating !", topic_motor_driver_cmd_pitch_sub.c_str());
	motor_driver_cmd_pitch_sub_ = n_.subscribe(topic_motor_driver_cmd_pitch_sub.c_str(), queue_size, &Motor_Driver::command_pitch_callBack, this);
}

void Motor_Driver::sub_shutdown()
{
    ROS_WARN("Subscriber %s shuting down !", topic_motor_driver_motor_status_sub.c_str());
    motor_driver_motor_status_sub_.shutdown();
    ROS_WARN("Subscriber %s shuting down !", topic_motor_driver_cmd_yaw_sub.c_str());
    motor_driver_cmd_yaw_sub_.shutdown();
    ROS_WARN("Subscriber %s shuting down !", topic_motor_driver_cmd_pitch_sub.c_str());
    motor_driver_cmd_pitch_sub_.shutdown();
}


#endif
