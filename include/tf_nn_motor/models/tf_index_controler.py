#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

config_folder = os.path.join(current_folder, "..", "..", "matrix", "python")
sys.path.append(config_folder)
from console_formatter import Console_Formatter

import numpy as np
import time
import csv

class INDEX_CONTROLER:
    #PUBLIC
    current_folder = os.path.join(os.getcwd())
    index_file = os.path.join(current_folder, "dataset_index.txt")


    #PRIVATE
    program_name_ = __name__
    consoler_ = Console_Formatter(program_name_)
    fid_index_file_ = None
    index_list = []

    def __init__(self):
        pass

    def __del__(self):
        self.close_file()

    def load_index_file(self, data_path=None, is_create_data=False):
        data_path = self.index_file if data_path == None else data_path
        if not self.check_path(data_path):
            #print(self.consoler_.WARN("index file : \"{}\" not found !".format(self.data_path)))
            if is_create_data:
                self.fid_index_file_ = open(data_path, 'w+')
            return self.index_list
        #print(self.consoler_.INFO("loading index file ..."))
        self.close_file()
        self.fid_index_file_ = open(data_path, 'r+')
        self.index_list = self.fid_index_file_.readlines()
        return self.index_list
        '''
        index_list = []
        with open(data_path, 'r') as fid:
            infile_cursor = csv.reader(fid, delimiter=',')
            
            for row in infile_cursor:
                index_list = np.append(index_list, row)# [row[0], row[1]])
        return index_list
        '''

    def write_index_file(self, data, recursive_search=True):
        if self.fid_index_file_ == None:
            return False
        it_ = iter(self.index_list)
        while recursive_search:
            try:
                if next(it_).strip() == data.strip():
                    return False
            except StopIteration:
                break
            
        data = "{}\n".format(data)
        self.index_list = np.append(self.index_list, data)
        self.fid_index_file_.write(data)
        return True

    def close_file(self, fid=None):
        fid = self.fid_index_file_ if fid == None else fid
        if fid != None:
            fid.close()

    def check_path(self, path):
        return os.path.exists(path)

    def current_time(self):
        return time.strftime("%Y%m%d%H%M%S", time.localtime()) #%Y-%m-%d %H:%M:%S

    def current_time_stamp(self):
        return time.time()



