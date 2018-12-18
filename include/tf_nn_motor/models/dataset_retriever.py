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
from tf_index_controler import INDEX_CONTROLER
from dataset_packer import DATASET_PACKER

class DATASET_RETRIEVER():
    program_name_ = __name__
    consoler_ = Console_Formatter(program_name_)
    index_controler_ = INDEX_CONTROLER()
    dataset_packer = DATASET_PACKER()
    
    current_folder = os.path.join(os.getcwd())
    dataset_folder  = os.path.join(current_folder, 'dataset_folder')
    index_file = os.path.join(current_folder, "dataset_index.txt")
    
    index_list = []
    it_ = None
    fid_index_file_ = None
    def load_index_file(self, data_path=None):
        data_path = self.index_file if data_path == None else data_path
        if not self.check_path(data_path):
            print(self.consoler_.ERR("Index file : \"{}\" not found !".format(self.data_path)))
            return False
        print(self.consoler_.INFO("Loading index file : \"{}\" ...".format(self.index_file)))
        self.fid_index_file_ = open(data_path, 'r')
        self.index_list = np.append(self.index_list, self.index_controler_.load_index_file(data_path))
        print(self.consoler_.INFO("Loading index file ok !".format(self.index_file)))
        self.it_ = iter(self.index_list)
        return True

    def retrieve_data(self, index=-1):
        if self.index_list == []:
            print(self.consoler_.WARN("Not loading index file yet !"))
            return None, None, False
        if index > self.index_list.shape[0]:
            print(self.consoler_.WARN("Index over index file size !"))
            return None, None, False
        while True:
            try:
                path, label = self.parse_index_content(next(self.it_) if index < 0 else self.index_list[index])
                if not self.check_path(os.path.join(self.dataset_folder, path.strip())):
                    continue
                print(self.consoler_.INFO("Retrieving label : \"{}\" >> file : \"{}\" ...".format(label, path)))
                img_path = os.path.join(self.dataset_folder, path)
                
                self.dataset_packer.add_file_name_class(img_path, label)
                #return img_path, label, True
            except StopIteration:
                return None, None, False
        
    def parse_index_content(self, index_content):
        parse_content = index_content.split(',')
        path = parse_content[0].strip()
        label = parse_content[1].strip()
        return path, label
        
    def load_coco_mask(self, dataset_dir='.', data_type='instances', data_year='val2014', class_names=[], is_crowd=None, is_anns=True):
        from api_coco import API_COCO
        coco = API_COCO()
        print(self.consoler_.INFO("Starting load COCO ..."))
        coco.load_coco(dataset_dir=dataset_dir, data_type=data_type, data_year=data_year)
        coco_data = coco.parse_coco(class_names=class_names, is_crowd=is_crowd, is_anns=is_anns)
        for i in coco_data.keys():
            print(self.consoler_.INFO("Loading COCO data : {} ...".format(i)))
            for ann_idx in range(len(coco_data[i]['annotation'])):
                for c in coco_data[i]['annotation'][int(ann_idx)]:
                    #bbox = c['bbox']
                    mask = c#c['segmentation']#coco.ann_to_mask(c)
                    #data_info = self.dataset_packer.add_bbox(file_name=coco_data[i]['file_name'], classes=coco_data[i]['class_name'][int(ann_idx)], bbox=bbox)
                    data_info = self.dataset_packer.add_mask(file_name=coco_data[i]['file_name'], classes=coco_data[i]['class_name'][int(ann_idx)], mask=mask)
        print(self.consoler_.INFO("Loading COCO data ok !"))
        return data_info
        
    def set_dataset_packer(self, packer):
        self.dataset_packer = packer
        
    def get_dataset_packer(self):
        return self.dataset_packer
        
    def get_dataset_data(self):
        return self.dataset_packer.get_data()    

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
        
    def __init__(self):
        pass
    def __del__(self):
        if not self.fid_index_file_ == None:
            self.fid_index_file_.close()


    
    

