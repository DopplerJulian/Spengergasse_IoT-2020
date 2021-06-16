from hcsr04 import HCSR04
from machine import Pin, PWM

frequenz = 1
d_sens = HCSR04(26, 27)
buzzer = PWM(Pin(32, Pin.OUT), freq=frequenz, duty = 256)


while True:
    n_frequenz = 11 - d_sens.distance_cm()//30
    if n_frequenz != frequenz:
        frequenz = n_frequenz
        buzzer.freq(frequenz)
    
    