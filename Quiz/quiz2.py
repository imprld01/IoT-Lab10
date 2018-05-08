import os
import sys
import math
import time
import smbus
import string
import thread
import random
import requests
import Adafruit_ADXL345
import Adafruit_BMP.BMP085 as BMP085

import numpy as np

from time import sleep

def lowpass(x, dt=1, RC=1):
    y = x
    alpha = dt / (RC + dt)
    
    for idx in range(1, x.shape[0]):
        y[idx] = alpha * x[idx] + (1 - alpha) * y[idx - 1]
        
    return y

def instLowpass(x, pasty, dt=1, RC=1):
   
    alpha = dt / (RC + dt)
    y = alpha * x + (1 - alpha) * pasty
        
    return y

accel = Adafruit_ADXL345.ADXL345()

first = True
past = 0.0

raw = np.array([])
filtered = np.array([])

while True:
    accx, _, _ = accel.read()
    if not first:
        newone = instLowpass(accx, past)
        first = False
    else: past = accx
    
    raw = np.append(raw, accx)
    filtered = np.append(filtered, newone)
    
    print('raw-x:{0}'.format(raw))
    print('filtered:{0}'.format(filtered))
    time.sleep(0.5)