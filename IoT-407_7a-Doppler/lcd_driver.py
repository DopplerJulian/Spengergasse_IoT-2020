'''
    I2C LCD1602 demo

    Author: shaoziyang
    Date:   2018.2

    http://www.micropython.org.cn

'''
from machine import I2C, Pin
from mp_i2c_lcd1602 import LCD1602
from time import sleep_ms

i2c = I2C(1, sda=Pin(21), scl=Pin(22))

LCD = LCD1602(i2c, 0x27)

LCD.print("hello world")

