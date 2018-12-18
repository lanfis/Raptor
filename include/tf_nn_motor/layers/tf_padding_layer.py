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

class Padding_Layer:
    kwas = {}
    
    def __init__(self, padding=[1, 1], data_format=None, dtype=None, name=None, **kwargs):
        '''
        padding: int, or tuple of 2 ints, or tuple of 2 tuples of 2 ints. - If int: the same symmetric padding is applied to height and width. - If tuple of 2 ints: interpreted as two different symmetric padding values for height and width: (symmetric_height_pad, symmetric_width_pad). - If tuple of 2 tuples of 2 ints: interpreted as ((top_pad, bottom_pad), (left_pad, right_pad))
        inputs: input tensor(s).
        *args: additional positional arguments to be passed to self.call.
        **kwargs: additional keyword arguments to be passed to self.call.
        '''
        kwargs['padding'] = padding
        kwargs['data_format'] = data_format
        kwargs['dtype'] = dtype
        kwargs['name'] = name
        
        self.layer = self.keras_layer(**kwargs)
    
    def __call__(self, tensor_in=None, **kwargs):
        return self.layer(tensor_in, **kwargs) if tensor_in is not None else self.layer
        
    def keras_layer(self, **kwargs):
        kwargs['dtype'] = kwargs['dtype'] if kwargs['dtype'] is not None else tf.float32
        
        if len(kwargs['padding']) == 1:
            layer = keras.layers.ZeroPadding1D(**kwargs)
        elif len(kwargs['padding']) == 2:
            layer = keras.layers.ZeroPadding2D(**kwargs)
        elif len(kwargs['padding']) == 3:
            layer = keras.layers.ZeroPadding3D(**kwargs)
        else:
            print("-- Padding layer error ! padding size : {}".format(kwargs['padding']))
            layer = None
        return layer


