#!/usr/bin/env python
# license removed for brevity
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
'''
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Bool
#from sensor_msgs.msg import Image
#from cv_bridge import CvBridge, CvBridgeError

full_path = os.path.realpath(__file__)
current_folder, file_name = os.path.split(full_path)
sys.path.append(current_folder)
sys.path.append(current_folder + "/../matrix/python")
from console_format import Console_Format

import numpy as np
import time
import json

from tf_nn_motor_com import TF_NN_MOTOR_COM
from tf_nn_motor_adjust import MOTOR_ADJUST
from tf_nn_motor_nn import TF_NN_MOTOR_NN

OUT = Console_Format()
class TF_NN_MOTOR:
    ####PUBLIC
    node_name = "TF_NN_MOTOR"
    topic_motor_control_sub = "motor_control_sub"
    topic_motor_control_pub = "motor_control_pub"
    topic_motor_status_sub = "motor_status_sub"
    topic_motor_status_pub = "motor_status_pub"
    
    data_path = os.path.join(current_folder, "..")
    weight_file_path = None
    weight_file_name = "motor_model.ckpt"
    '''
    motor_data_setting_file_path = None
    motor_data_setting_file_name = "motor_data_setting.txt"
    '''
    motor_data_record_file_path = None
    motor_data_record_file_name = "motor_data_record.txt"

    motor_size = 14 + 1#plus suggest motion
    motor_parameter = 3
    lr = 0.00001
    batch_size = 4
    
    motor_cmd_list = []
    motor_status_data = []
    
    queue_size = motor_size * 3
    
    ####PRIVATE
    ver = "1.0"
    ptime = time.time()
    motor_control_sub_ = None
    motor_control_pub_ = None
    motor_status_sub_ = None
    motor_status_pub_ = None
    
    motor_com_ = TF_NN_MOTOR_COM()
    
    flag_motor_init = False
    flag_nn_init = False
    
    ####PRIVATE    
    #motor_data_setting_controler_ = INDEX_CONTROLER()
    #motor_data_record_controler_ = INDEX_CONTROLER()
    motor_adjust_ = MOTOR_ADJUST()
    
    
    ##PRIVATE   
    tf_nn = TF_NN_MOTOR_NN()
    '''
    optimizer = tf_optimizer_op.optimizer_adam(learning_rate=lr)
    #initializer =  tf_builder.initializer_xavier(is_uniform=False)
    motor_status_input  = tf_util_op.add_variable_hold([None, motor_size, 3, 1], dtype=tf.float32, name="motor_status_input")
    motor_recommand_output, keep_prob = TF_NN_MODEL_BUILDER(tensor_in=motor_status_input, tensor_out=motor_size * 3, padding="SAME", kernel_size=3, strides=1, kernel_filters=64)
    '''
    
    def run(self):
        if not self.flag_motor_init:
            if self.motor_com_.motor_status_list != None:
                OUT.INFO(self.node_name, "Motor data readed ! Initialization starting ...")  
                self.initialize()
                return
            else:
                OUT.WARN(self.node_name, "Waiting for motor data ...")  
                self.initialize()##debug
                return
                
        self.motor_adjust_.adjust(self.motor_cmd_list)
        while len(self.motor_cmd_list) > 0:
            self.motor_status_publish(*self.motor_cmd_list.pop(0))
        
        self.motor_com_2_nn_data()
        #print(self.motor_status_data)##debug
    
    def motor_com_2_nn_data(self):
        if self.motor_com_.motor_status_list == None:
            return
        for i in range(self.motor_size):
            if str(i) in self.motor_com_.motor_status_list:
                transfer_data = self.motor_com_2_nn_data_(self.motor_com_.motor_status_list[str(i)])
            else:
                transfer_data = [[int(i)], [0], [0], [0], [0], [0]]
                
            if len(self.motor_status_data) < self.motor_size:
                self.motor_status_data.extend(transfer_data)
            else:
                if cmp(self.motor_status_data[int(i)], transfer_data) != 0:
                    self.motor_status_data[int(i)] = transfer_data
        
        return [self.motor_status_data[int(i)][1:4] for i in range(self.motor_size)]
        #return self.motor_status_data
    
    def motor_com_2_nn_data_(self, motor_data):
        return [[motor_data['id'] if motor_data['id'] in motor_data else -1], 
                [motor_data['position'] if motor_data['position'] in motor_data else 0], 
                [motor_data['speed'] if motor_data['speed'] in motor_data else 0], 
                [motor_data['load'] if motor_data['load'] in motor_data else 0], 
                [motor_data['voltage'] if motor_data['voltage'] in motor_data else 0], 
                [motor_data['temperature'] if motor_data['temperature'] in motor_data else 0]]
    '''
    def tf_nn_run(self):
        if not self.flag_nn_init:
            OUT.WARN(self.node_name, "TF NN is not initialized ! Initialization starting ...")  
            self.tf_init()
        return 
    '''
    def tf_init(self):
        self.tf_nn.weight_file_path = self.weight_file_path
        '''
        self.tf_nn.motor_data_setting_file_path = self.motor_data_setting_file_path
        '''
        self.tf_nn.motor_data_record_file_path = self.motor_data_record_file_path
        self.tf_nn.motor_size = self.motor_size
        self.tf_nn.motor_parameter = self.motor_parameter
        self.tf_nn.lr = self.lr
        self.tf_nn.batch_size = self.batch_size
        
        self.flag_nn_init = self.tf_nn.init()
        return self.flag_nn_init
        
    def motor_init(self):
        self.motor_com_.motor_size = self.motor_size
        self.motor_cmd_list.extend(self.motor_adjust_.init())
        
    def motor_control_publish(self, msg):
        pass
            
    def motor_control_callback(self, msg):
        if msg.data:
            pass
    
    def motor_status_publish(self, motor_id, func, data, inst='SET'):
        msg = self.motor_status_msg_generate(motor_id, func, data, inst)
        print(msg)
        tm = time.time()
        while tm - self.ptime < 0.01:
            time.sleep(0.0001)
            tm = time.time()
        self.ptime = tm
        self.motor_status_pub_.publish(msg)
        
    def motor_status_msg_generate(self, motor_id, func, data, inst='SET'):
        return self.motor_com_.get_motor_msg(motor_id, func, data, inst)
            
    def motor_status_callback(self, msg):
        if msg.data:
            self.motor_status_msg_resolve(msg.data)
        #print(self.motor_com_.motor_status_list)
    
    def motor_status_msg_resolve(self, msg):
        self.motor_com_.set_motor_msg(msg)
        return
        
    def initialize(self):
        OUT.INFO(self.node_name, "Initializing ...")  
        
        self.weight_file_path = os.path.join(self.data_path, self.weight_file_name)
        '''    
        self.motor_data_setting_file_path = os.path.join(self.data_path, self.motor_data_setting_file_name)
        OUT.INFO(self.node_name, "Motor data setting file : \"{}\" loading ...".format(self.motor_data_setting_file_path))
        #self.motor_data_setting_controler_.index_file = self.motor_data_setting_file_path
        #self.motor_data_file_content = self.motor_data_setting_controler_.load_index_file(is_create_data=True)
        if not self.check_file(self.motor_data_setting_file_path):
            OUT.WARN(self.node_name, "Motor data setting file : \"{}\" not found !".format(self.motor_data_setting_file_path))
        '''
        self.motor_data_record_file_path = os.path.join(self.data_path, self.motor_data_record_file_name)
        OUT.INFO(self.node_name, "Motor data record file : \"{}\" loading ...".format(self.motor_data_record_file_path))
        #self.motor_data_record_controler_.index_file = self.motor_data_record_file_path
        #self.motor_data_file_content = self.motor_data_record_controler_.load_index_file(is_create_data=True)
        if not self.check_file(self.motor_data_record_file_path):
            OUT.WARN(self.node_name, "Motor data record file : \"{}\" not found !".format(self.motor_data_record_file_path))
            
        
        OUT.INFO(self.node_name, "Initializing motor ...") 
        self.motor_init()
        
        OUT.INFO(self.node_name, "Initializing tf session ...")        
        self.tf_init()
        #OUT.INFO(self.node_name, "Initializing tf saver...")        
        #self.saver = tf.train.Saver()
        
        self.flag_motor_init = True
        
    def pub_init(self):
        OUT.INFO(self.node_name, "Publisher {} initiating !".format(self.topic_motor_control_pub))
        self.motor_control_pub_ = rospy.Publisher(self.topic_motor_control_pub, String, queue_size=self.queue_size)
        
        OUT.INFO(self.node_name, "Publisher {} initiating !".format(self.topic_motor_status_pub))
        self.motor_status_pub_ = rospy.Publisher(self.topic_motor_status_pub, String, queue_size=self.queue_size)
        
    def sub_init(self):
        OUT.INFO(self.node_name, "Subscriber {} initiating !".format(self.topic_motor_control_sub))
        self.motor_control_sub_ = rospy.Subscriber(self.topic_motor_control_sub, String, self.motor_control_callback)
        
        OUT.INFO(self.node_name, "Subscriber {} initiating !".format(self.topic_motor_status_sub))
        self.motor_status_sub_ = rospy.Subscriber(self.topic_motor_status_sub, String, self.motor_status_callback)
        
    def topic_init(self):    
        self.topic_motor_control_pub = self.node_name + "/" + self.topic_motor_control_pub
        self.topic_motor_control_sub = self.node_name + "/" + self.topic_motor_control_sub
        self.topic_motor_status_pub = self.node_name + "/" + self.topic_motor_status_pub
        self.topic_motor_status_sub = self.node_name + "/" + self.topic_motor_status_sub
            
    def check_file(self, file_path):
        if not os.path.isfile(file_path):
            OUT.WARN(self.node_name, "File : \"{}\" not found !".format(file_path))
            return False
        return True
    '''
    def load_file(self, fid, file_path, content):
        if self.check_file(file_path):
            fid = open(file_path, 'r+')
            OUT.INFO(self.node_name, "File : \"{}\" loading ...".format(file_path))
            content = fid.readlines()
            return True
        return False
    
    def close_file(self, fid):
        if fid != None:
            fid.close
    '''
    '''
    def close_session(self, sess):
        if(sess != None):
            sess.close()        
    '''
    def __init__(self, node_name=None):
        self.node_name = self.node_name if node_name is None else node_name
        self.topic_init()
        self.pub_init()
        self.sub_init()
        
        #self.run()

    def __del__(self):
        #print("## Program Done ! ##")
        OUT.INFO(self.node_name, "Closing ...")


