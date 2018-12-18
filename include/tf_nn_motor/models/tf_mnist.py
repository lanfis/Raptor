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
from tf_nn_builder import NN_BUILDER
import ops.tf_util_ops as tf_util_op
from layers import *


def mnist_builder(tensor_in, input_channels=1, output_labels=10, padding="VALID", initializer=None, use_gpu=False): 
    nn = NN_BUILDER(use_gpu)
    '''   
    nn = NN_BUILDER(use_gpu)
    
    conv_1 = nn.add_conv(filters_out=32, tensor_in=tensor_in, filters_in=input_channels, kernel_shape=[5, 5, input_channels, 32], strides=[1, 1, 1, 1], initializer=initializer, pad=padding, name="conv_1")
    max_pool_1 = nn.add_max_pool(kernel_shape=[1, 2, 2, 1], strides=[1, 1, 1, 1], pad=padding, name="max_pool_1")
    conv_2 = nn.add_conv(filters_out=64, kernel_shape=[5, 5, 32, 64], strides=[1, 1, 1, 1], initializer=initializer, pad=padding, name="conv_2")
    max_pool_2 = nn.add_max_pool(kernel_shape=[1, 2, 2, 1], strides=[1, 1, 1, 1], pad=padding, name="max_pool_2")
    fc_1 = nn.add_fc(filters_out=1024, initializer=None, name="fc_1")
    relu_1 = nn.add_relu(name="relu_1")
    keep_prob = tf_util_op.add_variable_hold()
    dropout_1 = nn.add_dropout(keep_prob, name="dropput_1")
    fc_2 = nn.add_fc(filters_out=output_labels, initializer=None, name="fc_2")
    softmax = nn.add_softmax(name="softmax")
    
    
    return softmax, keep_prob
    '''
    tensor = Conv_Layer(32, kernel_size=[5, 5], padding=padding, name="conv_1")(tensor_in)
    print(tensor)
    tensor = Pooling_Layer(pool_size=[2, 2], padding=padding, type='max', name="max_pool_1")(tensor)
    print(tensor)
    tensor = Conv_Layer(64, kernel_size=[5, 5], padding=padding, name="conv_2")(tensor)
    print(tensor)
    tensor = Pooling_Layer(pool_size=[2, 2], padding=padding, type='max', name="max_pool_2")(tensor)
    print(tensor)
    tensor = Flatten_Layer()(tensor)
    tensor = Dense_Layer(1024, name="fc_1")(tensor)
    print(tensor)
    tensor = Activation_Layer('relu', name="relu_1")(tensor)
    print(tensor)
    keep_prob = tf_util_op.add_variable_hold()
    tensor = Dropout_Layer(keep_prob, name="dropout")(tensor)
    print(tensor)
    tensor = Dense_Layer(output_labels, name="fc_2")(tensor)
    print(tensor)
    tensor = Softmax_Layer()(tensor)
    print(tensor)
    
    return tensor, keep_prob
