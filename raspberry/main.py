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
##  树莓派接受信息，并处理的Main程序
##  2016-5-13 Richard@olive.fm
##
######################################################################################

import socket
import binascii
import pgio_car as car
import raspberry

car.init()
car.stop()

address = ('', 5858)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
s.bind(address)  


print "Listening on port 5858..."
while True:
    data, addr = s.recvfrom(2048)
    if not data:  
        print "client has exist"
        break      
    print "[received] ",data ," from ",addr

    if(data=="car:left"):
        car.left()
        print "[control] car to left"

    elif(data=="car:right"):
        car.right()
        print "[control] car to right"

    elif(data=="car:forward"):
        car.forward()
        print "[control] car to forward"

    elif(data=="car:back"):
        car.back()
        print "[control] car to back"

    elif(data=="car:stop"):
        car.stop()
        print "[control] car to stop"

    elif(data=="board:cpu_temperature"):
        send_str='board:cpu_temperature='+raspberry.get_cpu_temp()
        s.sendto(send_str,addr)
        
        

    elif(data=="board:gpu_temperature"):
        send_str='board:gpu_temperature='+raspberry.get_gpu_temp()
        s.sendto(send_str,addr)
        print "[send] ", send_str, "to", addr

    elif(data=="board:time"):
        send_str='board:time='+raspberry.get_time_now()
        s.sendto(send_str,addr)
        print "[send] ", send_str, "to", addr

    elif(data=="board:ip_info"):
        send_str='board:ip_info='+raspberry.get_ip_info()
        s.sendto(send_str,addr)
        print "[send] ", send_str, "to", addr

    elif(data=="board:mem_info"):
        free,total =raspberry.get_mem_info()
        send_str='board:mem_info='+free+","+total
        s.sendto(send_str,addr)
        print "[send] ", send_str, "to", addr

s.close()