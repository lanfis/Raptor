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

class Pooling_Layer:
    kwas = {}
    layer = None
    
    def __init__(self, pool_size=[1, 1], strides=[1, 1], padding='SAME', type='max', data_format=None, dtype=None, name=None, **kwargs):
        '''
        pool_size: integer or tuple of 2 integers, factors by which to downscale (vertical, horizontal). (2, 2) will halve the input in both spatial dimension. If only one integer is specified, the same window length will be used for both dimensions.
        strides: Integer, tuple of 2 integers, or None. Strides values. If None, it will default to pool_size.
        padding: One of "valid" or "same" (case-insensitive).
        data_format: A string, one of channels_last (default) or channels_first. The ordering of the dimensions in the inputs. channels_last corresponds to inputs with shape (batch, height, width, channels) while channels_first corresponds to inputs with shape (batch, channels, height, width). It defaults to the image_data_format value found in your Keras config file at ~/.keras/keras.json. If you never set it, then it will be "channels_last".
        '''
        kwargs['pool_size'] = pool_size
        kwargs['strides'] = strides
        kwargs['padding'] = padding
        kwargs['data_format'] = data_format
        kwargs['dtype'] = dtype
        kwargs['name'] = name
        
        if type == 'avg':
            self.layer = self.keras_layer_avg(**kwargs)
        else:
            self.layer = self.keras_layer_max(**kwargs)
    
    def __call__(self, tensor_in=None, **kwargs):
        return self.layer(tensor_in, **kwargs) if tensor_in is not None else self.layer
        
    def keras_layer_max(self, **kwargs):
        kwargs['dtype'] = kwargs['dtype'] if kwargs['dtype'] is not None else tf.float32
        
        if len(kwargs['pool_size']) == 1:
            layer = keras.layers.MaxPool1D(**kwargs)
        if len(kwargs['pool_size']) == 2:
            layer = keras.layers.MaxPool2D(**kwargs)
        elif len(kwargs['pool_size']) == 3:
            layer = keras.layers.MaxPool3D(**kwargs)
        else:
            print("-- Conv layer error ! kernel size : {} / strides : {}".format(init_kwargs['pool_size'], init_kwargs['strides']))
            layer = None
        return layer
        
    def keras_layer_avg(self, **kwargs):
        kwargs['dtype'] = kwargs['dtype'] if kwargs['dtype'] is not None else tf.float32
        
        if len(kwargs['pool_size']) == 1:
            layer = keras.layers.AvgPool1D(**kwargs)
        if len(kwargs['pool_size']) == 2:
            layer = keras.layers.AvgPool2D(**kwargs)
        elif len(kwargs['pool_size']) == 3:
            layer = keras.layers.AvgPool3D(**kwargs)
        else:
            print("-- Conv layer error ! kernel size : {} / strides : {}".format(init_kwargs['pool_size'], init_kwargs['strides']))
            layer = None
        return layer


