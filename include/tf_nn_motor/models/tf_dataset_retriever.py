#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

config_folder = os.path.join(current_folder, "..", "..", "matrix", "python")
sys.path.append(config_folder)
from console_formatter import Console_Formatter
from tf_index_controler import INDEX_CONTROLER

import numpy as np
import time
import shutil
import csv
#import cv2

class DATASET_RETRIEVER:
    #PUBLIC
    current_folder = os.path.join(os.getcwd())
    dataset_folder  = os.path.join(current_folder, 'dataset_folder')
    index_file = os.path.join(current_folder, "dataset_index.txt")
    dataset_mark_name = ""

    index_list = []
    
    use_gpu = False

    #PRIVATE
    program_name_ = __name__
    consoler_ = Console_Formatter(program_name_)
    index_controler_ = INDEX_CONTROLER()
    
    it_ = None
    fid_index_file_ = None
    #count = 0

    def __init__(self, use_gpu=False):
        self.use_gpu = use_gpu

    def __del__(self):
        if not self.fid_index_file_ == None:
            self.fid_index_file_.close()

    def init(self):
        self.current_folder = os.path.realpath(self.current_folder)
        self.dataset_folder = os.path.realpath(self.dataset_folder)
        self.index_file = os.path.realpath(self.index_file)
        print(self.consoler_.INFO("initializing ..."))
        print(self.consoler_.INFO("checking files ..."))

        if not self.check_path(self.dataset_folder):
            print(self.consoler_.WARN("dataset folder : \"{}\" not found !".format(self.dataset_folder)))
            print(self.consoler_.WARN("creating dataset folder : \"{}\" ...".format(self.dataset_folder)))
            os.makedirs(self.dataset_folder)   
        else:
            print(self.consoler_.INFO("dataset folder : \"{}\" ok !".format(self.dataset_folder)))
            
        if not self.check_path(self.index_file):
            print(self.consoler_.WARN("index file : \"{}\" not found !".format(self.index_file)))
            print(self.consoler_.WARN("creating index file : \"{}\" ...".format(self.index_file)))
            with open(self.index_file, 'w') as fid:
                pass
        else:
            print(self.consoler_.INFO("index file : \"{}\" ok !".format(self.index_file)))
    
    def load_index_file(self, data_path=None):
        data_path = self.index_file if data_path == None else data_path
        if not self.check_path(data_path):
            print(self.consoler_.ERR("index file : \"{}\" not found !".format(self.data_path)))
            return None
        print(self.consoler_.INFO("loading index file : \"{}\" ...".format(self.index_file)))
        self.fid_index_file_ = open(data_path, 'r')
        self.index_list = np.append(self.index_list, self.index_controler_.load_index_file(data_path))
        print(self.consoler_.INFO("loading index file ok !".format(self.index_file)))
        self.it_ = iter(self.index_list)
        return self.index_list

    def retrieve_data(self, index=-1):
        if self.index_list == []:
            print(self.consoler_.WARN("not loading index file yet !"))
            return None, None, False
        if index > self.index_list.shape[0]:
            print(self.consoler_.WARN("index over index file size !"))
            return None, None, False
        while True:
            try:
                path, label = self.parse_index_content(next(self.it_) if index < 0 else self.index_list[index])
                if not self.check_path(os.path.join(self.dataset_folder, path.strip())):
                    continue
                print(self.consoler_.INFO("retrieving label : \"{}\" >> file : \"{}\" ...".format(label, path)))
                img_path = os.path.join(self.dataset_folder, path)
                #img = cv2.imread(img_path)
                return img_path, label, True
            except StopIteration:
                return None, None, False
        
    def parse_index_content(self, index_content):
        parse_content = index_content.split(',')
        path = parse_content[0].strip()
        label = parse_content[1].strip()
        return path, label

    def rewind_iterator(self):
        if self.index_list == []:
            return False
        self.it_ = iter(self.index_list)
        return True
        
    def check_path(self, path):
        return os.path.exists(path)

    def list_dirs(self, path):
        if not self.check_path(path):
            return None
        dir_list = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))] 
        return dir_list

    def list_files(self, path):
        if not self.check_path(path):
            return None
        file_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))] 
        return file_list

    def current_time(self):
        return time.strftime("%Y%m%d%H%M%S", time.localtime()) #%Y-%m-%d %H:%M:%S

    def current_time_stamp(self):
        return time.time()



