#!/usr/bin/env python
# license removed for brevity

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import numpy as np
import time

import tensorflow as tf

from models.tf_nn_builder import NN_BUILDER
from models.tf_dataset_builder import DATASET_BUILDER

from models.tf_resnet import resnet_builder as tf_model
#from models.tf_mnist import mnist_builder as tf_model
#from models.tf_resnet_24 import resnet_builder as tf_model
import ops.tf_nn_optimizer_ops as tf_optimizer_op
import ops.tf_util_ops as tf_util_op

from dataset_retriever import DATASET_RETRIEVER
from dataset_label_encoder import DATASET_LABEL_ENCODER

import utils.cv_utils as cv_util
import cv2

flag_image_show = False
flag_save = True
flag_restore = False
lr = 0.00001
training_cycle = 10000
use_gpu = True
img_size = 64#240#64
batch_size = 128#16#128
padding = 'VALID'#'VALID'#'SAME'

print("--Initializing ...")
tf_dataset_builder = DATASET_BUILDER()
dataset_folder = os.path.join(current_folder, "..", "..", "image_database")
#index_file = os.path.join(current_folder, "..", "..", "image_database", "dataset_index.txt")
index_file = os.path.join(current_folder, "..", "..", "image_database", "dataset_index_LPI.txt")

dataset_retriever = DATASET_RETRIEVER()
dataset_retriever.dataset_folder = dataset_folder
dataset_retriever.index_file = index_file
dataset_retriever.load_index_file(index_file)
dataset_retriever.retrieve_data()
dataset_data = dataset_retriever.get_dataset_data()

print("--Encoding dataset labels ...")
dataset_label_encoder = DATASET_LABEL_ENCODER()
for i in dataset_data:
    dataset_label_encoder.add_class(dataset_data[i].keys())
dataset_data, convert_table, deconvert_table = dataset_label_encoder.label_dataset_data(dataset_data)
    

index_path_list = list(dataset_data.keys())
index_label_list = []
for i in dataset_data.keys():
    for c in dataset_data[i].keys():
        index_label_list.append(dataset_data[i][c]['label'][0])
        
#np.random.shuffle(path_label_list)

    
index_path_tensor_list = tf_util_op.convert_to_tensor(index_path_list, dtype=tf.string)
index_code_tensor_list = tf_util_op.convert_to_tensor(index_label_list, dtype=tf.int32)
#partitions = [0] * len(index_code_tensor_list)
#random.shuffle(partitions)
dataset_queue = tf_dataset_builder.dataset_tensor_queue([index_path_tensor_list, index_code_tensor_list], shuffle=True, queue_size=batch_size)



tf_builder = NN_BUILDER(use_gpu)

input_channels = 1
output_labels = len(convert_table)

optimizer = tf_optimizer_op.optimizer_adam(learning_rate=lr)
#optimizer = tf_optimizer_op.optimizer_sgd(learning_rate=lr)
initializer =  tf_builder.initializer_xavier(is_uniform=False)
#initializer = tf_builder.initializer_truncated_normal()
#initializer = tf_builder.initializer_rand_uniform(min_value=-10.0, max_value=10.0)

data_input  = tf_util_op.add_variable_hold([None, img_size * img_size * input_channels], name="data_input")
label_input = tf_util_op.add_variable_hold([None, output_labels], dtype=tf.float32, name="label_input")
print("--Initializing model ...")
tensor_in = tf.reshape(data_input, [-1, img_size, img_size, input_channels])
#softmax, keep_prob = tf_model(tensor_in, input_channels, output_labels, padding, initializer, use_gpu) 
softmax, keep_prob, tensor_conv_bn, tensor_bottleneck = tf_model(tensor_in, input_channels, output_labels, padding, kernel_size=3, strides=2, kernel_filters=64, bottleneck_depth=3, initializer=initializer) 

print("--Setting loss function ...")
loss = tf_util_op.loss(tensor_labels=label_input, tensor_logits=softmax)

print("--Setting optimizer ...")
train_step = tf_optimizer_op.optimizer_minimize(optimizer, loss)

print("--Setting predict function ...")
predict = tf_util_op.tensor_argmax(softmax)

print("--Setting accuracy function ...")
accuracy = tf_util_op.accuracy(tf_util_op.tensor_cast(predict, tf.int32), tf_util_op.tensor_cast(tf_util_op.tensor_argmax(label_input), tf.int32))

#mnist = tf.contrib.learn.datasets.mnist.read_data_sets('/tmp/mnist', one_hot=True)

saver = tf.train.Saver()
model_weight = "model.ckpt"


image_data_content = tf.read_file(dataset_queue[0])
image_raw = tf.image.decode_png(image_data_content, channels=input_channels)
image_crop = tf.image.central_crop(image_raw, 0.8)
train_image = tf.image.resize_images(image_crop, [img_size, img_size])
train_image = tf_util_op.tensor_cast(train_image, tf.float32)
train_image = tf.divide(train_image, tf.constant(255.0, dtype=tf.float32, shape=train_image.shape))

train_label = tf.one_hot(tf_util_op.tensor_cast(dataset_queue[1], tf.int32), output_labels)
train_label = tf_util_op.tensor_cast(train_label, tf.float32)


train_image_batch, train_label_batch = tf_dataset_builder.dataset_tensor_batch(
                                    [train_image, train_label],
                                    batch_size=batch_size,
                                    threads=4
                                    )

'''
def img_func(filename, label):
    image_string = tf.read_file(filename)
    image_decoded = tf.image.decode_png(image_string, channels=1)
    image_resized = tf.image.resize_images(image_decoded, [img_size, img_size])
    label = tf.one_hot(tf_util_op.tensor_cast(label, tf.int32), output_labels)
    return image_resized, label

element_iter = tf_dataset_builder.dataset_fast_generator((tagger.index_path_list, tagger.index_code_list), img_func, len(tagger.index_path_list), batch_size, threads=4)
bx, by = tf_dataset_builder.get_element_op()
'''
'''
data_path = os.path.join(current_folder, "..", "..", "nn", "caffe2_data", "source_data", "cifar", "cifar10", "data_batch_1.bin")
print("--data_path : {}".format(data_path))
train_image_batch, train_label_batch = cifar_input.build_input('cifar10', data_path, batch_size, 'train')
print(train_image_batch)
print(train_label_batch)
'''
with tf.Session(config=tf.ConfigProto(allow_soft_placement=True, log_device_placement=True)) as sess:
    sess.run(tf.global_variables_initializer())
    if flag_restore:
        saver.restore(sess, os.path.join(current_folder, model_weight))
    
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)
    
    print("--starting training ...")
    for i in range(training_cycle):
        try:
            #batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            ##tf.reshape(batch_ys, [batch_size, -1])
            ##print("--{}".format(batch_xs))
            ##print("--{}".format(batch_ys))
            
            #batch_xs = np.reshape(batch_xs, (batch_size, img_size, img_size, -1))
            ##batch_ys = tf.one_hot(batch_ys, output_labels).eval()
            #batch_xs, batch_ys = tf_dataset_builder.get_element_op()
            batch_xs, batch_ys = sess.run([train_image_batch, train_label_batch])
            #print(batch_xs.shape)
            #print(batch_ys.shape)
            #Image.fromarray(np.asrray(batch_xs)).show
            
            '''
            if flag_image_show:
                cv_util.image_channel_show(batch_xs, 'image')
            '''
            #batch_xs = np.reshape(batch_xs, (-1, img_size* img_size))
            batch_xs = np.reshape(batch_xs, (batch_size, -1))
            #batch_ys = train_label_batch.eval()
            #batch_ys = tf.one_hot(batch_ys, output_labels).eval()
            
            sess.run(train_step, feed_dict={data_input: batch_xs, label_input: batch_ys, keep_prob: 1.0})
            
            if flag_image_show:
                batch_conv, batch_bottleneck = sess.run([tensor_conv_bn, tensor_bottleneck], feed_dict={data_input: batch_xs, label_input: batch_ys, keep_prob: 1.0})
                cv_util.image_channel_show(batch_conv, 'image_conv')
                cv_util.image_channel_show(batch_bottleneck, 'image_bottleneck')
            
            train_accuracy, train_loss = sess.run([accuracy, loss], feed_dict={data_input: batch_xs, label_input: batch_ys, keep_prob: 1.0})
            predict_val = predict.eval(session=sess, feed_dict={data_input: batch_xs, keep_prob: 1.0})
            print("--Processing {} : accuracy = {:<8} loss = {:<8} label = {} / {}".format(i, train_accuracy, train_loss, len(set(predict_val)), output_labels))
            print(predict_val)
            
        except tf.errors.OutOfRangeError:
            break
    if flag_save:
        save_path = saver.save(sess, os.path.join(current_folder, model_weight))
        print("Model saved in path: %s" % save_path)
    
    
    coord.request_stop()
    coord.join(threads)
    

#test_pic_path = current_folder
#test_pic_file = "8.png"

def image_read(test_pic_file):
    test_pic_path = current_folder
    img = cv2.imread(os.path.join(test_pic_path, test_pic_file), cv2.IMREAD_GRAYSCALE)
    rows = img.shape[0]
    cols = img.shape[1]
    min_edge = min(rows, cols)
    img_crop = img[int(rows/2-min_edge/2):int(rows/2+min_edge/2), int(cols/2-   min_edge/2):int(cols/2+min_edge/2)]
    img_src = cv2.resize(img_crop, (img_size, img_size))
    #img_src = 255 - img_src
    img_mod = img_src.reshape(-1, img_size * img_size)
    return img_mod


sess = tf.Session()
#predict = tf_util_op.tensor_argmax(softmax)
with tf.device("/device:{}:0".format("GPU" if use_gpu else "CPU")):
    saver.restore(sess, os.path.join(current_folder, model_weight))

    test_pic_file = "2.png"
    img_mod = image_read(test_pic_file)
    predict_val = predict.eval(session=sess, feed_dict={data_input: img_mod, keep_prob: 1.0})

    print("--file = {}".format(test_pic_file))
    print("--max = {}".format(int(predict_val)))
    print("--label = {}".format(deconvert_table[int(predict_val)]))
    
    test_pic_file = "3.png"
    img_mod = image_read(test_pic_file)
    predict_val = predict.eval(session=sess, feed_dict={data_input: img_mod, keep_prob: 1.0})

    print("--file = {}".format(test_pic_file))
    print("--max = {}".format(int(predict_val)))
    print("--label = {}".format(deconvert_table[int(predict_val)]))
    
    test_pic_file = "5.png"
    img_mod = image_read(test_pic_file)
    predict_val = predict.eval(session=sess, feed_dict={data_input: img_mod, keep_prob: 1.0})

    print("--file = {}".format(test_pic_file))
    print("--max = {}".format(int(predict_val)))
    print("--label = {}".format(deconvert_table[int(predict_val)]))
    '''
    test_pic_file = "8.png"
    img_mod = image_read(test_pic_file)
    predict_val = predict.eval(session=sess, feed_dict={data_input: img_mod, keep_prob: 1.0})

    print("--file = {}".format(test_pic_file))
    print("--max = {}".format(int(predict_val)))
    print("--label = {}".format(deconvert_table[int(predict_val)]))
    '''
    test_pic_file = "7_color.png"
    img_mod = image_read(test_pic_file)
    predict_val = predict.eval(session=sess, feed_dict={data_input: img_mod, keep_prob: 1.0})

    print("--file = {}".format(test_pic_file))
    print("--max = {}".format(int(predict_val)))
    print("--label = {}".format(deconvert_table[int(predict_val)]))
sess.close()

