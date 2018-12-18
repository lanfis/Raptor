#pragma once
#ifndef _MOTOR_CONTROL_H_
#define _MOTOR_CONTROL_H_

#include <ros/ros.h>
#include <nodelet/nodelet.h>
//#include <sstream> // for converting the command line parameter to integer
#include <string>
#include <cstring>
#include <sstream>
#include <std_msgs/Int32.h>
#include <std_msgs/Bool.h>
#include <std_msgs/String.h>
#include <fstream>


#include "matrix/MATRIX_LINK.h"
#include "Motor.h"
#include "Motor_Com.h"

using namespace std;
using namespace ros;

class Motor_Control
{    
  public:
    string nodeName = "Motor_Control";
    string topic_data_sub = "Motor_Control/motor_data_sub";
    string topic_data_pub = "Motor_Control/motor_data_pub";
    string topic_control_data_sub = "Motor_Control/control_data_sub";
    string topic_control_data_pub = "Motor_Control/control_data_pub";

  private:
    boost::shared_ptr< std_msgs::String > msg_data_;
    boost::shared_ptr< std_msgs::String > msg_control_data_;
    int queue_size = 64;
    ROS_Link *ros_link;
    Motor motor[16];
    char com[8];
    int com_size = 0;
    string ctr;
    
    ros::NodeHandle n_;
    ros::SubscriberStatusCallback connect_cb_data;
    ros::SubscriberStatusCallback disconnect_cb_data;
      
    ros::Subscriber data_sub_;
    ros::Publisher  data_pub_;
    ros::Subscriber control_data_sub_;
    ros::Publisher  control_data_pub_;


  private:
    void pub_topic_get();
    void pub_init();
    void pub_shutdown();
    void sub_topic_get();
    void sub_init();
    void sub_shutdown();

    void connectCb_data(const ros::SingleSubscriberPublisher& ssp)
    {
      if(data_pub_.getNumSubscribers() > 1) return;
      string status = topic_control_data_pub + " connected !";
      OUT_INFO(nodeName.c_str(), status);
      sub_init();
      sub_topic_get();
    }
    void disconnectCb_data(const ros::SingleSubscriberPublisher& ssp)
    {
      if(data_pub_.getNumSubscribers() > 0) return;
      string status = topic_control_data_pub + " disconnected !";
      OUT_WARN(nodeName.c_str(), status);
      sub_shutdown();
    }

  private:
    void data_publish();
    void data_callBack(const std_msgs::String::ConstPtr& msg);

    bool msg_resolve_position(string& msg)      {if(msg.length() < 3) return false; if(msg[1] != MOTOR_FUNC_POSITION) return false;     motor[int(msg[2])].position = int(msg[3]) * 256 + int(msg[4]); return true;};
    bool msg_resolve_speed(string& msg)         {if(msg.length() < 3) return false; if(msg[1] != MOTOR_FUNC_SPEED) return false;        motor[int(msg[2])].speed = int(msg[3]) * 256 + int(msg[4]); return true;};
    bool msg_resolve_load(string& msg)          {if(msg.length() < 3) return false; if(msg[1] != MOTOR_FUNC_LOAD) return false;         motor[int(msg[2])].load = int(msg[3]) * 256 + int(msg[4]); return true;};
    bool msg_resolve_voltage(string& msg)       {if(msg.length() < 3) return false; if(msg[1] != MOTOR_FUNC_VOLTAGE) return false;      motor[int(msg[2])].voltage = int(msg[4]); return true;};
    bool msg_resolve_temperature(string& msg)   {if(msg.length() < 3) return false; if(msg[1] != MOTOR_FUNC_TEMPERATURE) return false;  motor[int(msg[2])].temperature = int(msg[4]); return true;};
    bool msg_resolve_torque_enable(string& msg) {if(msg.length() < 3) return false; if(msg[1] != MOTOR_FUNC_TORQUE) return false;       if(int(msg[3]) * 256 + int(msg[4]) == 0){motor[int(msg[2])].torque = false;} else{motor[int(msg[2])].torque = true;} return true;};

    void msg_request_read(){COM_INST = MOTOR_INST_READ; com_size = 5;};
    void msg_request_write(){COM_INST = MOTOR_INST_WRITE; com_size = 5;};
    void msg_request_position(int& id){COM_FUNC = MOTOR_FUNC_POSITION; COM_ID = char(id);};
    void msg_request_speed(int& id){COM_FUNC = MOTOR_FUNC_SPEED; COM_ID = char(id);};
    void msg_request_load(int& id){COM_FUNC = MOTOR_FUNC_LOAD; COM_ID = char(id);};
    void msg_request_voltage(int& id){COM_FUNC = MOTOR_FUNC_VOLTAGE; COM_ID = char(id);};
    void msg_request_temperature(int& id){COM_FUNC = MOTOR_FUNC_TEMPERATURE; COM_ID = char(id);};
    void msg_request_torque_enable(int& id){COM_FUNC = MOTOR_FUNC_TORQUE; COM_ID = char(id);};
    void msg_request_data(int data){COM_DATA = char(data/256); COM_DATA2 = char(data%256);};

    void get_position(int& id)      {msg_request_read(); msg_request_position(id); data_publish();};
    void get_speed(int& id)         {msg_request_read(); msg_request_speed(id); data_publish();};
    void get_load(int& id)          {msg_request_read(); msg_request_load(id); data_publish();};
    void get_voltage(int& id)       {msg_request_read(); msg_request_voltage(id); data_publish();};
    void get_temperature(int& id)   {msg_request_read(); msg_request_temperature(id); data_publish();};
    //void get_torque_enable(int& id) {msg_request_read(); msg_request_torque_enable(id); data_publish();};

    void set_position(int& id, int data)        {motor[id].position = data;     msg_request_write(); msg_request_position(id); msg_request_data(data); data_publish();};
    void set_speed(int& id, int data)           {motor[id].speed = data;        msg_request_write(); msg_request_speed(id); msg_request_data(data); data_publish();};
    void set_load_limit(int& id, int data)      {motor[id].load_limit = data;   msg_request_write(); msg_request_load(id); msg_request_data(data); data_publish();};
    void set_torque_enable(int& id, bool data)  {motor[id].torque = data;       msg_request_write(); msg_request_torque_enable(id); if(data) msg_request_data(1);else msg_request_data(0); data_publish();};

  private:
    void control_data_publish();
    void control_data_callBack(const std_msgs::String::ConstPtr& msg);
    /*msg resolve*/
    bool control_msg_resolve_set_position(string& msg)      {return (msg[0] == CONTROL_INST_SET & msg[1] == CONTROL_FUNC_POSITION)? true : false;};
    bool control_msg_resolve_set_speed(string& msg)         {return (msg[0] == CONTROL_INST_SET & msg[1] == CONTROL_FUNC_SPEED)? true : false;};
    bool control_msg_resolve_set_load_limit(string& msg)    {return (msg[0] == CONTROL_INST_SET & msg[1] == CONTROL_FUNC_LOAD)? true : false;};
    bool control_msg_resolve_set_torque_enable(string& msg) {return (msg[0] == CONTROL_INST_SET & msg[1] == CONTROL_FUNC_TORQUE)? true : false;};
    
    bool control_msg_resolve_get_position(string& msg)      {return (msg[0] == CONTROL_INST_GET & msg[1] == CONTROL_FUNC_POSITION)? true : false;};
    bool control_msg_resolve_get_speed(string& msg)         {return (msg[0] == CONTROL_INST_GET & msg[1] == CONTROL_FUNC_SPEED)? true : false;};
    bool control_msg_resolve_get_load(string& msg)          {return (msg[0] == CONTROL_INST_GET & msg[1] == CONTROL_FUNC_LOAD)? true : false;};
    bool control_msg_resolve_get_voltage(string& msg)       {return (msg[0] == CONTROL_INST_GET & msg[1] == CONTROL_FUNC_VOLTAGE)? true : false;};
    bool control_msg_resolve_get_temperature(string& msg)   {return (msg[0] == CONTROL_INST_GET & msg[1] == CONTROL_FUNC_TEMPERATURE)? true : false;};
    
    bool control_msg_resolve_set_position_hard(string& msg) {return (msg[0] == CONTROL_INST_SET & msg[1] == CONTROL_FUNC_POSITION_HARD)? true : false;};
    bool control_msg_resolve_set_position_soft(string& msg) {return (msg[0] == CONTROL_INST_SET & msg[1] == CONTROL_FUNC_POSITION_SOFT)? true : false;};
    /*control to motor*/
    void motor_init(int& id){};
    void motor_set_position(int& id, int data)          {set_position(id, data);};
    void motor_set_speed(int& id, int data)             {set_speed(id, data);};
    void motor_set_load_limit(int& id, int data)        {set_load_limit(id, data);};
    void motor_set_torque_enable(int& id, int data)     {set_torque_enable(id, data);};
    
    void motor_get_position(int& id)        {get_position(id);};
    void motor_get_speed(int& id)           {get_speed(id);};
    void motor_get_load(int& id)            {get_load(id);};
    void motor_get_voltage(int& id)         {get_voltage(id);};
    void motor_get_temperature(int& id)     {get_temperature(id);};
    
    void motor_set_position_hard(int& id, int data)     {set_position(id, data); set_load_limit(id, 1023);};
    void motor_set_position_soft(int& id, int data)     {set_position(id, data); set_load_limit(id, 64);};
    /*motor to control*/
    void motor_status_position(int& id, int& data, char& status);
    void motor_status_speed(int& id, int& data, char& status);
    void motor_status_load(int& id, int& data, char& status);
    void motor_status_voltage(int& id, int& data, char& status);
    void motor_status_temperature(int& id, int& data, char& status);
    
  private:
    string data;
    int data_size;
    string control_data;
    int control_data_size;
    string status;
    char info_level;
    string motor_status_inst, motor_status_func, motor_status_id, motor_status_data, motor_status_dlc;
    bool msg_ack = false;

  public:
    Motor_Control(ros::NodeHandle& nh);
    ~Motor_Control();
    void run();
    
  public:
    virtual void init()
    {
      connect_cb_data    = boost::bind(&Motor_Control::connectCb_data, this, _1);
      disconnect_cb_data = boost::bind(&Motor_Control::disconnectCb_data, this, _1);
      pub_init();
      pub_topic_get();
      
      ros_link = new ROS_Link(n_, nodeName);
      ros_link -> pub_init();
      ros_link -> sub_init();
      ros_link -> add_cell(data_sub_, topic_data_sub);
      ros_link -> add_cell(data_pub_, topic_data_pub);
      ros_link -> add_cell(control_data_sub_, topic_control_data_sub);
      ros_link -> add_cell(control_data_pub_, topic_control_data_pub);
    }
};

Motor_Control::Motor_Control(ros::NodeHandle& nh) : n_(nh), msg_data_(new std_msgs::String), msg_control_data_(new std_msgs::String)
{    
    stringstream token;
    token << CTR_DLC;
    token >> motor_status_dlc;
}

Motor_Control::~Motor_Control()
{
    if(ros_link != NULL)
        delete ros_link;
}

void Motor_Control::run()
{
}

void Motor_Control::control_data_publish()
{
    msg_control_data_ -> data = ctr;
    control_data_pub_.publish(msg_control_data_);
}

void Motor_Control::control_data_callBack(const std_msgs::String::ConstPtr& msg)
{
    string str;
    stringstream token;
    string control_data_header;
    int control_data_id;
    int control_data_data;
  
    control_data = msg -> data;
    
    istringstream msg_token(control_data);
    getline(msg_token, str, motor_status_dlc.at(0));
    control_data_header = str;
    getline(msg_token, str, motor_status_dlc.at(0));
    token << str;
    token >> control_data_id;
    token.clear();
    getline(msg_token, str, motor_status_dlc.at(0));
    token << str;
    token >> control_data_data;
    token.clear();
    if(control_msg_resolve_set_position(control_data_header))
    {
        motor_set_position(control_data_id, control_data_data);
        return;
    }
    if(control_msg_resolve_set_speed(control_data_header))
    {
        motor_set_speed(control_data_id, control_data_data);
        return;
    }
    if(control_msg_resolve_set_load_limit(control_data_header))
    {
        motor_set_load_limit(control_data_id, control_data_data);
        return;
    }
    if(control_msg_resolve_set_torque_enable(control_data_header))
    {
        motor_set_torque_enable(control_data_id, control_data_data);
        return;
    }
  
    if(control_msg_resolve_get_position(control_data_header))
    {
        motor_get_position(control_data_id);
        return;
    }
    if(control_msg_resolve_get_speed(control_data_header))
    {
        motor_get_speed(control_data_id);
        return;
    }
    if(control_msg_resolve_get_load(control_data_header))
    {
        motor_get_load(control_data_id);
        return;
    }
    if(control_msg_resolve_get_voltage(control_data_header))
    {
        motor_get_voltage(control_data_id);
        return;
    }
    if(control_msg_resolve_get_temperature(control_data_header))
    {
        motor_get_temperature(control_data_id);
        return;
    }
    
    if(control_msg_resolve_set_position_hard(control_data_header))
    {
        motor_set_position_hard(control_data_id, control_data_data);
        return;
    }
    if(control_msg_resolve_set_position_soft(control_data_header))
    {
        motor_set_position_soft(control_data_id, control_data_data);
        return;
    }
    
}

void Motor_Control::data_publish()
{
    for(int i = 0; !msg_ack && i < 10000; i++)
        continue;
    string mdata;
    mdata.assign(com, com_size);
    msg_data_ -> data = mdata;
    data_pub_.publish(msg_data_);
    com_size = 0;
    msg_ack = false;
}

void Motor_Control::data_callBack(const std_msgs::String::ConstPtr& msg)
{
    string str;
    stringstream token;
    data = msg -> data;
    info_level = data[0];
	int id = int(data[2]);
    if(info_level == MOTOR_INST_ACK)
    {
        msg_ack = true;
    }
    if(msg_resolve_position(data))      
    {
        if(info_level == MOTOR_INST_WARN)   
        {
            token << id;
            token >> str;
            status = "POSITION " + str + " : "; 
            token.clear();
            token << motor[id].position; 
            token >> str; 
            status = status + str; 
            token.clear();
            OUT_WARN(nodeName.c_str(), status); 
        } 
        else if(info_level == MOTOR_INST_FATAL)  
        {
            token << id;
            token >> str;
            status = "POSITION " + str + " : "; 
            token.clear();
            token << motor[id].position; 
            token >> str; 
            status = status + str; 
            token.clear();
            OUT_ERROR(nodeName.c_str(), status); 
        }
        motor_status_position(id, motor[id].position, info_level);
        control_data_publish();
        return;
    };
    if(msg_resolve_speed(data))
    {
        if(info_level == MOTOR_INST_WARN)   
        {
            token << id;
            token >> str;
            status = "SPEED " + str + " : "; 
            token.clear();
            token << motor[id].speed; 
            token >> str; 
            status = status + str; 
            token.clear();
            OUT_WARN(nodeName.c_str(), status); 
        }
        else if(info_level == MOTOR_INST_FATAL)  
        {
            token << id;
            token >> str;
            status = "SPEED " + str + " : "; 
            token.clear();
            token << motor[id].speed; 
            token >> str; 
            status = status + str; 
            token.clear();
            OUT_ERROR(nodeName.c_str(), status); 
        }
        motor_status_speed(id, motor[id].speed, info_level);
        control_data_publish();
        return;
    };
    if(msg_resolve_load(data))          
    {
        if(info_level == MOTOR_INST_WARN)   
        {
            token << id;
            token >> str;
            status = "LOAD " + str + " : "; 
            token.clear();
            token << motor[id].load; 
            token >> str; 
            status = status + str; 
            token.clear();
            OUT_WARN(nodeName.c_str(), status); 
        }
        else if(info_level == MOTOR_INST_FATAL)  
        {
            token << id;
            token >> str;
            status = "LOAD " + str + " : "; 
            token.clear();
            token << motor[id].load; 
            token >> str; 
            status = status + str; 
            token.clear();
            OUT_ERROR(nodeName.c_str(), status); 
        }
        motor_status_load(id, motor[id].load, info_level);
        control_data_publish();
        return;
    };
    if(msg_resolve_voltage(data))       
    {
        if(info_level == MOTOR_INST_WARN)   
        {
            token << id;
            token >> str;
            status = "VOLTAGE " + str + " : "; 
            token.clear();
            token << motor[id].voltage; 
            token >> str; 
            status = status + str; 
            token.clear();
            OUT_WARN(nodeName.c_str(), status); 
        }
        else if(info_level == MOTOR_INST_FATAL)  
        {
            token << id;
            token >> str;
            status = "VOLTAGE " + str + " : "; 
            token.clear();
            token << motor[id].voltage; 
            token >> str; 
            status = status + str; 
            token.clear();
            OUT_ERROR(nodeName.c_str(), status); 
        }
        motor_status_voltage(id, motor[id].voltage, info_level);
        control_data_publish();
        return;
    };
    if(msg_resolve_temperature(data))   
    {
        if(info_level == MOTOR_INST_WARN)   
        {
            token << id;
            token >> str;
            status = "TEMPERATURE " + str + " : "; 
            token.clear();
            token << motor[id].temperature; 
            token >> str; 
            status = status + str; 
            token.clear();
            OUT_WARN(nodeName.c_str(), status); 
        }
        else if(info_level == MOTOR_INST_FATAL)  
        {
            token << id;
            token >> str;
            status = "TEMPERATURE " + str + " : "; 
            token.clear();
            token << motor[id].temperature; 
            token >> str; 
            status = status + str; 
            token.clear();
            OUT_ERROR(nodeName.c_str(), status); 
        }
        motor_status_temperature(id, motor[id].temperature, info_level);
        control_data_publish();
        return;
    };
}

void Motor_Control::motor_status_position(int& id, int& data, char& status)
{
    stringstream token; 
    token << status;
    token >> motor_status_inst;
    token.clear();
    token << CONTROL_FUNC_POSITION;
    token >> motor_status_func;
    token.clear();
    token << id;
    token >> motor_status_id;
    token.clear();
    token << data;
    token >> motor_status_data;
  
    ctr.clear();
    ctr.append(motor_status_inst);
    ctr.append(motor_status_func);
    ctr.append(motor_status_dlc);
    ctr.append(motor_status_id);
    ctr.append(motor_status_dlc);
    ctr.append(motor_status_data);
}

void Motor_Control::motor_status_speed(int& id, int& data, char& status)
{
    stringstream token; 
    token << status;
    token >> motor_status_inst;
    token.clear();
    token << CONTROL_FUNC_SPEED;
    token >> motor_status_func;
    token.clear();
    token << id;
    token >> motor_status_id;
    token.clear();
    token << data;
    token >> motor_status_data;
  
    ctr.clear();
    ctr.append(motor_status_inst);
    ctr.append(motor_status_func);
    ctr.append(motor_status_dlc);
    ctr.append(motor_status_id);
    ctr.append(motor_status_dlc);
    ctr.append(motor_status_data);
}

void Motor_Control::motor_status_load(int& id, int& data, char& status)
{
    stringstream token; 
    token << status;
    token >> motor_status_inst;
    token.clear();
    token << CONTROL_FUNC_LOAD;
    token >> motor_status_func;
    token.clear();
    token << id;
    token >> motor_status_id;
    token.clear();
    token << data;
    token >> motor_status_data;
  
    ctr.clear();
    ctr.append(motor_status_inst);
    ctr.append(motor_status_func);
    ctr.append(motor_status_dlc);
    ctr.append(motor_status_id);
    ctr.append(motor_status_dlc);
    ctr.append(motor_status_data);
}

void Motor_Control::motor_status_voltage(int& id, int& data, char& status)
{
    stringstream token; 
    token << status;
    token >> motor_status_inst;
    token.clear();
    token << CONTROL_FUNC_VOLTAGE;
    token >> motor_status_func;
    token.clear();
    token << id;
    token >> motor_status_id;
    token.clear();
    token << data;
    token >> motor_status_data;
  
    ctr.clear();
    ctr.append(motor_status_inst);
    ctr.append(motor_status_func);
    ctr.append(motor_status_dlc);
    ctr.append(motor_status_id);
    ctr.append(motor_status_dlc);
    ctr.append(motor_status_data);
}

void Motor_Control::motor_status_temperature(int& id, int& data, char& status)
{
    stringstream token; 
    token << status;
    token >> motor_status_inst;
    token.clear();
    token << CONTROL_FUNC_TEMPERATURE;
    token >> motor_status_func;
    token.clear();
    token << id;
    token >> motor_status_id;
    token.clear();
    token << data;
    token >> motor_status_data;
  
    ctr.clear();
    ctr.append(motor_status_inst);
    ctr.append(motor_status_func);
    ctr.append(motor_status_dlc);
    ctr.append(motor_status_id);
    ctr.append(motor_status_dlc);
    ctr.append(motor_status_data);
}

void Motor_Control::pub_topic_get()
{
    topic_data_pub = data_pub_.getTopic();
    topic_control_data_pub = control_data_pub_.getTopic();
}

void Motor_Control::pub_init()
{
    status = "Publisher " + topic_data_pub + " initiating !";
    OUT_INFO(nodeName.c_str(), status);
    data_pub_ = n_.advertise< std_msgs::String >(topic_data_pub, queue_size);
    status = "Publisher " + topic_control_data_pub + " initiating !";
    OUT_INFO(nodeName.c_str(), status);
    control_data_pub_ = n_.advertise< std_msgs::String >(topic_control_data_pub, queue_size);//, connect_cb_data, disconnect_cb_data);
    sub_init();
    sub_topic_get();
}

void Motor_Control::pub_shutdown()
{
    status = "Publisher " + topic_data_sub + " shuting down !";
    OUT_WARN(nodeName.c_str(), status);
    data_pub_.shutdown();
    status = "Publisher " + topic_control_data_pub + " shuting down !";
    OUT_WARN(nodeName.c_str(), status);
    control_data_pub_.shutdown();
}

void Motor_Control::sub_topic_get()
{   
    topic_data_sub = data_sub_.getTopic();
    topic_control_data_sub = control_data_sub_.getTopic();
}

void Motor_Control::sub_init()
{
    status = "Subscriber " + topic_data_sub + " initiating !";
    OUT_INFO(nodeName.c_str(), status);
    data_sub_ = n_.subscribe(topic_data_sub.c_str(), queue_size, &Motor_Control::data_callBack, this);
    status = "Subscriber " + topic_control_data_sub + " initiating !";
    OUT_INFO(nodeName.c_str(), status);
    control_data_sub_ = n_.subscribe(topic_control_data_sub.c_str(), queue_size, &Motor_Control::control_data_callBack, this);
}

void Motor_Control::sub_shutdown()
{
    status = "Subscriber " + topic_data_sub + " shuting down !";
    OUT_WARN(nodeName.c_str(), status);
    data_sub_.shutdown();
    status = "Subscriber " + topic_control_data_sub + " shuting down !";
    OUT_WARN(nodeName.c_str(), status);
    control_data_sub_.shutdown();
}
#endif
