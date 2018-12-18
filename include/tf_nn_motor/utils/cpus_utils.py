#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import psutil as psu
import numpy as np
from subprocess import Popen, PIPE

class CPUS_UTILS:
    #PUBLIC
    SOCKETS = 1
    CORES = 1
    THREADS = 1
    #PRIVATE
    CPU_INFO = {}
    
    def __init__(self):
        self.get_cpu_info()
        
    def __call__(self):
        return self.CORES
    
    def get_cpu_info(self):
        output = self.sys_call(["lscpu"])
        lines = output.split(os.linesep)
        for i in range(len(lines)):
            line = lines[i]
            vals = line.split(":")
            if len(vals) > 1:
                for j in range(len(vals)):
                    vals[j] = vals[j].strip()
                self.CPU_INFO[vals[0]] = vals[1]
        self.SOCKETS = int(self.CPU_INFO['Socket(s)'])
        self.CORES =  int(int(self.CPU_INFO['Core(s) per socket']) * self.SOCKETS)
        self.THREADS = int(int(self.CPU_INFO['Thread(s) per core']) * self.CORES)
        return self.CPU_INFO
        
    def sys_call(self, cmd):
        p = Popen(cmd, stdout=PIPE)
        output = p.stdout.read()
        return output
    
