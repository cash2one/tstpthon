#!/usr/bin/env python
# -*- coding:UTF-8 -*-

######################################################################################
##
##  Copyright (c) 2009-2016, Olive Software.
##  All rights reserved.
##  Redistribution and use in source and binary forms, with or without
##  modification, are permitted provided that the following conditions are met:
##
##     * Redistributions of source code must retain the above copyright
##       notice, this list of conditions and the following disclaimer.
##     * Redistributions in binary form must reproduce the above copyright
##       notice, this list of conditions and the following disclaimer in the
##       documentation and/or other materials provided with the distribution.
##     * Neither the name of the Olive nor the
##       names of its contributors may be used to endorse or promote products
##       derived from this software without specific prior written permission.
##
##  THIS SOFTWARE IS PROVIDED BY OLIVE AND CONTRIBUTORS "AS IS" AND ANY EXPRESS
##  OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
##  OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
##  IN NO EVENT SHALL OLIVE AND CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
##  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
##  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;LOSS OF USE, DATA,
##  OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
##  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
##  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
##  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##
##  树莓派主板有关的函数
##  2016-5-13 Richard@olive.fm
##
######################################################################################
from datetime import *
import commands

def get_cpu_temp():
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C'

def get_gpu_temp():
    tmp = commands.getoutput('vcgencmd measure_temp|awk -F= \'{print $2}\'').replace('\'C','')
    gpu = float(tmp)
    return '{:.2f}'.format( gpu ) + ' C'

def get_time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_ip_info():
    return commands.getoutput('ifconfig wlan0|grep inet|awk -Faddr: \'{print $2}\'|awk \'{print $1}\'')

def get_mem_info():
    total= commands.getoutput('free -m|grep Mem:|awk \'{print $2}\'')  
    free = commands.getoutput('free -m|grep cache:|awk \'{print $4}\'')
    return free,total