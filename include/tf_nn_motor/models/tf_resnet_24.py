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


#Total of layers is only half of the resnet-50
#Resnet -24

def resnet_builder(tensor_in, input_channels=1, output_labels=10, padding="SAME", kernel_size=3, strides=1, kernel_filters=64, bottleneck_depth=2, initializer=None, use_gpu=True):            
    nn = NN_BUILDER(use_gpu)
    conv_bn = conv_bn_layer(filters_out=kernel_filters, 
                            tensor_in=tensor_in, 
                            filters_in=None, 
                            kernel_shape=[kernel_size, kernel_size], 
                            strides=[strides, strides], 
                            initializer=initializer, 
                            padding=padding, 
                            name=None)
    max_pool_1 = nn.add_max_pool(tensor_in=conv_bn, kernel_shape=[1, 3, 3, 1], strides=[1, 1, 1, 1], pad=padding, name="max_pool_1")
    bottleneck = max_pool_1

    for i in range(bottleneck_depth):       
        kernel_filters = kernel_filters * 2 
        bottleneck = bottleneck_block(filters_out=kernel_filters, 
                                    tensor_in=bottleneck, 
                                    tensor_shortcut=bottleneck, 
                                    filters_in=None, 
                                    kernel_size=3, 
                                    strides=2, 
                                    initializer=initializer, 
                                    padding=padding, 
                                    use_gpu=use_gpu, 
                                    name="bottleneck_{}_1".format(int(i)+1))    
                                    
        bottleneck = bottleneck_block(filters_out=kernel_filters, 
                                    tensor_in=bottleneck, 
                                    tensor_shortcut=bottleneck, 
                                    filters_in=None, 
                                    kernel_size=3, 
                                    strides=1, 
                                    initializer=initializer, 
                                    padding=padding, 
                                    use_gpu=use_gpu, 
                                    name="bottleneck_{}_2".format(int(i)+1))
        '''
        bottleneck = bottleneck_block(filters_out=kernel_filters, 
                                    tensor_in=bottleneck, 
                                    tensor_shortcut=bottleneck, 
                                    filters_in=None, 
                                    kernel_size=3, 
                                    strides=1, 
                                    initializer=initializer, 
                                    padding=padding, 
                                    use_gpu=use_gpu, 
                                    name="bottleneck_{}_3".format(int(i)+1))
        '''
        
        
    keep_prob = tf_util_op.add_variable_hold()
    dropout_1 = nn.add_dropout(keep_prob, tensor_in=bottleneck, name="dropout_1")
    fc_1 = nn.add_fc(filters_out=output_labels, tensor_in=dropout_1, initializer=None, name="fc_1")
    softmax = nn.add_softmax(tensor_in=fc_1, name="softmax")
    
    return softmax, keep_prob, conv_bn, bottleneck
    
def bottleneck_block(filters_out, tensor_in, tensor_shortcut, filters_in=None, kernel_size=3, strides=1, initializer=None, padding='VALID', use_gpu=False, name=None):
    nn = NN_BUILDER(use_gpu)
    conv_bn = conv_bn_layer(filters_out, 
                            tensor_in, 
                            filters_in=filters_in, 
                            kernel_shape=[kernel_size, kernel_size], 
                            strides=[strides, strides], 
                            initializer=initializer, 
                            padding='SAME', 
                            name="{}_{}_1".format(name, "bottleneck"))
    conv_bn = conv_bn_layer(filters_out, 
                            conv_bn, 
                            filters_in=None, 
                            kernel_shape=[kernel_size, kernel_size], 
                            strides=[1, 1], 
                            initializer=initializer, 
                            padding='SAME', 
                            name="{}_{}_2".format(name, "bottleneck"))
    '''
    conv_bn = conv_bn_layer(filters_out, 
                            tensor_in, 
                            filters_in=filters_in, 
                            kernel_shape=[1, 1, 1, filters_out], 
                            strides=[1, 1, 1, 1], 
                            initializer=initializer, 
                            padding=padding, 
                            use_gpu=use_gpu, 
                            name="{}_{}_1".format(name, "bottleneck"))
    conv_bn = conv_bn_layer(filters_out, 
                            conv_bn, 
                            filters_in=None, 
                            kernel_shape=[kernel_size, kernel_size, 1, filters_out], 
                            strides=[1, strides, strides, 1], 
                            initializer=initializer, 
                            padding='SAME', 
                            use_gpu=use_gpu, 
                            name="{}_{}_2".format(name, "bottleneck"))
    conv_bn = conv_bn_layer(filters_out, 
                            conv_bn, 
                            filters_in=None, 
                            kernel_shape=[1, 1, 1, filters_out * 4], 
                            strides=[1, 1, 1, 1], 
                            initializer=initializer, 
                            padding=padding, 
                            use_gpu=use_gpu, 
                            name="{}_{}_3".format(name, "bottleneck"))
    '''
    if tensor_shortcut.get_shape()[-1] != filters_out:
        tensor_shortcut = nn.add_conv(filters_out=filters_out, 
                                        tensor_in=tensor_shortcut, 
                                        filters_in=filters_in, 
                                        kernel_shape=[1, 1, 1, filters_out], 
                                        strides=[1, strides, strides, 1], 
                                        initializer=initializer, 
                                        pad=padding, 
                                        name="{}_{}_shortcut".format(name, "bottleneck"))
    
    bottleneck_out = conv_bn + tensor_shortcut
    bottleneck_out = nn.add_relu(features=bottleneck_out)
    return bottleneck_out
    
 
def conv_bn_layer(filters_out, tensor_in, filters_in=None, kernel_shape=[1, 1], strides=[1, 1], initializer=None, padding='VALID', name=None, is_bn=True, is_conv=True, is_relu=True):
    '''
    nn = NN_BUILDER(use_gpu)
    
    if is_conv:
        tensor_in = nn.add_conv(filters_out=filters_out, 
                        tensor_in=tensor_in, 
                        filters_in=filters_in, 
                        kernel_shape=kernel_shape, 
                        strides=strides, 
                        initializer=initializer, 
                        pad=padding, 
                        name="{}_{}".format(name, "conv")
                        )
    
    if is_bn:
        tensor_in = nn.add_batch_norm(tensor_in=tensor_in, axes=[0, 1, 2], keep_dims=True, name="{}_{}".format(name, "batch_norm"))
        
    if is_relu:
        tensor_in = nn.add_relu(features=tensor_in, name="{}_{}".format(name, "relu"))
    return tensor_in
    '''
    
    if is_conv:
        tensor_in = Conv_Layer(filters_out, kernel_size=kernel_shape, strides=strides, padding=padding, name="{}_{}".format(name, 'conv'))(tensor_in)
    if is_bn:
        tensor_in = BN_Layer(name="{}_{}".format(name, 'batch_norm'))(tensor_in)
        #nn = NN_BUILDER(True)
        #tensor_in = nn.add_batch_norm(tensor_in=tensor_in, axes=[0, 1, 2], keep_dims=True, name="{}_{}".format(name, "batch_norm"))
    if is_relu:
        tensor_in = Activation_Layer('relu', name="{}_{}".format(name, 'relu'))(tensor_in)
    return tensor_in
    
