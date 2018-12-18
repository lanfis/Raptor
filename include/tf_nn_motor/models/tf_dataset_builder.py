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

import ops.tf_util_ops as tf_util_op

class DATASET_BUILDER:
    #PUBLIC
    
    #PRIVATE
    dataset = None
    iterator = None
    reader = None

    def __init__(self):
        None
        
    def dataset_fast_generator(self, tensor_list, mapping_func, shuffle_size, batch_size, repeats=None, iterator_type="one_hot", threads=None):
        dataset_tensor = self.dataset_tensor(tensor_list)#tensor_list = [a, b]
        self.set_repeat(repeats)
        self.set_map(mapping_func, num_parallel_calls=threads)
        self.set_shuffle(shuffle_size)
        self.set_batch(batch_size)
        dataset_iterator = self.set_iterater(type=iterator_type)
        return self.get_element_op()
        '''
        def img_func(filename, label):
            image_string = tf.read_file(filename)
            image_decoded = tf.image.decode_png(image_string, channels=1)
            image_resized = tf.image.resize_images(image_decoded, [img_size,        img_size])
            label = tf.one_hot(tf_util_op.tensor_cast(label, tf.int32), output_labels)
            return image_resized, label
    
        element_iter = tf_dataset_builder.dataset_fast_generator((filename, code), img_func)
        bx, by = tf_dataset_builder.get_element_op()
        '''

    def get_element_op(self):
        if self.iterator == None:
            return None
        next_element = self.iterator.get_next()
        return next_element
    
    def set_iterator(self, dataset=None, type="one_shot", shared_name=None):
        self.dataset = self.dataset if dataset is None else dataset
        if self.dataset == None:
            return None
        if type == "initializable":
            iterator = self.dataset.make_initializable_iterator(shared_name)
        elif type == "one_shot":
            iterator = self.dataset.make_one_shot_iterator()
        else:
            iterator = self.dataset.make_one_shot_iterator()
        self.iterator = iterator
        return self.iterator
        
    def set_map(self, func, num_parallel_calls=None):
        if self.dataset == None:
            return None
        self.dataset = self.dataset.map(func, num_parallel_calls)
        return self.dataset
    
    def set_batch(self, batch_size):
        if self.dataset == None:
            return None
        self.dataset = self.dataset.batch(batch_size)
        return self.dataset
        
    def set_shuffle(self, buffer_size):
        if self.dataset == None:
            return None
        self.dataset = self.dataset.shuffle(buffer_size)
        return self.dataset
        
    def set_repeat(self, count=None):
        if self.dataset == None:
            return None
        self.dataset = self.dataset.repeat(count)#The default behavior (if count is None or -1) is for the elements to be repeated indefinitely
        return self.dataset
    
    def set_reader_csv(self):
        self.reader = tf.TextLineReader()
        return self.reader
    
    def set_dataset_filename_queue(self, filenames, epochs=None, shuffle=False, capacity=32):
        filename_queue = tf.train.string_input_producer(
                            string_tensor=filenames,
                            num_epochs=epochs,
                            shuffle=shuffle,
                            seed=None,
                            capacity=capacity,
                            shared_name=None,
                            name=None,
                            cancel_op=None
                            )
        return filename_queue
    
    def dataset_range(self, max_value, min_value=0, interval=1):
        self.dataset = tf.data.Dataset.range(min_value, max_value, interval)
        return self.dataset
    
    def dataset_tensor(self, tensor):
        self.dataset = tf.data.Dataset.from_tensor_slices(tensor)
        return self.dataset

    def dataset_zip(self, datasets):
        self.dataset = tf.data.Dataset.zip(datasets)
        return self.dataset
        
    def dataset_concatenate(self, dataset):
        self.dataset = self.dataset.concatenate(dataset)
        return self.dataset
        
    def dataset_generator(self, gen, gen_type, gen_shape=None):
        self.dataset = tf.data.Dataset.from_generator(gen, gen_type, gen_shape)
        return self.dataset
    
    def get_dataset(self):
        return self.dataset
        
    def set_dataset(self, dataset):
        self.dataset = dataset
    ##
    def dataset_tensor_queue(self, tensor_list, epoch=None, shuffle=False, queue_size=32, name=None):
        dataset_queue = tf.train.slice_input_producer(
                        tensor_list, 
                        num_epochs=epoch, 
                        shuffle=shuffle, 
                        seed=None, 
                        capacity=queue_size, 
                        shared_name=None, 
                        name=None)
        return dataset_queue

    def dataset_tensor_batch(self, tensor, batch_size=64, threads=1):
        return tf.train.batch(tensor, batch_size=batch_size, num_threads=threads)



