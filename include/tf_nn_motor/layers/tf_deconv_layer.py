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

#from StringIO import StringIO

tf.logging.set_verbosity(tf.logging.INFO)

class Deconv_Layer:
    kwas = {}
    layer = None
    
    def __init__(self, filters_out, kernel_size=[1, 1], strides=[1, 1], padding='SAME', data_format=None, kernel_initializer=None, bias_initializer=None, dtype=None, name=None, **kwargs):
        '''        
        filters: Integer, the dimensionality of the output space (i.e. the number of output filters in the convolution).
        kernel_size: An integer or tuple/list of 2 integers, specifying the height and width of the 2D convolution window. Can be a single integer to specify the same value for all spatial dimensions.
        strides: An integer or tuple/list of 2 integers, specifying the strides of the convolution along the height and width. Can be a single integer to specify the same value for all spatial dimensions. Specifying any stride value != 1 is incompatible with specifying any dilation_rate value != 1.
        padding: one of "valid" or "same" (case-insensitive).
        data_format: A string, one of channels_last (default) or channels_first. The ordering of the dimensions in the inputs. channels_last corresponds to inputs with shape (batch, height, width, channels) while channels_first corresponds to inputs with shape (batch, channels, height, width). It defaults to the image_data_format value found in your Keras config file at ~/.keras/keras.json. If you never set it, then it will be "channels_last".
        dilation_rate: an integer or tuple/list of 2 integers, specifying the dilation rate to use for dilated convolution. Can be a single integer to specify the same value for all spatial dimensions. Currently, specifying any dilation_rate value != 1 is incompatible with specifying any stride value != 1.
        activation: Activation function to use. If you don't specify anything, no activation is applied (ie. "linear" activation: a(x) = x).
        use_bias: Boolean, whether the layer uses a bias vector.
        kernel_initializer: Initializer for the kernel weights matrix.
        bias_initializer: Initializer for the bias vector.
        kernel_regularizer: Regularizer function applied to the kernel weights matrix.
        bias_regularizer: Regularizer function applied to the bias vector.
        activity_regularizer: Regularizer function applied to the output of the layer (its "activation")..
        kernel_constraint: Constraint function applied to the kernel matrix.
        bias_constraint: Constraint function applied to the bias vector.
        '''
        kwargs['filters_out'] = filters_out
        kwargs['kernel_size'] = kernel_size
        kwargs['strides'] = strides
        kwargs['padding'] = padding
        kwargs['data_format'] = data_format
        kwargs['kernel_initializer'] = kernel_initializer
        kwargs['bias_initializer'] = bias_initializer
        kwargs['dtype'] = dtype
        kwargs['name'] = name
        
        self.layer = self.keras_layer(**kwargs)
    
    def __call__(self, tensor_in=None, **kwargs):
        return self.layer(tensor_in, **kwargs) if tensor_in is not None else self.layer
        
    def keras_layer(self, **kwargs):
        kwargs['filters'] = kwargs['filters_out']
        del kwargs['filters_out']
        kwargs['kernel_initializer'] = kwargs['kernel_initializer'] if kwargs['kernel_initializer'] is not None else 'glorot_uniform'
        kwargs['bias_initializer'] = kwargs['bias_initializer'] if kwargs['bias_initializer'] is not None else 'zeros'
        kwargs['dtype'] = kwargs['dtype'] if kwargs['dtype'] is not None else tf.float32
        
        if len(kwargs['kernel_size']) == 2:
            layer = keras.layers.Conv2DTranspose(**kwargs)
        elif len(kwargs['kernel_size']) == 3:
            layer = keras.layers.Conv3DTranspose(**kwargs)
        else:
            print("-- Conv layer error ! kernel size : {} / strides : {}".format(kwargs['kernel_size'], kwargs['strides']))
            layer = None
        return layer


