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
from tensorflow import keras
from layers import *

#from StringIO import StringIO

tf.logging.set_verbosity(tf.logging.INFO)

class CONV_BN_Layer:
    kwas = {}
    layer = None
    
    
    def __init__(self, filters_out, kernel_size=[1, 1], strides=[1, 1], padding='SAME', data_format=None, kernel_initializer=None, bias_initializer=None,
                        axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True, beta_initializer=None, gamma_initializer=None, moving_mean_initializer=None, moving_variance_initializer=None,
                        is_bn=True, is_conv=True, is_relu=True, 
                        dtype=None, name=None, **kwargs):
        kwargs['filters_out'] = filters_out
        kwargs['kernel_size'] = kernel_size
        kwargs['strides'] = strides
        kwargs['padding'] = padding
        kwargs['data_format'] = data_format
        kwargs['kernel_initializer'] = kernel_initializer
        kwargs['bias_initializer'] = bias_initializer
        
        kwargs['axis'] = axis
        kwargs['momentum'] = momentum
        kwargs['epsilon'] = epsilon
        kwargs['center'] = center
        kwargs['scale'] = scale
        kwargs['beta_initializer'] = beta_initializer
        kwargs['gamma_initializer'] = gamma_initializer
        kwargs['moving_mean_initializer'] = moving_mean_initializer
        kwargs['moving_variance_initializer'] = moving_variance_initializer
        kwargs['dtype'] = dtype
        kwargs['name'] = name
        
        kwargs['is_bn'] = is_bn
        kwargs['is_conv'] = is_conv
        kwargs['is_relu'] = is_relu
        
        self.kwas = kwargs
    
    def __call__(self, tensor_in=None, **kwargs):
        tensor_in = tensor_in if tensor_in is not None else self.layer
        if self.kwas['is_conv']:
            tensor_in = Conv_Layer(filters_out=self.kwas['filters_out'], kernel_size=self.kwas['kernel_size'], strides=self.kwas['strides'], padding=self.kwas['padding'], name="{}_{}".format(self.kwas['name'], 'conv'))(tensor_in)
        if self.kwas['is_bn']:
            tensor_in = BN_Layer(name="{}_{}".format(self.kwas['name'], 'batch_norm'))(tensor_in)
        if self.kwas['is_relu']:
            tensor_in = Activation_Layer('relu', name="{}_{}".format(self.kwas['name'], 'relu'))(tensor_in)
        return tensor_in
        