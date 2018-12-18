#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)
main_folder = os.path.join(current_folder, "..")
sys.path.append(main_folder)


import numpy as np
import tensorflow as tf
full_path = os.path.dirname(__file__)
sys.path.append(full_path)
import ops.tf_util_ops as tf_util_op
from layers import *


def TF_NN_MODEL_BUILDER(tensor_in, padding="SAME", kernel_size=3, strides=1, kernel_filters=64): 
    '''
    tensor = Conv_Layer(filters_out=kernel_filters, 
                        kernel_size=[kernel_size, kernel_size], 
                        strides=[strides, strides], 
                        padding=padding, 
                        name="conv_1")(tensor_in)
    '''
    unit_size = 1
    for i in range(1, len(tensor_in.get_shape())):
        unit_size *= int(tensor_in.get_shape()[i])
        
    tensor = CONV_BN_Layer(filters_out=kernel_filters, 
                            kernel_size=[1, 1], 
                            strides=[1, 1], 
                            padding=padding, 
                            is_bn=True, 
                            is_conv=True, 
                            is_relu=True, 
                            dtype=None, 
                            name="conv_bn_1")(tensor_in)
    '''
    tensor = CONV_BN_Layer(filters_out=kernel_filters, 
                            kernel_size=[kernel_size, kernel_size], 
                            strides=[strides, strides], 
                            padding=padding, 
                            is_bn=True, 
                            is_conv=True, 
                            is_relu=True, 
                            dtype=None, 
                            name="conv_bn_2")(tensor)
    '''
    tensor = Flatten_Layer()(tensor)
    tensor = Dense_Layer(kernel_filters * 32, name="fc_1")(tensor)
    
    keep_prob = tf_util_op.add_variable_hold()
    tensor = Dropout_Layer(keep_prob, name="dropout_1")(tensor)
    
    tensor = Dense_Layer(kernel_filters * 32, name="fc_2")(tensor)
    
    tensor = Dense_Layer(unit_size, name="fc_2")(tensor)
    
    tensor = Activation_Layer(activation='relu', name='relu')(tensor)
    #tensor = Softmax_Layer(name="softmax")(tensor)
    
    tensor = Reshape_Layer(shape=[int(tensor_in.get_shape()[i]) for i in range(1, len(tensor_in.get_shape()))], name='reshape')(tensor)
    
    return tensor, keep_prob
                            