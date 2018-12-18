#!/usr/bin/env python
# license removed for brevity


class MOTOR_ADJUST:
    ####PUBLIC
    cmd_func_load = 'load'
    cmd_func_speed = 'speed'
    cmd_func_position = 'position'
    cmd_func_temperature = 'temperature'
    cmd_func_torque = 'torque'
    
    cmd_inst_set = 'SET'
    cmd_inst_get = 'GET'
    
    motor_parameter_list = {}
    
    ####PUBLIC  
    MOTOR_MOUTH_ID                          = 1
    MOTOR_MOUTH_ANGLE_MIN                   = 427
    MOTOR_MOUTH_ANGLE_MAX                   = 768
    MOTOR_MOUTH_LOAD_LIMIT_MAX              = 1023
    MOTOR_MOUTH_SPEED_MIN                   = 1
    MOTOR_MOUTH_SPEED_MAX                   = 1023
    
    MOTOR_MOUTH_INIT_ANGLE                  = 512
    MOTOR_MOUTH_INIT_LOAD_LIMIT             = 102
    MOTOR_MOUTH_INIT_SPEED                  = 10
    MOTOR_MOUTH_INIT_TORQUE                 = 1
    
    def motor_mouth_init(self):
        self.motor_parameter_list[str(self.MOTOR_MOUTH_ID)] = {
            'angle_min' : self.MOTOR_MOUTH_ANGLE_MIN, 
            'angle_max' : self.MOTOR_MOUTH_ANGLE_MAX, 
            'load_limit_max' : self.MOTOR_MOUTH_LOAD_LIMIT_MAX, 
            'speed_min' : self.MOTOR_MOUTH_SPEED_MIN, 
            'speed_max' : self.MOTOR_MOUTH_SPEED_MAX
        }
        init_list = []
        init_data = [self.MOTOR_MOUTH_ID, self.cmd_func_torque, self.MOTOR_MOUTH_INIT_TORQUE, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_MOUTH_ID, self.cmd_func_load, self.MOTOR_MOUTH_INIT_LOAD_LIMIT, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_MOUTH_ID, self.cmd_func_speed, self.MOTOR_MOUTH_INIT_SPEED, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_MOUTH_ID, self.cmd_func_position, self.MOTOR_MOUTH_INIT_ANGLE, self.cmd_inst_set]
        init_list.append(init_data)
        return init_list
    
    MOTOR_NECK_VERTICAL_ID                  = 2
    MOTOR_NECK_VERTICAL_ANGLE_MIN           = 410
    MOTOR_NECK_VERTICAL_ANGLE_MAX           = 819
    MOTOR_NECK_VERTICAL_LOAD_LIMIT_MAX      = 1023
    MOTOR_NECK_VERTICAL_SPEED_MIN           = 1
    MOTOR_NECK_VERTICAL_SPEED_MAX           = 1023
    
    MOTOR_NECK_VERTICAL_INIT_ANGLE          = 512
    MOTOR_NECK_VERTICAL_INIT_LOAD_LIMIT     = 102
    MOTOR_NECK_VERTICAL_INIT_SPEED          = 10
    MOTOR_NECK_VERTICAL_INIT_TORQUE         = 1
    def motor_neck_vertical_init(self):
        self.motor_parameter_list[str(self.MOTOR_NECK_VERTICAL_ID)] = {
            'angle_min' : self.MOTOR_NECK_VERTICAL_ANGLE_MIN, 
            'angle_max' : self.MOTOR_NECK_VERTICAL_ANGLE_MAX, 
            'load_limit_max' : self.MOTOR_NECK_VERTICAL_LOAD_LIMIT_MAX, 
            'speed_min' : self.MOTOR_NECK_VERTICAL_SPEED_MIN, 
            'speed_max' : self.MOTOR_NECK_VERTICAL_SPEED_MAX
        }
        init_list = []
        init_data = [self.MOTOR_NECK_VERTICAL_ID, self.cmd_func_torque, self.MOTOR_NECK_VERTICAL_INIT_TORQUE, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_NECK_VERTICAL_ID, self.cmd_func_load, self.MOTOR_NECK_VERTICAL_INIT_LOAD_LIMIT, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_NECK_VERTICAL_ID, self.cmd_func_speed, self.MOTOR_NECK_VERTICAL_INIT_SPEED, self.cmd_inst_set]
        init_list.append(init_data)
        #init_data = [self.MOTOR_NECK_VERTICAL_ID, self.cmd_func_position, self.MOTOR_NECK_VERTICAL_INIT_ANGLE, self.cmd_inst_set]
        #init_list.append(init_data)
        return init_list
    
    MOTOR_NECK_HORIZON_ID                   = 3
    MOTOR_NECK_HORIZON_ANGLE_MIN            = 290
    MOTOR_NECK_HORIZON_ANGLE_MAX            = 734
    MOTOR_NECK_HORIZON_LOAD_LIMIT_MAX       = 1023
    MOTOR_NECK_HORIZON_SPEED_MIN            = 1
    MOTOR_NECK_HORIZON_SPEED_MAX            = 1023
    
    MOTOR_NECK_HORIZON_INIT_ANGLE           = 512
    MOTOR_NECK_HORIZON_INIT_LOAD_LIMIT      = 102
    MOTOR_NECK_HORIZON_INIT_SPEED           = 10
    MOTOR_NECK_HORIZON_INIT_TORQUE          = 1
    def motor_neck_horizon_init(self):
        self.motor_parameter_list[str(self.MOTOR_NECK_HORIZON_ID)] = {
            'angle_min' : self.MOTOR_NECK_HORIZON_ANGLE_MIN, 
            'angle_max' : self.MOTOR_NECK_HORIZON_ANGLE_MAX, 
            'load_limit_max' : self.MOTOR_NECK_HORIZON_LOAD_LIMIT_MAX, 
            'speed_min' : self.MOTOR_NECK_HORIZON_SPEED_MIN, 
            'speed_max' : self.MOTOR_NECK_HORIZON_SPEED_MAX
        }
        init_list = []
        init_data = [self.MOTOR_NECK_HORIZON_ID, self.cmd_func_torque, self.MOTOR_NECK_HORIZON_INIT_TORQUE, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_NECK_HORIZON_ID, self.cmd_func_load, self.MOTOR_NECK_HORIZON_INIT_LOAD_LIMIT, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_NECK_HORIZON_ID, self.cmd_func_speed, self.MOTOR_NECK_HORIZON_INIT_SPEED, self.cmd_inst_set]
        init_list.append(init_data)
        #init_data = [self.MOTOR_NECK_HORIZON_ID, self.cmd_func_position, self.MOTOR_NECK_HORIZON_INIT_ANGLE, self.cmd_inst_set]
        #init_list.append(init_data)
        return init_list
    
    MOTOR_LEFT_THIGH_ID                     = 4
    MOTOR_LEFT_THIGH_ANGLE_MIN              = 205
    MOTOR_LEFT_THIGH_ANGLE_MAX              = 819
    MOTOR_LEFT_THIGH_LOAD_LIMIT_MAX         = 1023
    MOTOR_LEFT_THIGH_SPEED_MIN              = 1
    MOTOR_LEFT_THIGH_SPEED_MAX              = 1023
    
    MOTOR_LEFT_THIGH_INIT_ANGLE             = 512
    MOTOR_LEFT_THIGH_INIT_LOAD_LIMIT        = 102
    MOTOR_LEFT_THIGH_INIT_SPEED             = 10
    MOTOR_LEFT_THIGH_INIT_TORQUE            = 1
    def motor_left_thigh_init(self):
        self.motor_parameter_list[str(self.MOTOR_LEFT_THIGH_ID)] = {
            'angle_min' : self.MOTOR_LEFT_THIGH_ANGLE_MIN, 
            'angle_max' : self.MOTOR_LEFT_THIGH_ANGLE_MAX, 
            'load_limit_max' : self.MOTOR_LEFT_THIGH_LOAD_LIMIT_MAX, 
            'speed_min' : self.MOTOR_LEFT_THIGH_SPEED_MIN, 
            'speed_max' : self.MOTOR_LEFT_THIGH_SPEED_MAX
        }
        init_list = []
        init_data = [self.MOTOR_LEFT_THIGH_ID, self.cmd_func_torque, self.MOTOR_LEFT_THIGH_INIT_TORQUE, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_LEFT_THIGH_ID, self.cmd_func_load, self.MOTOR_LEFT_THIGH_INIT_LOAD_LIMIT, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_LEFT_THIGH_ID, self.cmd_func_speed, self.MOTOR_LEFT_THIGH_INIT_SPEED, self.cmd_inst_set]
        init_list.append(init_data)
        #init_data = [self.MOTOR_LEFT_THIGH_ID, self.cmd_func_position, self.MOTOR_LEFT_THIGH_INIT_ANGLE, self.cmd_inst_set]
        #init_list.append(init_data)
        return init_list
    
    MOTOR_LEFT_CALF_ID                      = 5
    MOTOR_LEFT_CALF_ANGLE_MIN               = 188
    MOTOR_LEFT_CALF_ANGLE_MAX               = 700
    MOTOR_LEFT_CALF_LOAD_LIMIT_MAX          = 1023
    MOTOR_LEFT_CALF_SPEED_MIN               = 1
    MOTOR_LEFT_CALF_SPEED_MAX               = 1023
    
    MOTOR_LEFT_CALF_INIT_ANGLE              = 512
    MOTOR_LEFT_CALF_INIT_LOAD_LIMIT         = 102
    MOTOR_LEFT_CALF_INIT_SPEED              = 10
    MOTOR_LEFT_CALF_INIT_TORQUE             = 1
    def motor_left_calf_init(self):
        self.motor_parameter_list[str(self.MOTOR_LEFT_CALF_ID)] = {
            'angle_min' : self.MOTOR_LEFT_CALF_ANGLE_MIN, 
            'angle_max' : self.MOTOR_LEFT_CALF_ANGLE_MIN, 
            'load_limit_max' : self.MOTOR_LEFT_CALF_LOAD_LIMIT_MAX, 
            'speed_min' : self.MOTOR_LEFT_CALF_SPEED_MIN, 
            'speed_max' : self.MOTOR_LEFT_CALF_SPEED_MAX
        }
        init_list = []
        init_data = [self.MOTOR_LEFT_CALF_ID, self.cmd_func_torque, self.MOTOR_LEFT_CALF_INIT_TORQUE, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_LEFT_CALF_ID, self.cmd_func_load, self.MOTOR_LEFT_CALF_INIT_LOAD_LIMIT, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_LEFT_CALF_ID, self.cmd_func_speed, self.MOTOR_LEFT_CALF_INIT_SPEED, self.cmd_inst_set]
        init_list.append(init_data)
        #init_data = [self.MOTOR_LEFT_CALF_ID, self.cmd_func_position, self.MOTOR_LEFT_CALF_INIT_ANGLE, self.cmd_inst_set]
        #init_list.append(init_data)
        return init_list
    
    MOTOR_LEFT_ANKLE_ID                     = 6
    MOTOR_LEFT_ANKLE_ANGLE_MIN              = 376
    MOTOR_LEFT_ANKLE_ANGLE_MAX              = 802
    MOTOR_LEFT_ANKLE_LOAD_LIMIT_MAX         = 1023
    MOTOR_LEFT_ANKLE_SPEED_MIN              = 1
    MOTOR_LEFT_ANKLE_SPEED_MAX              = 1023
    
    MOTOR_LEFT_ANKLE_INIT_ANGLE             = 512
    MOTOR_LEFT_ANKLE_INIT_LOAD_LIMIT        = 102
    MOTOR_LEFT_ANKLE_INIT_SPEED             = 10
    MOTOR_LEFT_ANKLE_INIT_TORQUE            = 1
    def motor_left_ankle_init(self):
        self.motor_parameter_list[str(self.MOTOR_LEFT_ANKLE_ID)] = {
            'angle_min' : self.MOTOR_LEFT_ANKLE_ANGLE_MIN, 
            'angle_max' : self.MOTOR_LEFT_ANKLE_ANGLE_MAX, 
            'load_limit_max' : self.MOTOR_LEFT_ANKLE_LOAD_LIMIT_MAX, 
            'speed_min' : self.MOTOR_LEFT_ANKLE_SPEED_MIN, 
            'speed_max' : self.MOTOR_LEFT_ANKLE_SPEED_MAX
        }
        init_list = []
        init_data = [self.MOTOR_LEFT_ANKLE_ID, self.cmd_func_torque, self.MOTOR_LEFT_ANKLE_INIT_TORQUE, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_LEFT_ANKLE_ID, self.cmd_func_load, self.MOTOR_LEFT_ANKLE_INIT_LOAD_LIMIT, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_LEFT_ANKLE_ID, self.cmd_func_speed, self.MOTOR_LEFT_ANKLE_INIT_SPEED, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_LEFT_ANKLE_ID, self.cmd_func_position, self.MOTOR_LEFT_ANKLE_INIT_ANGLE, self.cmd_inst_set]
        init_list.append(init_data)
        return init_list
    
    MOTOR_RIGHT_THIGH_ID                    = 7
    MOTOR_RIGHT_THIGH_ANGLE_MIN             = 205
    MOTOR_RIGHT_THIGH_ANGLE_MAX             = 819
    MOTOR_RIGHT_THIGH_LOAD_LIMIT_MAX        = 1023
    MOTOR_RIGHT_THIGH_SPEED_MIN             = 1
    MOTOR_RIGHT_THIGH_SPEED_MAX             = 1023
    
    MOTOR_RIGHT_THIGH_INIT_ANGLE            = 512
    MOTOR_RIGHT_THIGH_INIT_LOAD_LIMIT       = 102
    MOTOR_RIGHT_THIGH_INIT_SPEED            = 10
    MOTOR_RIGHT_THIGH_INIT_TORQUE           = 1
    def motor_right_thigh_init(self):
        self.motor_parameter_list[str(self.MOTOR_RIGHT_THIGH_ID)] = {
            'angle_min' : self.MOTOR_RIGHT_THIGH_ANGLE_MIN, 
            'angle_max' : self.MOTOR_RIGHT_THIGH_ANGLE_MAX, 
            'load_limit_max' : self.MOTOR_RIGHT_THIGH_LOAD_LIMIT_MAX, 
            'speed_min' : self.MOTOR_RIGHT_THIGH_SPEED_MIN, 
            'speed_max' : self.MOTOR_RIGHT_THIGH_SPEED_MAX
        }
        init_list = []
        init_data = [self.MOTOR_RIGHT_THIGH_ID, self.cmd_func_torque, self.MOTOR_RIGHT_THIGH_INIT_TORQUE, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_RIGHT_THIGH_ID, self.cmd_func_load, self.MOTOR_RIGHT_THIGH_INIT_LOAD_LIMIT, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_RIGHT_THIGH_ID, self.cmd_func_speed, self.MOTOR_RIGHT_THIGH_INIT_SPEED, self.cmd_inst_set]
        init_list.append(init_data)
        #init_data = [self.MOTOR_RIGHT_THIGH_ID, self.cmd_func_position, self.MOTOR_RIGHT_THIGH_INIT_ANGLE, self.cmd_inst_set]
        #init_list.append(init_data)
        return init_list
    
    MOTOR_RIGHT_CALF_ID                     = 8
    MOTOR_RIGHT_CALF_ANGLE_MIN              = 324
    MOTOR_RIGHT_CALF_ANGLE_MAX              = 836
    MOTOR_RIGHT_CALF_LOAD_LIMIT_MAX         = 1023
    MOTOR_RIGHT_CALF_SPEED_MIN              = 1
    MOTOR_RIGHT_CALF_SPEED_MAX              = 1023
    
    MOTOR_RIGHT_CALF_INIT_ANGLE             = 512
    MOTOR_RIGHT_CALF_INIT_LOAD_LIMIT        = 102
    MOTOR_RIGHT_CALF_INIT_SPEED             = 10
    MOTOR_RIGHT_CALF_INIT_TORQUE            = 1
    def motor_right_calf_init(self):
        self.motor_parameter_list[str(self.MOTOR_RIGHT_CALF_ID)] = {
            'angle_min' : self.MOTOR_RIGHT_CALF_ANGLE_MIN, 
            'angle_max' : self.MOTOR_RIGHT_CALF_ANGLE_MAX, 
            'load_limit_max' : self.MOTOR_RIGHT_CALF_LOAD_LIMIT_MAX, 
            'speed_min' : self.MOTOR_RIGHT_CALF_SPEED_MIN, 
            'speed_max' : self.MOTOR_RIGHT_CALF_SPEED_MAX
        }
        init_list = []
        init_data = [self.MOTOR_RIGHT_CALF_ID, self.cmd_func_torque, self.MOTOR_RIGHT_CALF_INIT_TORQUE, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_RIGHT_CALF_ID, self.cmd_func_load, self.MOTOR_RIGHT_CALF_INIT_LOAD_LIMIT, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_RIGHT_CALF_ID, self.cmd_func_speed, self.MOTOR_RIGHT_CALF_INIT_SPEED, self.cmd_inst_set]
        init_list.append(init_data)
        #init_data = [self.MOTOR_RIGHT_CALF_ID, self.cmd_func_position, self.MOTOR_RIGHT_CALF_INIT_ANGLE, self.cmd_inst_set]
        #init_list.append(init_data)
        return init_list
    
    MOTOR_RIGHT_ANKLE_ID                    = 9
    MOTOR_RIGHT_ANKLE_ANGLE_MIN             = 222
    MOTOR_RIGHT_ANKLE_ANGLE_MAX             = 649
    MOTOR_RIGHT_ANKLE_LOAD_LIMIT_MAX        = 1023
    MOTOR_RIGHT_ANKLE_SPEED_MIN             = 1
    MOTOR_RIGHT_ANKLE_SPEED_MAX             = 1023
    
    MOTOR_RIGHT_ANKLE_INIT_ANGLE            = 512
    MOTOR_RIGHT_ANKLE_INIT_LOAD_LIMIT       = 102
    MOTOR_RIGHT_ANKLE_INIT_SPEED            = 10
    MOTOR_RIGHT_ANKLE_INIT_TORQUE           = 1
    def motor_right_ankle_init(self):
        self.motor_parameter_list[str(self.MOTOR_RIGHT_ANKLE_ID)] = {
            'angle_min' : self.MOTOR_RIGHT_ANKLE_ANGLE_MIN, 
            'angle_max' : self.MOTOR_RIGHT_ANKLE_ANGLE_MAX, 
            'load_limit_max' : self.MOTOR_RIGHT_ANKLE_LOAD_LIMIT_MAX, 
            'speed_min' : self.MOTOR_RIGHT_ANKLE_SPEED_MIN, 
            'speed_max' : self.MOTOR_RIGHT_ANKLE_SPEED_MAX
        }
        init_list = []
        init_data = [self.MOTOR_RIGHT_ANKLE_ID, self.cmd_func_torque, self.MOTOR_RIGHT_ANKLE_INIT_TORQUE, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_RIGHT_ANKLE_ID, self.cmd_func_load, self.MOTOR_RIGHT_ANKLE_INIT_LOAD_LIMIT, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_RIGHT_ANKLE_ID, self.cmd_func_speed, self.MOTOR_RIGHT_ANKLE_INIT_SPEED, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_RIGHT_ANKLE_ID, self.cmd_func_position, self.MOTOR_RIGHT_ANKLE_INIT_ANGLE, self.cmd_inst_set]
        init_list.append(init_data)
        return init_list
    
    MOTOR_ASS_ID                            = 11
    MOTOR_ASS_MIN                           = 256
    MOTOR_ASS_MAX                           = 768
    MOTOR_ASS_LOAD_LIMIT_MAX                = 1023
    MOTOR_ASS_SPEED_MIN                     = 1
    MOTOR_ASS_SPEED_MAX                     = 1023
    
    MOTOR_ASS_INIT_ANGLE                    = 512
    MOTOR_ASS_INIT_LOAD_LIMIT               = 102
    MOTOR_ASS_INIT_SPEED                    = 10
    MOTOR_ASS_INIT_TORQUE                   = 1
    def motor_ass_init(self):
        self.motor_parameter_list[str(self.MOTOR_ASS_ID)] = {
            'angle_min' : self.MOTOR_ASS_MIN, 
            'angle_max' : self.MOTOR_ASS_MAX, 
            'load_limit_max' : self.MOTOR_ASS_LOAD_LIMIT_MAX, 
            'speed_min' : self.MOTOR_ASS_SPEED_MIN, 
            'speed_max' : self.MOTOR_ASS_SPEED_MAX
        }
        init_list = []
        init_data = [self.MOTOR_ASS_ID, self.cmd_func_torque, self.MOTOR_ASS_INIT_TORQUE, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_ASS_ID, self.cmd_func_load, self.MOTOR_ASS_INIT_LOAD_LIMIT, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_ASS_ID, self.cmd_func_speed, self.MOTOR_ASS_INIT_SPEED, self.cmd_inst_set]
        init_list.append(init_data)
        #init_data = [self.MOTOR_ASS_ID, self.cmd_func_position, self.MOTOR_ASS_INIT_ANGLE, self.cmd_inst_set]
        #init_list.append(init_data)
        return init_list
    
    MOTOR_TAIL_1_ID                         = 12
    MOTOR_TAIL_1_MIN                        = 205
    MOTOR_TAIL_1_MAX                        = 819
    MOTOR_TAIL_1_LOAD_LIMIT_MAX             = 1023
    MOTOR_TAIL_1_SPEED_MIN                  = 1
    MOTOR_TAIL_1_SPEED_MAX                  = 1023
    
    MOTOR_TAIL_1_INIT_ANGLE                 = 512
    MOTOR_TAIL_1_INIT_LOAD_LIMIT            = 102
    MOTOR_TAIL_1_INIT_SPEED                 = 10
    MOTOR_TAIL_1_INIT_TORQUE                = 1
    def motor_tail_1_init(self):
        self.motor_parameter_list[str(self.MOTOR_TAIL_1_ID)] = {
            'angle_min' : self.MOTOR_TAIL_1_MIN, 
            'angle_max' : self.MOTOR_TAIL_1_MAX, 
            'load_limit_max' : self.MOTOR_TAIL_1_LOAD_LIMIT_MAX, 
            'speed_min' : self.MOTOR_TAIL_1_SPEED_MIN, 
            'speed_max' : self.MOTOR_TAIL_1_SPEED_MAX
        }
        init_list = []
        init_data = [self.MOTOR_TAIL_1_ID, self.cmd_func_torque, self.MOTOR_TAIL_1_INIT_TORQUE, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_TAIL_1_ID, self.cmd_func_load, self.MOTOR_TAIL_1_INIT_LOAD_LIMIT, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_TAIL_1_ID, self.cmd_func_speed, self.MOTOR_TAIL_1_INIT_SPEED, self.cmd_inst_set]
        init_list.append(init_data)
        #init_data = [self.MOTOR_TAIL_1_ID, self.cmd_func_position, self.MOTOR_TAIL_1_INIT_ANGLE, self.cmd_inst_set]
        #init_list.append(init_data)
        return init_list
    
    MOTOR_TAIL_2_ID                         = 13
    MOTOR_TAIL_2_MIN                        = 205
    MOTOR_TAIL_2_MAX                        = 819
    MOTOR_TAIL_2_LOAD_LIMIT_MAX             = 1023
    MOTOR_TAIL_2_SPEED_MIN                  = 1
    MOTOR_TAIL_2_SPEED_MAX                  = 1023
    
    MOTOR_TAIL_2_INIT_ANGLE                 = 512
    MOTOR_TAIL_2_INIT_LOAD_LIMIT            = 102
    MOTOR_TAIL_2_INIT_SPEED                 = 10
    MOTOR_TAIL_2_INIT_TORQUE                = 1
    def motor_tail_2_init(self):
        self.motor_parameter_list[str(self.MOTOR_TAIL_2_ID)] = {
            'angle_min' : self.MOTOR_TAIL_2_MIN, 
            'angle_max' : self.MOTOR_TAIL_2_MAX, 
            'load_limit_max' : self.MOTOR_TAIL_2_LOAD_LIMIT_MAX, 
            'speed_min' : self.MOTOR_TAIL_2_SPEED_MIN, 
            'speed_max' : self.MOTOR_TAIL_2_SPEED_MAX
        }
        init_list = []
        init_data = [self.MOTOR_TAIL_2_ID, self.cmd_func_torque, self.MOTOR_TAIL_2_INIT_TORQUE, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_TAIL_2_ID, self.cmd_func_load, self.MOTOR_TAIL_2_INIT_LOAD_LIMIT, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_TAIL_2_ID, self.cmd_func_speed, self.MOTOR_TAIL_2_INIT_SPEED, self.cmd_inst_set]
        init_list.append(init_data)
        #init_data = [self.MOTOR_TAIL_2_ID, self.cmd_func_position, self.MOTOR_TAIL_2_INIT_ANGLE, self.cmd_inst_set]
        #init_list.append(init_data)
        return init_list
    
    MOTOR_TAIL_3_ID                         = 14
    MOTOR_TAIL_3_MIN                        = 205
    MOTOR_TAIL_3_MAX                        = 819
    MOTOR_TAIL_3_LOAD_LIMIT_MAX             = 1023
    MOTOR_TAIL_3_SPEED_MIN                  = 1
    MOTOR_TAIL_3_SPEED_MAX                  = 1023
    
    MOTOR_TAIL_3_INIT_ANGLE                 = 512
    MOTOR_TAIL_3_INIT_LOAD_LIMIT            = 102
    MOTOR_TAIL_3_INIT_SPEED                 = 10
    MOTOR_TAIL_3_INIT_TORQUE                = 1
    def motor_tail_3_init(self):
        self.motor_parameter_list[str(self.MOTOR_TAIL_3_ID)] = {
            'angle_min' : self.MOTOR_TAIL_3_MIN, 
            'angle_max' : self.MOTOR_TAIL_3_MAX, 
            'load_limit_max' : self.MOTOR_TAIL_3_LOAD_LIMIT_MAX, 
            'speed_min' : self.MOTOR_TAIL_3_SPEED_MIN, 
            'speed_max' : self.MOTOR_TAIL_3_SPEED_MAX
        }
        init_list = []
        init_data = [self.MOTOR_TAIL_3_ID, self.cmd_func_torque, self.MOTOR_TAIL_3_INIT_TORQUE, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_TAIL_3_ID, self.cmd_func_load, self.MOTOR_TAIL_3_INIT_LOAD_LIMIT, self.cmd_inst_set]
        init_list.append(init_data)
        init_data = [self.MOTOR_TAIL_3_ID, self.cmd_func_speed, self.MOTOR_TAIL_3_INIT_SPEED, self.cmd_inst_set]
        init_list.append(init_data)
        #init_data = [self.MOTOR_TAIL_3_ID, self.cmd_func_position, self.MOTOR_TAIL_3_INIT_ANGLE, self.cmd_inst_set]
        #init_list.append(init_data)
        return init_list

    ####PRIVATE
    ver = "1.0" 
    
    def adjust(self, cmd_list):
        for i in cmd_list:
            if i[3] == self.cmd_inst_get:
                continue
            if i[1] == self.cmd_func_position:
                i[2] = min(i[2], self.motor_parameter_list[str(i[0])]['angle_max'])
                i[2] = max(i[2], self.motor_parameter_list[str(i[0])]['angle_min'])
            if i[1] == self.cmd_func_load:
                i[2] = min(i[2], self.motor_parameter_list[str(i[0])]['load_limit_max'])
            if i[1] == self.cmd_func_speed:
                i[2] = min(i[2], self.motor_parameter_list[str(i[0])]['speed_max'])
                i[2] = max(i[2], self.motor_parameter_list[str(i[0])]['speed_min'])
        return cmd_list
    
    def init(self):
        init_list = []
        init_list.extend(self.motor_mouth_init())
        init_list.extend(self.motor_neck_vertical_init())
        init_list.extend(self.motor_neck_horizon_init())
        init_list.extend(self.motor_left_thigh_init())
        init_list.extend(self.motor_left_calf_init())
        init_list.extend(self.motor_left_ankle_init())
        init_list.extend(self.motor_right_thigh_init())
        init_list.extend(self.motor_right_calf_init())
        init_list.extend(self.motor_right_ankle_init())
        init_list.extend(self.motor_ass_init())
        init_list.extend(self.motor_tail_1_init())
        init_list.extend(self.motor_tail_2_init())
        init_list.extend(self.motor_tail_3_init())
        
        return self.adjust(init_list)
            
    def __init__(self):
        self.init()

    def __del__(self):
        pass


