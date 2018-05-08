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

from time import sleep

# Accelerometer
#==================================================================

accel = Adafruit_ADXL345.ADXL345()

# Gyroscope
#==================================================================

def getSignedNumber(number):
    if number & (1 << 15):
        return number | ~65535
    else:
        return number & 65535

i2c_bus=smbus.SMBus(1)
i2c_address=0x69

i2c_bus.write_byte_data(i2c_address,0x20,0x0F)
i2c_bus.write_byte_data(i2c_address,0x23,0x20)

# Magnetometer
#==================================================================

bus = smbus.SMBus(1)
addrHMC = 0x1e

def init_imu():
    bus.write_byte_data(addrHMC, 0, 0b01110000)  # Set to 8 samples @ 15Hz
    bus.write_byte_data(addrHMC, 1, 0b00100000)  # 1.3 gain LSb / Gauss 1090 (default)
    bus.write_byte_data(addrHMC, 2, 0b00000000)  # Continuous sampling

def read_word(address, adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val

def read_word_2c(address, adr):
    val = read_word(address, adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

init_imu()

#==================================================================

while True:
    # Accelerometer
    #==================================================================
    accx, accy, accz = accel.read()
    
    # Gyroscope
    #==================================================================
    
    i2c_bus.write_byte(i2c_address,0x28)
    X_L = i2c_bus.read_byte(i2c_address)
    i2c_bus.write_byte(i2c_address,0x29)
    X_H = i2c_bus.read_byte(i2c_address)
    X = X_H << 8 | X_L

    i2c_bus.write_byte(i2c_address,0x2A)
    Y_L = i2c_bus.read_byte(i2c_address)
    i2c_bus.write_byte(i2c_address,0x2B)
    Y_H = i2c_bus.read_byte(i2c_address)
    Y = Y_H << 8 | Y_L

    i2c_bus.write_byte(i2c_address,0x2C)
    Z_L = i2c_bus.read_byte(i2c_address)
    i2c_bus.write_byte(i2c_address,0x2D)
    Z_H = i2c_bus.read_byte(i2c_address)
    Z = Z_H << 8 | Z_L

    gyrox = getSignedNumber(X)
    gyroy = getSignedNumber(Y)
    gyroz = getSignedNumber(Z)
    
    # Magnetometer
    #==================================================================
    
    magx = read_word_2c(addrHMC, 3)
    magy = read_word_2c(addrHMC, 7)
    magz = read_word_2c(addrHMC, 5)
    
    # Altitude
    #==================================================================
    
    sensor = BMP085.BMP085()
    
    alti = sensor.read_altitude()
    
    #==================================================================
    
    print('ACC: x:{0},y:{1},z:{2}; GYRO: x:{3},y:{4},z:{5}; MAG: x:{6},y:{7},z:{8}; Alti: {9:0.2f}m'.format(accx/256.0, accy/256.0, accz/287.0, (gyrox*35.0)/1000.0, (gyroy*35.0)/1000.0, (gyroz*35.0)/1000.0, magx*0.92, magy*0.92, magz*0.92, alti))
    time.sleep(0.5)