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

class Leaky_Relu_Layer:
    layer = None
    
    def __init__(self, alpha=0.3, dtype=None, name=None, **kwargs):
        '''
        alpha: float >= 0. Negative slope coefficient.
        inputs: input tensor(s).
        *args: additional positional arguments to be passed to self.call.
        **kwargs: additional keyword arguments to be passed to self.call.
        '''
        kwargs['alpha'] = alpha
        kwargs['dtype'] = dtype
        kwargs['name'] = name
        
        self.layer = self.keras_layer(**kwargs)
    
    def __call__(self, tensor_in=None, **kwargs):
        return self.layer(tensor_in, **kwargs) if tensor_in is not None else self.layer
        
    def keras_layer(self, **kwargs):
        kwargs['dtype'] = kwargs['dtype'] if kwargs['dtype'] is not None else tf.float32
        
        layer = keras.layers.LeakyReLU(**kwargs)
        return layer


