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

class Reshape_Layer:
    kwas = {}
    layer = None
    
    def __init__(self, shape, name=None, **kwargs):
        '''
        inputs: input tensor(s).
        *args: additional positional arguments to be passed to self.call.
        **kwargs: additional keyword arguments to be passed to self.call.
        '''
        kwargs['target_shape'] = shape
        kwargs['name'] = name
        
        self.layer = self.keras_layer(**kwargs)
    
    def __call__(self, tensors_in=None, **kwargs):
        return self.layer(tensors_in, **kwargs) if tensors_in is not None else self.layer
        
    def keras_layer(self, **kwargs):        
        layer = keras.layers.Reshape(**kwargs)
        return layer


