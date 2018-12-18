#!/usr/bin/env python
# license removed for brevity


class TF_NN_MOTOR_DATA_CONTROLER():
    motor_status_list = {}
    #motor_status = {1 : {id : 1, position : 1, speed : 1, load : 1, voltage : 1, temperature : 1}}
    def update_data(self, motor_id, data_name, data):
        if motor_id not in self.motor_status_list:
            self.add_motor(motor_id)
        self.motor_status_list[motor_id][data_name] = data
        
    def get_data(self, motor_id, data_name):
        if motor_id not in self.motor_status_list:
            return NULL
        else:
            if data_name not in self.motor_status_list[motor_id]:
                return NULL
            else:
                return self.motor_status_list[motor_id][data_name]      
            
    def add_motor(self, motor_id):
        if motor_id not in self.motor_status_list:
            content = {'id' : int(motor_id)}
            self.motor_status_list[motor_id] = content
    
    def __call__(self, motor_id, data_name, data):
        self.update_data(motor_id, data_name, data)
    '''
    def __call__(self, motor_id, data_name):
        return self.get_data(motor_id, data_name)
    '''
    def __init__(self):
        pass
    
    def __del__(self):
        pass


