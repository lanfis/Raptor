#!/usr/bin/env python
# license removed for brevity


class DATASET_PACKER():
    data_info = {}
    #datas = {file_name : {class : {'bbox' : [bbox], 'mask' : [mask], 'label' : [label]}}}
    #file_name 
    #--class_name
    #----bbox [[], []]
    #----mask [[], []]            
    def add_file_name_class(self, file_name, classes):
        if file_name in self.data_info:
            if classes in self.data_info[file_name]:
                return self.data_info
            else:
                self.data_info[file_name][classes] = {}
        else:
            data = {classes : {}}
            self.data_info[file_name] = data
        
        return self.data_info     
        
    def add_content(self, file_name, classes, content_dict, content):
        if file_name in self.data_info:
            if classes in self.data_info[file_name]:
                if content_dict in self.data_info[file_name][classes]:
                    self.data_info[file_name][classes][content_dict] += [content]
                else:
                    self.data_info[file_name][classes][content_dict] = [content]
            else:
                self.data_info[file_name][classes] = {content_dict : [content]}
        else:
            data = {classes : {content_dict : [content]}}
            self.data_info[file_name] = data
        
        return self.data_info
        
    def add_label(self, file_name, classes, label):
        return self.add_content(file_name, classes, 'label', label)
        
    def add_bbox(self, file_name, classes, bbox):
        return self.add_content(file_name, classes, 'bbox', bbox)
        
    def add_mask(self, file_name, classes, mask):
        return self.add_content(file_name, classes, 'mask', mask)
        
    def check_path(self, path):
        return os.path.exists(path)

    def current_time(self):
        return time.strftime("%Y%m%d%H%M%S", time.localtime()) #%Y-%m-%d %H:%M:%S

    def current_time_stamp(self):
        return time.time()
        
    def update_data(self, data):
        self.data_info.update(data)
        return self.data_info
        
    def set_data(self, data):
        self.data_info = data
        
    def get_data(self):
        return self.data_info
    
    def __init__(self):
        pass
    def __del__(self):
        pass


