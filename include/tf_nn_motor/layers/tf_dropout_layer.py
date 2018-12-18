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

class Dropout_Layer:
    layer = None
    
    def __init__(self, rate, noise_shape=None, dtype=None, name=None, **kwargs):
        '''
        rate: float between 0 and 1. Fraction of the input units to drop.
noise_shape: 1D integer tensor representing the shape of the binary dropout mask that will be multiplied with the input. For instance, if your inputs have shape (batch_size, timesteps, features) and you want the dropout mask to be the same for all timesteps, you can use noise_shape=(batch_size, 1, features).
seed: A Python integer to use as random seed.
        '''
        kwargs['rate'] = rate
        kwargs['noise_shape'] = noise_shape
        kwargs['dtype'] = dtype
        kwargs['name'] = name
        
        self.layer = self.keras_layer(**kwargs)
    
    def __call__(self, tensor_in=None, **kwargs):
        return self.layer(tensor_in, **kwargs) if tensor_in is not None else self.layer
        
    def keras_layer(self, **kwargs):
        kwargs['dtype'] = kwargs['dtype'] if kwargs['dtype'] is not None else tf.float32
        
        
        layer = keras.layers.Dropout(**kwargs)
        return layer


