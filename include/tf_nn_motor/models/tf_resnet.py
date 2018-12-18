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

def resnet_builder(tensor_in, input_channels=1, output_labels=10, padding="SAME", kernel_size=3, strides=1, kernel_filters=64, bottleneck_depth=5, initializer=None, use_gpu=True, use_bn=True):   
    ConvLayer = []
    FPNLayer = []
    
    #tensor = Noise_Layer()(tensor_in)
    tensor = Padding_Layer(padding=[3, 3])(tensor_in)
    tensor = conv_bn_layer(filters_out=kernel_filters, 
                            tensor_in=tensor, 
                            kernel_shape=[kernel_size, kernel_size], 
                            strides=[strides, strides], 
                            initializer=initializer, 
                            padding=padding, 
                            is_bn=use_bn,
                            name="Conv_1")
    tensor = Pooling_Layer(pool_size=[3, 3], strides=[2, 2], type='max', padding='SAME')(tensor)
                            
    bottleneck = tensor
    ConvLayer.append(bottleneck)
    kernel_filters = kernel_filters * 2
    
    idx = 0
    for i in range(3):
        bottleneck = bottleneck_block(filters_out=kernel_filters, 
                                    tensor_in=bottleneck, 
                                    tensor_shortcut=bottleneck, 
                                    kernel_size=3, 
                                    strides=1,
                                    initializer=initializer, 
                                    padding=padding, 
                                    use_bn=use_bn,
                                    name="bottleneck_{}".format(int(idx)))  
        idx += 1
        kernel_filters = kernel_filters * 2
    ConvLayer.append(bottleneck)
    '''
    kernel_filters = kernel_filters * 2
    for i in range(4):
        bottleneck = bottleneck_block(filters_out=kernel_filters, 
                                    tensor_in=bottleneck, 
                                    tensor_shortcut=bottleneck, 
                                    kernel_size=3, 
                                    strides=1,
                                    initializer=initializer, 
                                    padding=padding, 
                                    use_bn=use_bn,
                                    name="bottleneck_{}".format(int(idx))) 
        idx += 1
    ConvLayer.append(bottleneck)
    '''
    '''
    kernel_filters = kernel_filters * 2
    bottleneck = bottleneck_block(filters_out=kernel_filters, 
                                    tensor_in=bottleneck, 
                                    tensor_shortcut=bottleneck, 
                                    kernel_size=3, 
                                    strides=1,
                                    initializer=initializer, 
                                    padding=padding, 
                                    use_bn=use_bn,
                                    name="bottleneck_{}".format(int(idx))) 
    idx += 1
    for i in range(bottleneck_depth):
        bottleneck = bottleneck_block(filters_out=kernel_filters, 
                                    tensor_in=bottleneck, 
                                    tensor_shortcut=bottleneck, 
                                    kernel_size=3, 
                                    strides=1,
                                    initializer=initializer, 
                                    padding=padding, 
                                    use_bn=use_bn,
                                    name="bottleneck_{}".format(int(idx))) 
        idx += 1
    ConvLayer.append(bottleneck)
    
    kernel_filters = kernel_filters * 2
    for i in range(3):
        bottleneck = bottleneck_block(filters_out=kernel_filters, 
                                    tensor_in=bottleneck, 
                                    tensor_shortcut=bottleneck, 
                                    kernel_size=3, 
                                    strides=1,
                                    initializer=initializer, 
                                    padding=padding, 
                                    use_bn=use_bn,
                                    name="bottleneck_{}".format(int(idx))) 
        idx += 1
    ConvLayer.append(bottleneck)
    '''
    for i in range(len(ConvLayer)):
        print(ConvLayer[i])
        
    keep_prob = tf_util_op.add_variable_hold()
    dropout_1 = Dropout_Layer(keep_prob, name="dropout_1")(bottleneck)
    dropout_1 = Flatten_Layer()(dropout_1)
    fc_1 = Dense_Layer(output_labels, name="fc_1")(dropout_1)
    softmax = Softmax_Layer(name="softmax")(fc_1)
    
    return softmax, keep_prob, tensor, bottleneck
    
def bottleneck_block(filters_out, tensor_in, tensor_shortcut, kernel_size=3, strides=1, initializer=None, padding='VALID', use_bn=True, name=None):
    conv_bn = conv_bn_layer(filters_out, 
                            tensor_in, 
                            kernel_shape=[1, 1], 
                            strides=[strides, strides], 
                            initializer=initializer, 
                            padding=padding, 
                            is_bn=use_bn,
                            name="{}_{}_1".format(name, "bottleneck"))
    conv_bn = conv_bn_layer(filters_out, 
                            conv_bn, 
                            kernel_shape=[kernel_size, kernel_size], 
                            strides=[1, 1], 
                            initializer=initializer, 
                            padding='SAME', 
                            is_bn=use_bn,
                            name="{}_{}_2".format(name, "bottleneck"))
    '''
    conv_bn = conv_bn_layer(filters_out * 4, 
                            conv_bn, 
                            kernel_shape=[1, 1], 
                            strides=[strides, strides], 
                            initializer=initializer, 
                            padding=padding, 
                            is_bn=use_bn,
                            name="{}_{}_3".format(name, "bottleneck"))
    '''
    if tensor_shortcut.get_shape()[-1] != filters_out:
        tensor_shortcut = conv_bn_layer(filters_out=filters_out, 
                                        tensor_in=tensor_shortcut, 
                                        kernel_shape=[1, 1], 
                                        strides=[strides, strides], 
                                        initializer=initializer, 
                                        padding=padding, 
                                        is_bn=use_bn,
                                        is_relu=False,
                                        name="{}_{}_shortcut".format(name, "bottleneck"))
    
    bottleneck_out = Add_Layer()([conv_bn, tensor_shortcut])
    bottleneck_out = Activation_Layer('relu')(bottleneck_out)
    return bottleneck_out
    
 
def conv_bn_layer(filters_out, tensor_in, filters_in=None, kernel_shape=[1, 1], strides=[1, 1], initializer=None, padding='VALID', name=None, is_bn=True, is_conv=True, is_relu=True):
    if is_conv:
        tensor_in = Conv_Layer(filters_out, kernel_size=kernel_shape, strides=strides, padding=padding, name="{}_{}".format(name, 'conv'))(tensor_in)
    if is_bn:
        tensor_in = BN_Layer(name="{}_{}".format(name, 'batch_norm'))(tensor_in)
    if is_relu:
        tensor_in = Activation_Layer('relu', name="{}_{}".format(name, 'relu'))(tensor_in)
        #tensor_in = Leaky_Relu_Layer(0.1, name="{}_{}".format(name, 'relu'))(tensor_in)
    return tensor_in
    
