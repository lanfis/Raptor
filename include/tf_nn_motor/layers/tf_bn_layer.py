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

class BN_Layer:
    kwas = {}
    layer = None
    is_keras = False
    
    def __init__(self, axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True, beta_initializer=None, gamma_initializer=None, moving_mean_initializer=None, moving_variance_initializer=None, dtype=None, name=None, is_keras=False, **kwargs):
        '''
        axis: Integer, the axis that should be normalized (typically the features axis). For instance, after a Conv2D layer with data_format="channels_first", set axis=1 in BatchNormalization.
        momentum: Momentum for the moving average.
        epsilon: Small float added to variance to avoid dividing by zero.
        center: If True, add offset of beta to normalized tensor. If False, beta is ignored.
        scale: If True, multiply by gamma. If False, gamma is not used. When the next layer is linear (also e.g. nn.relu), this can be disabled since the scaling will be done by the next layer.
        beta_initializer: Initializer for the beta weight.
        gamma_initializer: Initializer for the gamma weight.
        moving_mean_initializer: Initializer for the moving mean.
        moving_variance_initializer: Initializer for the moving variance.
        beta_regularizer: Optional regularizer for the beta weight.
        gamma_regularizer: Optional regularizer for the gamma weight.
        beta_constraint: Optional constraint for the beta weight.
        gamma_constraint: Optional constraint for the gamma weight.
        renorm: Whether to use Batch Renormalization (https://arxiv.org/abs/1702.03275). This adds extra variables during training. The inference is the same for either value of this parameter.
        renorm_clipping: A dictionary that may map keys 'rmax', 'rmin', 'dmax' to scalar Tensors used to clip the renorm correction. The correction (r, d) is used as corrected_value = normalized_value * r + d, with r clipped to [rmin, rmax], and d to [-dmax, dmax]. Missing rmax, rmin, dmax are set to inf, 0, inf, respectively.
        renorm_momentum: Momentum used to update the moving means and standard deviations with renorm. Unlike momentum, this affects training and should be neither too small (which would add noise) nor too large (which would give stale estimates). Note that momentum is still applied to get the means and variances for inference.
        fused: if None or True, use a faster, fused implementation if possible. If False, use the system recommended implementation.
        trainable: Boolean, if True also add variables to the graph collection GraphKeys.TRAINABLE_VARIABLES (see tf.Variable).
        virtual_batch_size: An int. By default, virtual_batch_size is None, which means batch normalization is performed across the whole batch. When virtual_batch_size is not None, instead perform "Ghost Batch Normalization", which creates virtual sub-batches which are each normalized separately (with shared gamma, beta, and moving statistics). Must divide the actual batch size during execution.
        adjustment: A function taking the Tensor containing the (dynamic) shape of the input tensor and returning a pair (scale, bias) to apply to the normalized values (before gamma and beta), only during training. For example, if axis==-1, adjustment = lambda shape: ( tf.random_uniform(shape[-1:], 0.93, 1.07), tf.random_uniform(shape[-1:], -0.1, 0.1)) will scale the normalized value by up to 7% up or down, then shift the result by up to 0.1 (with independent scaling and bias for each feature but shared across all examples), and finally apply gamma and/or beta. If None, no adjustment is applied. Cannot be specified if virtual_batch_size is specified.
        '''
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
        
        self.is_keras = is_keras
        if self.is_keras:
            self.layer = self.keras_layer(**kwargs)
        else:
            self.kwas['name'] = kwargs['name']
    
    def __call__(self, tensor_in=None, **kwargs):
        for i in self.kwas:
            kwargs[i] = self.kwas[i]
        if self.is_keras:
            return self.layer(tensor_in, **kwargs) if tensor_in is not None else self.layer
        else:
            return self.nn_layer(tensor_in, **kwargs)
        
    def keras_layer(self, **kwargs):
        kwargs['beta_initializer'] = kwargs['beta_initializer'] if kwargs['beta_initializer'] is not None else 'zeros'
        kwargs['gamma_initializer'] = kwargs['gamma_initializer'] if kwargs['gamma_initializer'] is not None else 'ones'
        kwargs['moving_mean_initializer'] = kwargs['moving_mean_initializer'] if kwargs['moving_mean_initializer'] is not None else 'zeros'
        kwargs['moving_variance_initializer'] = kwargs['moving_variance_initializer'] if kwargs['moving_variance_initializer'] is not None else 'ones'
        kwargs['dtype'] = kwargs['dtype'] if kwargs['dtype'] is not None else tf.float32
        
        
        layer = keras.layers.BatchNormalization(**kwargs)
        return layer

    def nn_layer(self, tensor_in, axes=[0, 1, 2], keep_dims=True, name=None, **kwargs):
        tensor_mean, tensor_variance = self.add_moment(tensor_in, axes, keep_dims)        
        tensor_offset = self.variable_init('{}_offset'.format(name), shape=tensor_in.get_shape()[-1:], dtype=None, initializer=self.initializer_zero(), trainable=True)
        tensor_scale = self.variable_init('{}_scale'.format(name), shape=tensor_in.get_shape()[-1:], dtype=None, initializer=self.initializer_one(), trainable=True)
        tensor = tf.nn.batch_normalization(
                                            tensor_in,
                                            tensor_mean,
                                            tensor_variance,
                                            offset=tensor_offset,
                                            scale=tensor_scale,
                                            variance_epsilon=0.000001,
                                            name=None if name is None else name
                                            )
        return tensor
        
    def add_moment(self, tensor_in=None, axes=[0], keep_dims=False, name=None):
        mean, variance = tf.nn.moments(
                                        x=tensor_in if tensor_in is not None else self.tensor_cont,
                                        axes=axes,#[batch, height, width, depth], pass axes=[0, 1, 2].for simple batch normalization pass axes=[0] (batch only).
                                        shift=None,
                                        name=None if name is None else name,
                                        keep_dims=keep_dims
                                        )
        return mean, variance
        
    def variable_init(self, name, shape, dtype=None, initializer=None, trainable=True):
        dtype = tf.float32 if dtype is None else dtype
        initializer = self.initializer_rand_normal() if initializer is None else initializer
        variable = tf.get_variable(
                                name=name,
                                shape=shape,
                                dtype=dtype,
                                initializer=initializer,
                                regularizer=None,
                                trainable=trainable,
                                collections=None,
                                caching_device=None,
                                partitioner=None,
                                validate_shape=True,
                                use_resource=None,
                                custom_getter=None,
                                constraint=None
                                )
        return variable
        
    def initializer_global_variable(self):
        return tf.initializers.global_variables()

    def initializer_xavier(self, is_uniform=False, seed=None, dtype=None):#Whether to use uniform or normal distributed random initialization.
        initilaizer = tf.contrib.layers.xavier_initializer(is_uniform, seed, dtype=tf.float32 if dtype is None else dtype)
        return initilaizer

    def initializer_uniform_unit_scale(self, factor=1.0, seed=None, dtype=None):
        return tf.initializers.uniform_unit_scaling(factor, seed, dtype=tf.float32 if dtype is None else dtype)

    def initializer_constant(self, value=0.0, dtype=None):
        return tf.constant_initializer(value, dtype=tf.float32 if dtype is None else dtype)

    def initializer_rand_uniform(self, min_value=-1.0, max_value=1.0, seed=None, dtype=None):
        return tf.initializers.random_uniform(min_value, max_value, seed, dtype=tf.float32 if dtype is None else dtype)

    def initializer_truncated_normal(self, mean=0.0, std=1.0, seed=None, dtype=None):
        return tf.initializers.truncated_normal(mean, std, seed, dtype=tf.float32 if dtype is None else dtype)

    def initializer_rand_normal(self, mean=0.0, std=1.0, seed=None, dtype=None):
        return tf.initializers.random_normal(mean, std, seed, dtype=tf.float32 if dtype is None else dtype)
        
    def initializer_zero(self):
        return tf.zeros_initializer
        
    def initializer_one(self):
        return tf.ones_initializer
        
        
        
        
        
