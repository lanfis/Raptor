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
from tf_dataset_retriever import DATASET_RETRIEVER

import numpy as np
import time
import shutil
import csv

class DATASET_LABEL_ENCODER:
    #PUBLIC
    current_folder = os.path.join(os.getcwd())
    dataset_folder  = os.path.join(current_folder, 'dataset_folder')
    index_file = os.path.join(current_folder, "dataset_index.txt")
    dataset_mark_name = ""

    index_list = []
    #FOR ENCODING INDEX LIST
    index_path_list = []
    index_label_list = []
    index_code_list = []
    #FOR ENCODING FUNC
    label_list = []
    code_list = []

    use_gpu = False

    #PRIVATE
    program_name_ = __name__
    consoler_ = Console_Formatter(program_name_)
    retriever_ = DATASET_RETRIEVER()
    count_ = 0
    
    
    def __init__(self, use_gpu=False):
        self.use_gpu = use_gpu

    def __del__(self):
        pass

    def init(self):
        self.retriever_.init()
        
    def encoding_index_list(self):
        status = True
        path_label_list = []
        while status:
            img_path, label, status = self.retriever_.retrieve_data()
            if not status:
                break
            code = self.encoding_list_search(label.strip())
            self.index_path_list = np.append(self.index_path_list, img_path.strip())
            self.index_label_list = np.append(self.index_label_list, label.strip())
            self.index_code_list  = np.append(self.index_code_list, code)
            path_label_list = np.append(path_label_list, img_path.strip()+","+label.strip())
                
        return path_label_list
            
    def encoding_list_search(self, label):
        if self.label_list == []:
            self.encoding_function(label)
            return self.code_list[0]
        label_it = iter(self.label_list)
        code_it  = iter(self.code_list)
        while True:
            try:
                label_ = next(label_it)
                code_  = next(code_it)
                if label_.strip() == label.strip():
                    return code_
            except StopIteration:
                self.encoding_function(label)
                return self.code_list[0]
            
    def encoding_function(self, label):
        if self.label_list == []:
            self.label_list = [label.strip()]
            self.code_list  = [self.count_]
            #self.label_list.insert(0, label.strip())
            #self.code_list.insert(0, self.count_)
            self.count_ += 1
            return True
        self.label_list.insert(len(self.label_list), label.strip())
        self.code_list.insert(len(self.code_list), self.count_)
        self.count_ += 1
        return True
    
    def load_index_file(self, data_path=None):
        self.index_list = self.retriever_.load_index_file(data_path)
        return self.index_list
        
    def set_dataset_folder(self, data_path=None):
        self.dataset_folder = self.dataset_folder if data_path == None else data_path
        self.retriever_.dataset_folder = self.dataset_folder
        return self.check_path(self.dataset_folder)
    
    def set_index_file(self, file_path=None):
        self.index_file = self.index_file if file_path == None else file_path
        self.retriever_.index_file = self.index_file
        return self.check_path(self.index_file)
        
    def check_path(self, path):
        return os.path.exists(path)

    def current_time(self):
        return time.strftime("%Y%m%d%H%M%S", time.localtime()) #%Y-%m-%d %H:%M:%S

    def current_time_stamp(self):
        return time.time()



