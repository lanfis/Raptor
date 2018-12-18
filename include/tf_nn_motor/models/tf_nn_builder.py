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
import time
import math
import ops.tf_util_ops as tf_util_ops

#from StringIO import StringIO

tf.logging.set_verbosity(tf.logging.INFO)

class NN_BUILDER:
    #PUBLIC
    data_format = "NHWC"#"NHWC", "NCHW". Defaults to "NHWC"
    use_cudnn   = False
    #batch_size  = 128

    prefix_var   = ""
    postfix_var  = ""
    prefix_conv  = ""
    postfix_conv = ""
    prefix_deconv  = ""
    postfix_deconv = ""
    prefix_softmax  = ""
    postfix_softmax = ""
    prefix_relu  = ""
    postfix_relu = ""
    prefix_max_pool = ""
    postfix_max_pool = ""
    prefix_avg_pool = ""
    postfix_avg_pool = ""
    prefix_fc = ""
    postfix_fc = ""
    prefix_dropout = ""
    postfix_dropout = ""
    prefix_softmax_cross_entropy = ""
    postfix_softmax_cross_entropy = ""
    prefix_batch_norm = ""
    postfix_batch_norm = ""
    
    prefix_weight = ""
    postfix_weight = "_weight"
    prefix_bias = ""
    postfix_bias = "_bias"

    tensor_cont  = None
        
    #PRIVATE
    

    def __init__(self, use_gpu=False):
        self.use_cudnn = use_gpu

    def add_conv(self, filters_out=None, tensor_in=None, filters_in=None, kernel_shape=[1, 1, 1, 1], strides=[1, 1, 1, 1], pad="SAME", dtype=None, initializer=None, name=None):
        '''
        tensor_in = [batch, //indepth, in_height, in_width, in_channels]  
        kernel_shape = [//filter_depth, filter_height, filter_width, in_channels, out_channels]
        strides[0] = strides[4] = 1
        '''
        tensor_in = tensor_in if tensor_in is not None else self.tensor_cont
        kernel_shape[-2] = filters_in if filters_in is not None else tensor_in.get_shape()[-1] 
        kernel_shape[-1] = filters_out if filters_out is not None else tensor_in.get_shape()[-1] 
        strides[0] = strides[-1] = 1
        with tf.variable_scope("conv" if name is None else self.prefix_conv+name+self.postfix_conv):
            kernel = self.variable_init(
                                        name="conv" if name is None else self.prefix_var+name+self.postfix_var, 
                                        shape=kernel_shape, 
                                        dtype=dtype if dtype is not None else tf.float32,
                                        initializer=self.initializer_xavier() if initializer is None else initializer,
                                        trainable=True
                                        )
            if len(kernel_shape) == 5:
                tensor_out = tf.nn.conv3d(
                                          input=tensor_in if tensor_in is not None else self.tensor_cont,
                                          filter=kernel,
                                          strides=strides,
                                          padding=pad,#"SAME" or "VALID"
                                          use_cudnn_on_gpu=self.use_cudnn,
                                          data_format=self.data_format,
                                          name=None if name is None else self.prefix_conv+name+self.postfix_conv
                                          )
            elif len(kernel_shape) == 3:
                tensor_out = tf.nn.conv1d(
                                          input=tensor_in if tensor_in is not None else self.tensor_cont,
                                          filter=kernel,
                                          strides=strides,
                                          padding=pad,#"SAME" or "VALID"
                                          use_cudnn_on_gpu=self.use_cudnn,
                                          data_format=self.data_format,
                                          name=None if name is None else self.prefix_conv+name+self.postfix_conv
                                          )
            else:
                tensor_out = tf.nn.conv2d(
                                          input=tensor_in if tensor_in is not None else self.tensor_cont,
                                          filter=kernel,
                                          strides=strides,
                                          padding=pad,#"SAME" or "VALID"
                                          use_cudnn_on_gpu=self.use_cudnn,
                                          data_format=self.data_format,
                                          name=None if name is None else self.prefix_conv+name+self.postfix_conv
                                          )
            self.tensor_cont  = tensor_out
            return tensor_out
            
    def add_deconv(self, filters_out=None, tensor_in=None, filters_in=None, kernel=None, kernel_in_shape=[1, 1, 1, 1], tensor_out_shape=[-1, -1, -1, -1], strides=[-1, -1, -1, -1], pad="SAME", data_format='NHWC', dtype=None, initializer=None, name=None):
        '''
        value: A 5-D Tensor of type float and shape [batch, //depth, height, width, in_channels].
        filter: A 5-D Tensor with the same type as value and shape [//depth, height, width, output_channels, in_channels]. filter's in_channels dimension must match that of value.
        output_shape: A 1-D Tensor representing the output shape of the deconvolution op.[NHWC]
        strides: A list of ints. The stride of the sliding window for each dimension of the input tensor.
        padding: A string, either 'VALID' or 'SAME'. The padding algorithm. See the comment here
        data_format: A string, either 'NDHWC' or 'NCDHW' specifying the layout of the input and output tensors. Defaults to 'NDHWC'.
        name: Optional name for the returned tensor.
        '''
        #kernel_in_shape : kernel shape, will be disable if kernel is not None
        #Be aware of reversing conv layer size should be possible to count out from normal conv layer size
        
        
        tensor_in = tensor_in if tensor_in is not None else self.tensor_cont
        if kernel is not None:
            kernel_in_shape = []
            for i in range(len(kernel.get_shape())):
                kernel_in_shape.append(kernel.get_shape()[int(i)])
        else:
            kernel_in_shape[-1] = filters_in if filters_in is not None else tensor_in.get_shape()[-1] 
            kernel_in_shape[-2] = filters_out if filters_out is not None else tensor_in.get_shape()[-1]
        
        tensor_out_shape[0] = tensor_out_shape[0] if tensor_out_shape[0] != -1 else tensor_in.get_shape()[0]
        tensor_out_shape[-1] = tensor_out_shape[-1] if tensor_out_shape[-1] != -1 else int(tensor_in.get_shape()[-1])
        tensor_out_shape[-2] = tensor_out_shape[-2] if tensor_out_shape[-2] != -1 else int(tensor_in.get_shape()[-2]) * kernel_in_shape[-3]
        tensor_out_shape[-3] = tensor_out_shape[-3] if tensor_out_shape[-3] != -1 else int(tensor_in.get_shape()[-3]) * kernel_in_shape[-4]
        
        strides[1] = strides[1] if strides[1] != -1 else kernel_in_shape[-4]
        strides[2] = strides[2] if strides[2] != -1 else kernel_in_shape[-3]
        strides[0] = strides[-1] = 1
        
        with tf.variable_scope("deconv" if name is None else self.prefix_deconv+name+self.postfix_deconv):
            kernel = kernel if kernel is not None else self.variable_init(
                                                name="deconv" if name is None else self.prefix_var+name+self.postfix_var, 
                                                shape=kernel_in_shape, 
                                                dtype=dtype if dtype is not None else tf.float32,
                                                initializer=self.initializer_xavier() if initializer is None else initializer,
                                                trainable=True
                                                )
            if len(tensor_in.shape) == 5:
                tf.nn.conv3d_transpose(
                                        value=tensor_in,
                                        filter=kernel,
                                        output_shape=tensor_out_shape,
                                        strides=strides,
                                        padding=pad,
                                        data_format=data_format,
                                        name=None
                                        )

            else:
                tensor_out = tf.nn.conv2d_transpose(
                                        value=tensor_in,
                                        filter=kernel,
                                        output_shape=tensor_out_shape,
                                        strides=strides,
                                        padding=pad,
                                        data_format=data_format,
                                        name=None
                                        )

            self.tensor_cont  = tensor_out
            return tensor_out
            
    def add_dropout(self, keep_prob, tensor_in=None, noise_shape=None, seed=None, name=None):
        self.tensor_cont = tf.nn.dropout(
                                        x=tensor_in if tensor_in is not None else self.tensor_cont,
                                        keep_prob=keep_prob,
                                        noise_shape=noise_shape,
                                        seed=seed,
                                        name=None if name is None else self.prefix_dropout+name+self.postfix_dropout
                                        )
        return self.tensor_cont
        
    def add_fc(self, filters_out, tensor_in=None, initializer=None, name=None):
        tensor_in = tensor_in if tensor_in is not None else self.tensor_cont 
        unit_size = 1
        for i in range(1, len(tensor_in.get_shape())):
            unit_size *= int(tensor_in.get_shape()[i])
        x = tf.reshape(
                       tensor_in, 
                       [-1, unit_size]
                      )
        initializer_weight = self.initializer_xavier(is_uniform=True) if initializer is None else initializer
        weight = self.variable_init(
                                    self.prefix_weight+"fc"+self.postfix_weight if name is None else self.prefix_weight+name+self.postfix_weight, 
                                    [x.get_shape()[1], filters_out], 
                                    initializer=initializer_weight
                                    )
        initializer_bias = self.initializer_constant()
        bias = self.variable_init(
                                  self.prefix_bias+"fc"+self.postfix_bias if name is None else self.prefix_bias+name+self.postfix_bias, 
                                  [filters_out], 
                                  initializer=initializer_bias
                                  )
        self.tensor_cont = tf.nn.xw_plus_b(x, weight, biases=bias, name=None if name is None else self.prefix_fc+name+self.postfix_fc)
        return self.tensor_cont
    
    def add_softmax(self, tensor_in=None, dim=-1, name=None):
        self.tensor_cont = tf.nn.softmax(
                                        logits=tensor_in if tensor_in is not None else self.tensor_cont, 
                                        dim=dim,
                                        name=None if name is None else self.prefix_softmax+name+self.postfix_softmax
                                        )
        return self.tensor_cont

    def add_relu(self, features=None, name=None):
        self.tensor_cont = tf.nn.relu(features if features is not None else self.tensor_cont, None if name is None else self.prefix_relu+name+self.postfix_relu)
        return self.tensor_cont

    def add_max_pool(self, tensor_in=None, kernel_shape=[1, 2, 2, 1], strides=[1, 1, 1, 1], pad="SAME", name=None):
        '''
        tensor_in = [batch, //depth, rows, cols, channels]
        ksize[0] = ksize[4] = 1
        strides[0] = strides[4] = 1
        '''
        kernel_shape[0] = kernel_shape[-1] = 1
        strides[0] = strides[-1] = 1
        if len(kernel_shape) == 5:
            tensor_out = tf.nn.max_pool3d(
                                        value=tensor_in if tensor_in is not None else self.tensor_cont,
                                        ksize=kernel_shape, 
                                        strides=strides, 
                                        padding=pad, 
                                        data_format=self.data_format, 
                                        name=None if name is None else self.prefix_max_pool+name+self.postfix_max_pool
                                        )
        else:
            tensor_out = tf.nn.max_pool(
                                        value=tensor_in if tensor_in is not None else self.tensor_cont,
                                        ksize=kernel_shape, 
                                        strides=strides, 
                                        padding=pad, 
                                        data_format=self.data_format, 
                                        name=None if name is None else self.prefix_max_pool+name+self.postfix_max_pool
                                        )
        self.tensor_cont = tensor_out
        return tensor_out
        
        
    def add_avg_pool(self, tensor_in=None, kernel_shape=[1, 2, 2, 1], strides=[1, 1, 1, 1], pad="SAME", name=None):
        '''

        tensor_in = [batch, //depth, rows, cols, channels]

        ksize[0] = ksize[4] = 1

        strides[0] = strides[4] = 1

        '''
        kernel_shape[0] = kernel_shape[-1] = 1
        strides[0] = strides[-1] = 1
        if len(kernel_shape) == 5:
            tensor_out = tf.nn.avg_pool3d(
                                        value=tensor_in if tensor_in is not None else self.tensor_cont,
                                        ksize=kernel_shape, 
                                        strides=strides, 
                                        padding=pad, 
                                        data_format=self.data_format, 
                                        name=None if name is None else self.prefix_avg_pool+name+self.postfix_avg_pool
                                        )
        else:
            tensor_out = tf.nn.avg_pool(
                                        value=tensor_in if tensor_in is not None else self.tensor_cont,
                                        ksize=kernel_shape, 
                                        strides=strides, 
                                        padding=pad, 
                                        data_format=self.data_format, 
                                        name=None if name is None else self.prefix_avg_pool+name+self.postfix_avg_pool
                                        )
                                
        self.tensor_cont = tensor_out
        return tensor_out
        
    def add_resize(self, tensor_in, height, width, method=None, align_corners=False):
        '''
        images: 4-D Tensor of shape [batch, height, width, channels] or 3-D Tensor of shape [height, width, channels].
        size: A 1-D int32 Tensor of 2 elements: new_height, new_width. The new size for the images.
        method: ResizeMethod. Defaults to ResizeMethod.BILINEAR.
            ResizeMethod.BILINEAR: Bilinear interpolation.
            ResizeMethod.NEAREST_NEIGHBOR: Nearest neighbor interpolation.
            ResizeMethod.BICUBIC: Bicubic interpolation.
            ResizeMethod.AREA: Area interpolation.
        align_corners: bool. If True, the centers of the 4 corner pixels of the input and output tensors are aligned, preserving the values at the corner pixels. Defaults to False.
        '''
        method = method if method is not None else tf.image.ResizeMethod.BILINEAR
        return tf.image.resize_images(
                                        tensor_in,
                                        size=(height, width),
                                        method=method,
                                        align_corners=align_corners
                                        )

    def add_resize_multiply(self, tensor_in, height_multiply=1, width_multiply=1, method=None, align_corners=False):
        '''
        images: 4-D Tensor of shape [batch, height, width, channels] or 3-D Tensor of shape [height, width, channels].
        size: A 1-D int32 Tensor of 2 elements: new_height, new_width. The new size for the images.
        method: ResizeMethod. Defaults to ResizeMethod.BILINEAR.
            ResizeMethod.BILINEAR: Bilinear interpolation.
            ResizeMethod.NEAREST_NEIGHBOR: Nearest neighbor interpolation.
            ResizeMethod.BICUBIC: Bicubic interpolation.
            ResizeMethod.AREA: Area interpolation.
        align_corners: bool. If True, the centers of the 4 corner pixels of the input and output tensors are aligned, preserving the values at the corner pixels. Defaults to False.
        '''
        method = method if method is not None else tf.image.ResizeMethod.BILINEAR
        height = int(tensor_in.get_shape()[-3]) * height_multiply
        width = int(tensor_in.get_shape()[-2]) * width_multiply
        return tf.image.resize_images(
                                        tensor_in,
                                        size=(height, width),
                                        method=method,
                                        align_corners=align_corners
                                        )
    '''
    def add_resize_multiply(self, tensor_in, height_multiply=1, width_multiply=1):
        height = int(tensor_in.get_shape()[-3]) * height_multiply
        width = int(tensor_in.get_shape()[-2]) * width_multiply
        return tf.image.resize_image_with_crop_or_pad(tensor_in, height, width)
    '''
        
    def add_spatial_pyramid_pool(self, tensor_in=None, pyramid_kernel_shape=[3, 4, 5], strides=[-1, -1, -1], pad="SAME"):
        '''
        pyramid_kernel_shape : 3  
        strides : 3 #-1 as a default value to set to euqal to pyramid_kernel_shape size
        pyramid_kernel_shape : 4  
        strides : 4 #-1 as a default value to set to euqal to pyramid_kernel_shape size
        pyramid_kernel_shape : 5  
        strides : 5 #-1 as a default value to set to euqal to pyramid_kernel_shape size
        '''
        tensor_in = tensor_in if tensor_in is not None else self.tensor_cont
        if len(tensor_in.get_shape()) == 5:
            tensor_batch = tensor_in.get_shape()[0]
            tensor_depth = tensor_in.get_shape()[1]
            tensor_height = tensor_in.get_shape()[2]
            tensor_width = tensor_in.get_shape()[3]
            tensor_channel = tensor_in.get_shape()[4]
            shape_size = tensor_depth * tensor_height * tensor_width * tensor_channel
        else:
            tensor_batch = tensor_in.get_shape()[0]
            tensor_height = tensor_in.get_shape()[1]
            tensor_width = tensor_in.get_shape()[2]
            tensor_channel = tensor_in.get_shape()[3]
            shape_size = tensor_height * tensor_width * tensor_channel
        
        spp = []
        for i in range(len(pyramid_kernel_shape)):
            kernel_shape_size = pyramid_kernel_shape[int(i)]
            stride_size = strides[int(i)] if strides[int(i)] > -1 else kernel_shape_size
            
            height_stride_need_count = math.ceil(float(int(tensor_height)) - float(kernel_shape_size)) / float(stride_size)
            width_stride_need_count  = math.ceil(float(int(tensor_width))  - float(kernel_shape_size)) / float(stride_size)
            height_suit_size = height_stride_need_count * stride_size + kernel_shape_size
            width_suit_size  = width_stride_need_count  * stride_size + kernel_shape_size
            height_need_pad = int(height_suit_size - int(tensor_height))
            width_need_pad  = int(width_suit_size  - int(tensor_width))
            
            h_l = int(height_need_pad / 2)
            h_r = int(height_need_pad / 2) if int(height_need_pad) % 2 == 0 else int(height_need_pad / 2) + 1
            w_l = int(width_need_pad  / 2)
            w_r = int(width_need_pad  / 2) if int(width_need_pad)  % 2 == 0 else int(width_need_pad  / 2) + 1
            
            if len(tensor_in.get_shape()) == 5:
                pad_size = tf.constant([[0, 0], [0, 0], [h_l, h_r], [w_l, w_r], [0, 0]])
            else:
                pad_size = tf.constant([[0, 0], [h_l, h_r], [w_l, w_r], [0, 0]])
            tensor_padded = self.add_pad(pad_size, tensor_in, mode='CONSTANT', name=None, constant_values=0.0)
            tensor_pool = self.add_avg_pool(tensor_padded,
                                     kernel_shape=[1, kernel_shape_size, kernel_shape_size, 1],
                                     strides=[1, stride_size, stride_size, 1], 
                                     pad=pad)
            #spp.append(tf.reshape(tensor_pool, [-1, shape_size]))
            
            if i == 0:
                spp = tf.reshape(tensor_pool, [-1, shape_size])
            else:
                spp = self.add_concat([spp, tf.reshape(tensor_pool, [-1, shape_size])], axis=1)
            
        #if len(pyramid_kernel_shape) > 1:
            #spp = self.add_concat(spp, axis=0)
        
        self.tensor_cont = spp
        return self.tensor_cont
        #return tensor_pool
            
    
    def add_batch_norm(self, tensor_in=None, axes=[0, 1, 2], keep_dims=True, name=None, is_train=False):
        tensor_in = tensor_in if tensor_in is not None else self.tensor_cont
        tensor_mean, tensor_variance = self.add_moment(tensor_in, axes, keep_dims)
        if is_train:
            tensor_mean_scale = self.variable_init('{}_mean_scale'.format(name), shape=tensor_in.get_shape()[-1:], dtype=None, initializer=self.initializer_one(), trainable=True)        
            #tensor_mean_offset = self.variable_init('{}_mean_offset'.format(name), shape=tensor_in.get_shape()[-1:], dtype=None, initializer=self.initializer_zero(), trainable=True)
            tensor_variance_scale = self.variable_init('{}_variance_scale'.format(name), shape=tensor_in.get_shape()[-1:], dtype=None, initializer=self.initializer_one(), trainable=True)
            #tensor_variance_offset = self.variable_init('{}_variance_offset'.format(name), shape=tensor_in.get_shape()[-1:], dtype=None, initializer=self.initializer_zero(), trainable=True)
        
            tensor_mean = tf_util_ops.tensor_multiply(tensor_mean, tensor_mean_scale)
            #tensor_mean = tf_util_ops.tensor_add(tensor_mean, tensor_mean_offset)
            tensor_variance = tf_util_ops.tensor_multiply(tensor_variance, tensor_variance_scale)
            #tensor_variance = tf_util_ops.tensor_add(tensor_variance, tensor_variance_offset)
        
        tensor_offset = self.variable_init('{}_offset'.format(name), shape=tensor_in.get_shape()[-1:], dtype=None, initializer=self.initializer_zero(), trainable=True)
        tensor_scale = self.variable_init('{}_scale'.format(name), shape=tensor_in.get_shape()[-1:], dtype=None, initializer=self.initializer_one(), trainable=True)
        self.tensor_cont = tf.nn.batch_normalization(
                                                    tensor_in,
                                                    tensor_mean,
                                                    tensor_variance,
                                                    offset=tensor_offset,
                                                    scale=tensor_scale,
                                                    variance_epsilon=0.000001,
                                                    name=None if name is None else self.prefix_batch_norm+name+self.postfix_batch_norm
                                                    )
        return self.tensor_cont
        
    def add_moment(self, tensor_in=None, axes=[0], keep_dims=False, name=None):
        mean, variance = tf.nn.moments(
                                        x=tensor_in if tensor_in is not None else self.tensor_cont,
                                        axes=axes,#[batch, height, width, depth], pass axes=[0, 1, 2].for simple batch normalization pass axes=[0] (batch only).
                                        shift=None,
                                        name=None if name is None else name,
                                        keep_dims=keep_dims
                                        )
        return mean, variance
        
    def add_moving_average(self, decay=0.999, num_updates=None, zero_debias=False, name='ExponentialMovingAverage'):
        return tf.train.ExponentialMovingAverage(decay=decay, 
                                                num_updates=num_updates,
                                                zero_debias=zero_debias,
                                                name=name)
    
    def add_pad(self, pad, tensor_in=None, mode='CONSTANT', name=None, constant_values=0):
        '''
        tensor: A Tensor.
        paddings: A Tensor of type int32.[[batch, batch], [height, height], [width, width], [channel, channel]]
        mode: One of "CONSTANT", "REFLECT", or "SYMMETRIC" (case-insensitive)
        name: A name for the operation (optional).
        constant_values: In "CONSTANT" mode, the scalar pad value to use. Must be same type as tensor.
        '''
        tensor_in = tensor_in if tensor_in is not None else self.tensor_cont
        self.tensor_cont = tf.pad(tensor_in, pad, mode, name, constant_values)
        return self.tensor_cont
    
    def add_concat(self, tensors_in, axis=1, name=None):
        '''
        values: A list of Tensor objects or a single Tensor.
        axis: 0-D int32 Tensor. Dimension along which to concatenate. Must be in the range [-rank(values), rank(values)). As in Python, indexing for axis is 0-based. Positive axis in the rage of [0, rank(values)) refers to axis-th dimension. And negative axis refers to axis + rank(values)-th dimension.
        '''
        return tf.concat(tensors_in, axis, name)
    
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

