#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)
main_folder = os.path.join(current_folder, "..")
sys.path.append(main_folder)

import time
import numpy as np
full_path = os.path.dirname(__file__)
sys.path.append(full_path)

config_folder = os.path.join(current_folder, "..", "..", "matrix", "python")
sys.path.append(config_folder)
from console_formatter import Console_Formatter
from dataset_packer import DATASET_PACKER


class DATASET_LABEL_ENCODER():
    program_name_ = __name__
    consoler_ = Console_Formatter(program_name_)
    classes_labels_list = {}
    convert_table = {}
    deconvert_table = {}
    
    is_encode = False
    #classes_labels_list = {class : {'label' : label, 'count' : count}}
    #data
    #--class
    #----label
    #----count
    
    def add_class(self, cls):
        '''
        if type(cls) is not list:
            cls = list(cls)
        if not isinstance(output_slice, (tuple, list)):
            output_slice = [output_slice]
        '''
        print(self.consoler_.INFO("Adding class : {} ...".format(cls)))
        for c in cls:
            if c in self.classes_labels_list:
                self.classes_labels_list[c]['count'] += 1
            else:
                self.classes_labels_list[c] = {'count' : 1}
        
    def run_encoding(self, encoding_function=None):
        print(self.consoler_.INFO("Encoding ..."))
        encoding_function = self.encoding_function_ if encoding_function is None else encoding_function
        
        self.classes_labels_list = encoding_function(self.classes_labels_list)
        self.is_encode = True
        print(self.consoler_.INFO("Encoding ok !"))
        return self.classes_labels_list
        
    def label_dataset_data(self, dataset_data):
        if not self.is_encode:
            self.run_encoding()
        dataset_packer = DATASET_PACKER()
        dataset_packer.set_data(dataset_data)
        convert_table, deconvert_table = self.generate_convert_table()
        print(self.consoler_.INFO("Labeling dataset data : ..."))
        for i in dataset_data.keys():
            for c in dataset_data[i].keys():
                dataset_packer.add_label(i, c, convert_table[c])
        print(self.consoler_.INFO("Labeling dataset data ok !".format(i)))
        return dataset_packer.get_data(), convert_table, deconvert_table
        
    def generate_convert_table(self):
        if not self.is_encode:
            self.run_encoding()
        print(self.consoler_.INFO("Generating convert tables ..."))
        for c in self.classes_labels_list.keys():
            self.convert_table[c] = self.classes_labels_list[c]['label']
            self.deconvert_table[self.classes_labels_list[c]['label']] = c
        print(self.consoler_.INFO("Generating convert tables ok !"))
        return self.convert_table, self.deconvert_table
        
    def get_convert_table(self):
        return self.convert_table
        
    def get_deconvert_table(self):
        return self.deconvert_table        
            
    def encoding_function_(self, class_label_list):
        cl = []
        for c in class_label_list.keys():
            cl.append((c, class_label_list[c]['count']))
            
        cl = sorted(cl, key=lambda c: c[1], reverse=False)

        for i in range(len(cl)):
            class_label_list[cl[int(i)][0]]['label'] = int(i)
    
        return class_label_list
        
    def __init__(self):
        pass
    def __del__(self):
        pass

    
    

