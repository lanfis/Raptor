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
#from dataset_packer import DATASET_PACKER
from dataset_retriever import DATASET_RETRIEVER
from dataset_label_encoder import DATASET_LABEL_ENCODER


if __name__ == "__main__":
    from api_coco import API_COCO

    coco = API_COCO()
    data_retr = DATASET_RETRIEVER()
    path = '/home/dataset/MS_COCO'
    
    #data_retr.load_coco_mask(path, class_names=[])
    data_retr.load_coco_mask(path, class_names=['person', 'dog'])
    image_info = data_retr.get_dataset_data()
    #print(image_info)
    
    dl_encoder = DATASET_LABEL_ENCODER()
    for i in image_info:
        dl_encoder.add_class(image_info[i].keys())
    labeled_data, convert_table, deconvert_table = dl_encoder.label_dataset_data(image_info)
    print(convert_table)
    print(deconvert_table)
    #print(labeled_data)
    
    

