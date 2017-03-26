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
##  树莓派Car有关的函数
##  2016-5-13 Richard@olive.fm
##
######################################################################################
import RPi.GPIO as GPIO
import time

LeftIn1= 2
LeftIn2= 3
LeftIn3= 27
LeftIn4= 22
RightIn1= 18
RightIn2= 23
RightIn3= 24
RightIn4= 25

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LeftIn1,GPIO.OUT)
    GPIO.setup(LeftIn2,GPIO.OUT)
    GPIO.setup(LeftIn3,GPIO.OUT)
    GPIO.setup(LeftIn4,GPIO.OUT)
    GPIO.setup(RightIn1,GPIO.OUT)
    GPIO.setup(RightIn2,GPIO.OUT)
    GPIO.setup(RightIn3,GPIO.OUT)
    GPIO.setup(RightIn4,GPIO.OUT)


def stop():
    GPIO.output(LeftIn1,False)
    GPIO.output(LeftIn2,False)
    GPIO.output(LeftIn3,False)
    GPIO.output(LeftIn4,False)
    GPIO.output(RightIn1,False)
    GPIO.output(RightIn2,False)
    GPIO.output(RightIn3,False)
    GPIO.output(RightIn4,False)

def forward():
    GPIO.output(LeftIn1,True)
    GPIO.output(LeftIn2,False)
    GPIO.output(LeftIn3,True)
    GPIO.output(LeftIn4,False)
    GPIO.output(RightIn1,False)
    GPIO.output(RightIn2,True)
    GPIO.output(RightIn3,False)
    GPIO.output(RightIn4,True)

def back():
    GPIO.output(LeftIn1,False)
    GPIO.output(LeftIn2,True)
    GPIO.output(LeftIn3,False)
    GPIO.output(LeftIn4,True)
    GPIO.output(RightIn1,True)
    GPIO.output(RightIn2,False)
    GPIO.output(RightIn3,True)
    GPIO.output(RightIn4,False)

def right():
    GPIO.output(LeftIn1,False)
    GPIO.output(LeftIn2,True)
    GPIO.output(LeftIn3,False)
    GPIO.output(LeftIn4,True)
    GPIO.output(RightIn1,False)
    GPIO.output(RightIn2,True)
    GPIO.output(RightIn3,False)
    GPIO.output(RightIn4,True)

def left():
    GPIO.output(LeftIn1,True)
    GPIO.output(LeftIn2,False)
    GPIO.output(LeftIn3,True)
    GPIO.output(LeftIn4,False)
    GPIO.output(RightIn1,True)
    GPIO.output(RightIn2,False)
    GPIO.output(RightIn3,True)
    GPIO.output(RightIn4,False)

