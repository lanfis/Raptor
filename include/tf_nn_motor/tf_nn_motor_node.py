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
import time
import numpy as np

full_path = os.path.realpath(__file__)
current_folder, file_name = os.path.split(full_path)
sys.path.append(current_folder)
sys.path.append(current_folder + "/../matrix/python")
from console_format import Console_Format

import numpy as np
import time

import tensorflow as tf

from layers import *
import ops.tf_nn_optimizer_ops as tf_optimizer_op
import ops.tf_util_ops as tf_util_op

from models.tf_index_controler import INDEX_CONTROLER
from models.dataset_retriever import DATASET_RETRIEVER
from models.dataset_label_encoder import DATASET_LABEL_ENCODER
from tf_nn_motor_com import TF_NN_MOTOR_COM

OUT = Console_Format()
class TF_NN_MOTOR:
    ####PUBLIC
    node_name = "TF_NN_MOTOR"
    queue_size = 8
    topic_motor_control_status_sub = "motor_control_status_sub"
    topic_motor_control_status_pub = "motor_control_status_pub"

    ####PRIVATE
    ver = "1.0"
    motor_control_status_sub_ = None
    motor_control_status_pub_ = None
    
    motor_com = TF_NN_MOTOR_COM()
    sess = None
    saver = None

    def motor_control_msg_resolve(self, msg):
        pass
    
    def motor_control_status_publish(self, msg):
        pass
            
    def motor_control_status_callback(self, msg):
        pass
        
    def initialize(self):
        OUT.INFO(self.node_name, "Initializing ...")
        
    def pub_init(self):
        OUT.INFO(self.node_name, "Publisher {} initiating !".format(self.topic_motor_control_status_pub))
        self.motor_control_status_pub_ = rospy.Publisher(self.topic_motor_control_status_pub, String, queue_size=self.queue_size)
        
    def sub_init(self):
        OUT.INFO(self.node_name, "Subscriber {} initiating !".format(self.topic_motor_control_status_sub))
        self.motor_control_status_sub_ = rospy.Subscriber(self.topic_motor_control_status_sub, String, self.motor_control_status_callback)
        
    def topic_init(self):    
        self.topic_motor_control_status_pub = self.node_name + "/" + self.topic_motor_control_status_pub
        self.topic_motor_control_status_sub = self.node_name + "/" + self.topic_motor_control_status_sub
            
    def __init__(self, node_name=None):
        self.node_name = self.node_name if node_name is None else node_name
        tf.logging.set_verbosity(tf.logging.INFO)
        self.initialize()
        self.topic_init()
        self.pub_init()
        self.sub_init()

    def __del__(self):
        if(self.sess != None):
            self.sess.close()
        #print("## Program Done ! ##")
        OUT.INFO(self.node_name, "Closing ...")


