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

class Dense_Layer:
    kwas = {}
    layer = None
    
    def __init__(self, unit_out, kernel_initializer=None, bias_initializer=None, dtype=None, name=None, **kwargs):
        '''
        units: Positive integer, dimensionality of the output space.
        activation: Activation function to use. If you don't specify anything, no activation is applied (ie. "linear" activation: a(x) = x).
        use_bias: Boolean, whether the layer uses a bias vector.
        kernel_initializer: Initializer for the kernel weights matrix.
        bias_initializer: Initializer for the bias vector.
        kernel_regularizer: Regularizer function applied to the kernel weights matrix.
        bias_regularizer: Regularizer function applied to the bias vector.
        activity_regularizer: Regularizer function applied to the output of the layer (its "activation")..
        kernel_constraint: Constraint function applied to the kernel weights matrix.
        bias_constraint: Constraint function applied to the bias vector.
        '''
        kwargs['units'] = unit_out
        kwargs['kernel_initializer'] = kernel_initializer
        kwargs['bias_initializer'] = bias_initializer
        kwargs['dtype'] = dtype
        kwargs['name'] = name
        
        self.layer = self.keras_layer(**kwargs)
    
    def __call__(self, tensor_in=None, **kwargs):
        return self.layer(tensor_in, **kwargs) if tensor_in is not None else self.layer
        
    def keras_layer(self, **kwargs):
        kwargs['kernel_initializer'] = kwargs['kernel_initializer'] if kwargs['kernel_initializer'] is not None else 'glorot_uniform'
        kwargs['bias_initializer'] = kwargs['bias_initializer'] if kwargs['bias_initializer'] is not None else 'zeros'
        kwargs['dtype'] = kwargs['dtype'] if kwargs['dtype'] is not None else tf.float32

        layer = keras.layers.Dense(**kwargs)
        return layer


