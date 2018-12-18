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

full_path = os.path.realpath(__file__)
current_folder, file_name = os.path.split(full_path)
sys.path.append(current_folder)
sys.path.append(current_folder + "/../matrix/python")
#from console_format import Console_Format

import numpy as np
import time
import json

import tensorflow as tf

from layers import *
import ops.tf_nn_optimizer_ops as tf_optimizer_op
import ops.tf_util_ops as tf_util_op

from models.tf_index_controler import INDEX_CONTROLER
from models.tf_dataset_builder import DATASET_BUILDER
from tf_nn_motor_model import TF_NN_MODEL_BUILDER

class TF_NN_MOTOR_NN:
    ####PUBLIC    
    data_path = os.path.join(current_folder, "..")
    weight_file_path = None
    weight_file_name = "motor_model.ckpt"
    '''
    motor_data_setting_file_path = None
    motor_data_setting_file_name = "motor_data_setting.txt"
    '''
    motor_data_record_file_path = None
    motor_data_record_file_name = "motor_data_record.txt"

    motor_status_data = []
    
    motor_size = 16
    motor_parameter = 3
    lr = 0.00001
    batch_size = 4
    
    ####PRIVATE
    ver = "1.0"
    ptime = time.time()
    sess_ = None
    #saver_ = tf.train.Saver()
    
    flag_nn_init = False
    
    
    motor_data_record_content = None
    
    motor_data_record_controler = INDEX_CONTROLER() 
    tf_dataset_builder = DATASET_BUILDER()
    
    ##PRIVATE   
    motor_status_input = None
    motor_recommand_output = None
    motor_recommand_output_status_result = None
    
    motor_dataset_present_motor_status_input = None
    motor_dataset_next_motor_status_input = None
    motor_dataset_iterator = None
    
    optimizer = None
    keep_prob = None
    train_step = None
    loss = None
    
    
    def run(self):
        if not self.flag_nn_init:
            self.tf_init()
        return 
    
    def init(self):
        print("--Creating motor model ...")
        self.nn_model_init()
        print(self.motor_recommand_output)
        print("--Creating optimizer ...")
        self.optimizer_init()
        print("--Initializing dataset ...")
        self.dataset_init()
        print("--Initializing training functions ...")
        self.training_init()
        self.flag_nn_init = True    
        
    def training_init(self):
        '''
        diff = keras.backend.abs(target_bbox - rpn_bbox)
        less_than_one = keras.backend.cast(keras.backend.less(diff, 1.0), "float32")
        loss = (less_than_one * 0.5 * diff**2) + (1 - less_than_one) * (diff - 0.5)
        '''
        print("--Setting loss function ...")
        diff = tf_util_op.tensor_abs(self.motor_recommand_output - self.motor_recommand_output_status_result)
        less_than_one = tf_util_op.tensor_cast(tf_util_op.tensor_less(diff, 1.0), tf.float32)
        tensor_match_loss = (less_than_one * 0.5 * diff**2) + (1 - less_than_one) * (diff - 0.5)
        
        tensor_left_right_balance = tf_util_op.tensor_index(self.motor_recommand_output_status_result, [[[0, 11, 2]], [[1, 11, 2]], [[2, 11, 2]], [[3, 11, 2]]])
        
        
        tensor_fore_back_balance  = tf_util_op.tensor_index(self.motor_recommand_output_status_result, [[[0, 4, 2]], [[1, 4, 2]], [[2, 4, 2]], [[3, 4, 2]]]) + tf_util_op.tensor_index(self.motor_recommand_output_status_result, [[[0, 7, 2]], [[1, 7, 2]], [[2, 7, 2]], [[3, 7, 2]]])
        #print(tensor_left_right_balance)
        #tensor_fore_back_balance = self.motor_recommand_output_status_result[3, 2, 0] - self.motor_recommand_output_status_result[6, 2, 0]
        tensor_scores = [tensor_match_loss, tensor_left_right_balance, tensor_fore_back_balance]
        tensor_loss = tensor_scores
        '''
        tensor_loss = tf.constant(tensor_scores, 
                                    dtype=tf.float32, 
                                    name="nn_motor_loss")
        '''
        #tensor_loss = tf_util_op.abs(tensor_loss)
        self.loss = tf_util_op.tensor_reducemean(tensor_loss)

        print("--Setting training step function ...")
        self.train_step = tf_optimizer_op.optimizer_minimize(self.optimizer, self.loss)
        '''
        #OUT.INFO(self.node_name, "Setting prediction function ...")  
        #predict = tf_util_op.tensor_argmax(self.motor_recommand_output)

        #OUT.INFO(self.node_name, "Setting accuracy function ...")  
        #accuracy = tf_util_op.accuracy(tf_util_op.tensor_cast(predict, tf.int32), tf_util_op.tensor_cast(tf_util_op.tensor_argmax(label_input), tf.int32))
        '''
        return 
    
    def dataset_init(self):     
        self.motor_data_record_content = self.motor_data_record_controler.load_index_file(is_create_data=True)
        for i in range(len(self.motor_data_record_content)):
            self.motor_data_record_content[int(i)] = self.dataset_data_reader(self.motor_data_record_content[int(i)])
        #present_motor_status_list = [self.motor_data_record_content[int(i)][0] for i in range(len(self.motor_data_record_content))]
        #next_motor_status_list       = [self.motor_data_record_content[int(i)][1] for i in range(len(self.motor_data_record_content))]
        
        #tensor_present_motor_status_list = tf_util_op.tensor_cast(present_motor_status_list, tf.float32)
        #tensor_next_motor_status_list    = tf_util_op.tensor_cast(next_motor_status_list, tf.float32)
        self.motor_dataset_iterator = self.dataset_model_init(len(self.motor_data_record_content))         
        return self.motor_dataset_iterator
    
    def dataset_model_init(self, dataset_size): 
        self.motor_dataset_present_motor_status_input = tf_util_op.add_variable_hold([dataset_size, self.motor_size, self.motor_parameter, 1], dtype=tf.float32, name="present_motor_dataset_input")
        self.motor_dataset_next_motor_status_input    = tf_util_op.add_variable_hold([dataset_size, self.motor_size, self.motor_parameter, 1], dtype=tf.float32, name="next_motor_dataset_input")
        
        self.tf_dataset_builder.dataset_tensor([self.motor_dataset_present_motor_status_input, 
                                                self.motor_dataset_next_motor_status_input])
        self.tf_dataset_builder.set_repeat()
        self.tf_dataset_builder.set_shuffle(dataset_size)
        self.tf_dataset_builder.set_batch(self.batch_size)
        return self.tf_dataset_builder.set_iterator(type="initializable")
        
    def dataset_data_formatter(self, present_stage_motor_status_nn_data, next_stage_motor_status_nn_data):#nn_data => serialize nn_data
        return json.dumps([present_stage_motor_status_nn_data, next_stage_motor_status_nn_data])
        
    def dataset_data_reader(self, content):
        return json.loads(content)
        
    def dataset_data_recorder(self, content):
        return self.motor_data_record_controler.write_index_file(content)
    
    def optimizer_init(self):
        self.optimizer = tf_optimizer_op.optimizer_adam(learning_rate=self.lr)
        return True
    
    def nn_model_init(self):
        if self.sess_ != None:
            self.close_session(self.sess_)
        self.sess_ = tf.Session()
        
        self.motor_status_input  = tf_util_op.add_variable_hold([self.batch_size, self.motor_size, self.motor_parameter, 1], dtype=tf.float32, name="motor_status_input")
        self.motor_recommand_output_status_result = tf_util_op.add_variable_hold([self.batch_size, self.motor_size, self.motor_parameter, 1], dtype=tf.float32, name="motor_recommand_status_result")
        
        tensor_model_out = TF_NN_MODEL_BUILDER(tensor_in=self.motor_status_input, padding="SAME", kernel_size=3, strides=1, kernel_filters=64)
        [self.motor_recommand_output, self.keep_prob] = tensor_model_out
        return True
        
    def close_session(self, sess):
        if(sess != None):
            sess.close()        
            
    def __init__(self):
        pass

    def __del__(self):
        self.close_session(self.sess_)


