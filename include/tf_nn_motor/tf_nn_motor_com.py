#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

from tf_nn_motor_data_controler import TF_NN_MOTOR_DATA_CONTROLER

class TF_NN_MOTOR_COM:  
    ####PUBLIC
    motor_status_list = None
    motor_size = 16
    
    ####PRIVATE
    CTR_DLC                     =  '*'
    CONTROL_INST_SET            =  'S'
    CONTROL_INST_GET            =  'G'
    CONTROL_INST_INFO           =  '-'
    CONTROL_INST_WARN           =  '~'
    CONTROL_INST_FATAL          =  '!'

    CONTROL_FUNC_POSITION       =  'P'
    CONTROL_FUNC_SPEED          =  'S'
    CONTROL_FUNC_LOAD           =  'L'
    CONTROL_FUNC_VOLTAGE        =  'V'
    CONTROL_FUNC_TEMPERATURE    =  'T'
    CONTROL_FUNC_TORQUE         =  'Q'

    CONTROL_FUNC_POSITION_HARD  =  'Z'
    CONTROL_FUNC_POSITION_SOFT  =  'X'
    
    ####PRIVATE
    motor_status_position       = 'position'
    motor_status_speed          = 'speed'
    motor_status_load           = 'load'
    motor_status_voltage        = 'voltage'
    motor_status_temperature    = 'temperature'
    motor_status_torque         = 'torque'

    msg_header  = None
    msg_inst    = None
    msg_func    = None
    msg_id      = None
    msg_data    = None
    
    motor_status_controler_ = TF_NN_MOTOR_DATA_CONTROLER()
    def get_motor_msg(self, motor_id, func, data, inst='SET'):
        msg_id = motor_id
        msg_data = data
        
        if   inst == 'SET':
            msg_inst = self.CONTROL_INST_SET
        elif inst == 'GET':
            msg_inst = self.CONTROL_INST_GET
            
        if func == self.motor_status_position:
            msg_func = self.CONTROL_FUNC_POSITION
        elif func == self.motor_status_speed:
            msg_func = self.CONTROL_FUNC_SPEED
        elif func == self.motor_status_load:
            msg_func = self.CONTROL_FUNC_LOAD
        elif func == self.motor_status_voltage:
            msg_func = self.CONTROL_FUNC_VOLTAGE
        elif func == self.motor_status_temperature:
            msg_func = self.CONTROL_FUNC_TEMPERATURE
        elif func == self.motor_status_torque:
            msg_func = self.CONTROL_FUNC_TORQUE
        else:
            return ""
            
        return self.generate_msg([msg_inst, msg_func, msg_id, msg_data])
    
    def get_motor_status(self, motor_id, data_name):
        return self.motor_status_controler_.get_data(motor_id, data_name)
    
    def set_motor_msg(self, msg):
        motor_inst, motor_func, motor_id, motor_data = self.parse_msg(msg)
        if not (motor_inst == self.CONTROL_INST_INFO or motor_inst == self.CONTROL_INST_WARN or motor_inst == self.CONTROL_INST_FATAL):
            return
        if int(motor_id) > self.motor_size:
            return
        if motor_func == self.CONTROL_FUNC_POSITION:
            if int(motor_data) > 1023:
                return
            self.motor_status_controler_.update_data(motor_id, self.motor_status_position, int(motor_data))
        if motor_func == self.CONTROL_FUNC_SPEED:
            if int(motor_data) > 1023:
                return
            self.motor_status_controler_.update_data(motor_id, self.motor_status_speed, int(motor_data))
        if motor_func == self.CONTROL_FUNC_LOAD:
            if int(motor_data) > 1023:
                return
            self.motor_status_controler_.update_data(motor_id, self.motor_status_load, int(motor_data))
        if motor_func == self.CONTROL_FUNC_VOLTAGE:
            if int(motor_data) > 256:
                return
            self.motor_status_controler_.update_data(motor_id, self.motor_status_voltage, int(motor_data))
        if motor_func == self.CONTROL_FUNC_TEMPERATURE:
            if int(motor_data) > 128:
                return
            self.motor_status_controler_.update_data(motor_id, self.motor_status_temperature, int(motor_data))
        self.motor_status_list = self.motor_status_controler_.motor_status_list
    
    def parse_msg(self, msg):
        print("{}".format(msg))
        msg_arr = msg.split(self.CTR_DLC)
        self.msg_header = msg_arr[0]
        self.msg_inst   = self.msg_header[0]
        self.msg_func   = self.msg_header[1]
        self.msg_id     = msg_arr[1]
        self.msg_data   = msg_arr[2]
        return self.msg_inst, self.msg_func, self.msg_id, self.msg_data
    
    def generate_msg(self, data):
        msg_inst = data[0]
        msg_func = data[1]
        msg_id = data[2]
        msg_data = data[3]
        msg = "{}{}{}{}{}{}".format(msg_inst, msg_func, self.CTR_DLC, msg_id, self.CTR_DLC, msg_data)
        return msg
    
    '''
    def __call__(self, msg):
        self.set_motor_msg(msg)
        
    def __call__(self, motor_id, data_name):
        return self.get_motor_status(motor_id, data_name)
    '''
    def __init__(self):
        pass
    
    def __del__(self):
        pass