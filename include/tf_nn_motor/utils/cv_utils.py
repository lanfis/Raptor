#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import numpy as np
import cv2
import math


def image_batch_show(image_batch, window_name='image', wait_time=1):
    batch_size = image_batch.shape[0]
    channels = image_batch.shape[3] 
    rows = int(math.sqrt(batch_size))
    cols = int(batch_size / rows)
    
    for ch in range(channels):
        for r in range(rows):
            for c in range(cols):
                if int(c) == 0:
                    image_r = image_batch[int(r) * cols + int(c), :, :, int(ch)]
                else:
                    image_r = image_horizontal_concat(image_r, image_batch[int(r) * cols + int(c), :, :, int(ch)])
            if int(r) == 0:
                image = image_r
            else:
                image = image_vertical_concat(image, image_r)
                
    image_show(image, window_name, wait_time)
    return image
    
def image_channel_show(image_batch, window_name='image', wait_time=1):
    batch_size = image_batch.shape[0]
    channels = image_batch.shape[3] 
    rows = int(math.sqrt(channels))
    cols = int(channels / rows)
    
    for bh in range(batch_size):
        for r in range(rows):
            for c in range(cols):
                if int(c) == 0:
                    image_r = image_batch[int(bh), :, :, int(r) * cols + int(c)]
                else:
                    image_r = image_horizontal_concat(image_r, image_batch[int(bh), :, :, int(r) * cols + int(c)])
            if int(r) == 0:
                image = image_r
            else:
                image = image_vertical_concat(image, image_r)
                
    image_show(image, window_name, wait_time)
    return image

def image_horizontal_concat(image_src, image):
    return cv2.hconcat((image_src, image))
    
def image_vertical_concat(image_src, image):
    return cv2.vconcat((image_src, image))

def image_show(image, window_name='image', wait_time=1):
    cv2.imshow(window_name, image)
    cv2.waitKey(wait_time)

def image_save(image, file_name):
    cv2.imwrite(file_name, image)
