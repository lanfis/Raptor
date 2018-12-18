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

class DATASET_CONSTRUCTOR:
    #PUBLIC
    current_folder = os.path.join(os.getcwd())
    source_folder = os.path.join(current_folder, 'source_folder')
    output_folder  = os.path.join(current_folder, 'dataset_folder')
    index_file = os.path.join(current_folder, "dataset_index.txt")
    dataset_mark_name = ""

    src_path_list = []
    src_folder_list = []
    label_list = []
    index_list = []

    use_gpu = False
    flag_folder_transfer = False
    flag_path_transfer = False

    #PRIVATE
    program_name_ = __name__
    consoler_ = Console_Formatter(program_name_)
    index_controler_ = INDEX_CONTROLER()

    def __init__(self, use_gpu=False):
        self.use_gpu = use_gpu

    def __del__(self):
        pass

    def init(self):
        self.current_folder = os.path.realpath(self.current_folder)
        self.source_folder = os.path.realpath(self.source_folder)
        self.output_folder = os.path.realpath(self.output_folder)
        self.index_file = os.path.realpath(self.index_file)
        print(self.consoler_.INFO("initializing ..."))
        print(self.consoler_.INFO("checking files ..."))

        if not self.check_path(self.source_folder):
            print(self.consoler_.WARN("source folder : \"{}\" not found !".format(self.source_folder)))
            print(self.consoler_.WARN("creating source folder : \"{}\" ...".format(self.source_folder)))
            os.makedirs(self.source_folder)   
        else:
            print(self.consoler_.INFO("source folder : \"{}\" ok !".format(self.source_folder)))

        if not self.check_path(self.output_folder):
            print(self.consoler_.WARN("output folder : \"{}\" not found !".format(self.output_folder)))
            print(self.consoler_.WARN("creating output folder : \"{}\" ...".format(self.output_folder)))
            os.makedirs(self.output_folder)   
        else:
            print(self.consoler_.INFO("output folder : \"{}\" ok !".format(self.output_folder)))
            
        if not self.check_path(self.index_file):
            print(self.consoler_.WARN("index file : \"{}\" not found !".format(self.index_file)))
            print(self.consoler_.WARN("creating index file : \"{}\" ...".format(self.index_file)))
            with open(self.index_file, 'w') as fid:
                pass
            self.index_controler_.load_index_file(self.index_file)
        else:
            self.index_controler_.load_index_file(self.index_file)
            print(self.consoler_.INFO("index file : \"{}\" ok !".format(self.index_file)))

    def run_transfer_data(self):
        if not self.check_path(os.path.join(self.output_folder, self.dataset_mark_name)):
            os.makedirs(os.path.join(self.output_folder, self.dataset_mark_name))
        dst_folder = self.dataset_mark_name
        if self.flag_folder_transfer:
            for dirs_i in range(self.src_folder_list.shape[0]):
                src_folder = str(self.src_folder_list[int(dirs_i)])
                if not self.check_path(os.path.join(self.source_folder, src_folder)):
                    print(self.consoler_.WARN("source directories : \"{}\" not found !".format(src_folder)))
                else:
                    file_list = self.list_files(os.path.join(self.source_folder, src_folder))
                    for i in range(len(file_list)):
                        src_data_name = file_list[int(i)]
                        #dst_data_name = "{}_{}".format(self.current_time_stamp(), os.path.split(src_data_name)[1])
                        dst_data_name = "{}".format(os.path.split(src_data_name)[1])
                        src_data_path = os.path.join(self.source_folder, src_folder, src_data_name)
                        dst_data_path = os.path.join(self.output_folder, dst_folder, dst_data_name)
                        
                        if not self.check_path(dst_data_path):
                            print(self.consoler_.INFO("transfering : {} >> {}".format(os.path.join(src_folder, src_data_name), os.path.join(dst_folder, dst_data_name))))
                            index = "{}, {}".format(os.path.join(self.dataset_mark_name, dst_data_name), self.label_list[int(dirs_i)])
                            self.index_controler_.write_index_file(index)
                            self.transfer_data(src_data_path, dst_data_path)
                        else:
                            print(self.consoler_.WARN("transfering : \"{}\" file same name occur !".format(os.path.join(dst_folder, dst_data_name))))
                            index = "{}, {}".format(os.path.join(self.dataset_mark_name, dst_data_name), self.label_list[int(dirs_i)])
                            self.index_controler_.write_index_file(index)

    def load_dir_label_list(self, data_path):##TODO overwriting from "csv reader" to "io"
        if not self.check_path(data_path):
            print(self.consoler_.WARN("directories_label_list file : \"{}\" not found !".format(self.data_path)))
            return None
        print(self.consoler_.INFO("loading directories_label_list file ..."))
        with open(data_path, 'r') as fid:
            infile_cursor = csv.reader(fid, delimiter=',')
            
            for row in infile_cursor:
                self.src_folder_list = np.append(self.src_folder_list, row[0].strip())
                self.label_list = np.append(self.label_list, row[1].strip())
            self.flag_folder_transfer = True
        return self.src_folder_list, self.label_list

    def transfer_data_function(self, src_data):
        return None

    def transfer_data(self, src_data_path, dst_data_path):
        if self.transfer_data_function(src_data_path) == None:
            shutil.copyfile(src_data_path, dst_data_path)
        return dst_data_path

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



