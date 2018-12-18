#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import numpy as np
import tensorflow as tf

    
def accuracy(tensor_results, tensor_labels, name=None):
    correct_tensor = tensor_cast(tf.equal(tensor_results, tensor_labels, name), tf.float32)
    accuracy = tensor_reducemean(correct_tensor)
    return accuracy

def loss(tensor_labels=None, tensor_logits=None, dim=-1, name=None):
    return tensor_reducemean(softmax_cross_entropy_tensor(tensor_labels=tensor_labels, tensor_logits=tensor_logits, dim=dim, name=name))
        
def softmax_cross_entropy_tensor(tensor_labels=None, tensor_logits=None, dim=-1, name=None):
    return tf.nn.softmax_cross_entropy_with_logits(
                                                    labels=tensor_labels,
                                                    logits=tensor_logits,
                                                    dim=dim,
                                                    name=name
                                                    )
    
def tensor_reducemean(tensor, axis=None, keep_dims=False, reduction_indices=None, name=None):
    return tf.reduce_mean(
                        input_tensor=tensor,
                        axis=axis,#The dimensions to reduce. If None (the default), reduces all dimensions. Must be in the range [-rank(input_tensor), rank(input_tensor)).
                        keepdims=keep_dims,#If true, retains reduced dimensions with length 1
                        name=name,
                        reduction_indices=reduction_indices#The old (deprecated) name for axis.
                        )
                            
def tensor_equal(tensor_x, tensor_y, name=None):
    return tf.equal(tensor_x, tensor_y, name=name)
        
def tensor_cast(tensor, dtype=None, name=None):
    dtype = tf.float32 if dtype is None else dtype
    return tf.cast(tensor, dtype, name)
        
def tensor_argmax(tensor_in, dim=1, dtype=None, name=None):
    dtype = tf.int64 if dtype is None else dtype 
    return tf.arg_max(input=tensor_in, dimension=dim, output_type=dtype, name=None)
        
def tensor_shape(tensor):
    return tf.shape(tensor)
    
def tensor_reshape(tensor, shape):
    return tf.reshape(tensor, shape)
        
def tensor_reshape(tnesor_in, shape, name=None):
    return tf.reshape(tensor_in, shape, name)
    
def tensor_expand_dim(tensor, axis, name=None):
    return tf.expand_dims(tensor, axis, name)

def add_variable_hold(shape=None, dtype=None, name=None):
    dtype = tf.float32 if dtype is None else dtype
    return tf.placeholder(dtype, shape, name)
    
def add_ones(shape, dtype=None, name=None):
    dtype = tf.float32 if dtype is None else dtype
    return tf.ones(shape, dtype, name)
    
def convert_to_tensor(value, dtype=None, name=None):
    dtype = tf.float32 if dtype is None else dtype 
    return tf.convert_to_tensor(value, dtype=None, name=None, preferred_dtype=None)
        
def tensor_index(tensor, index, name=None):
    return tf.gather_nd(tensor, index, name)
    
def tensor_add(tensor_1, tensor_2, name=None):
    return tf.add(tensor_1, tensor_2, name)
    
def tensor_subtract(tensor_1, tensor_2, name=None):
    return tf.subtract(tensor_1, tensor_2, name)
        
def tensor_multiply(tensor_1, tensor_2, name=None):
    return tf.multiply(tensor_1, tensor_2, name)
    
def tensor_divide(tensor_1, tensor_2, name=None):
    return tf.divide(tensor_1, tensor_2, name)

def tensor_abs(tensor, name=None):
    return tf.abs(tensor, name)
    
def tensor_squre(tensor, name=None):
    return tf.squre(tensor, name)
    
def tensor_less(x, y, name=None):
    return tf.math.less(x, y, name)
    
def tensor_sqrt(tensor, name=None):
    return tf.sqrt(tensor, name)
