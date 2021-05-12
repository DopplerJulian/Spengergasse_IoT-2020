from time import sleep
from machine import Pin

led_r = Pin(25, Pin.OUT)
led_g = Pin(26, Pin.OUT)
led_b = Pin(27, Pin.OUT)

# 1...Rot | 2...Grün | 3...Gelb | else...off
def color(col):
    if col == 1:
        led_r.on()
        led_g.off()
        led_b.off()
    elif col == 2:
        led_r.off()
        led_g.on()
        led_b.off()
    elif col == 3:
        led_r.on()
        led_g.on()
        led_b.off()
    else:
        led_r.off()
        led_g.off()
        led_b.off()


while True:
    color(1)
    sleep(10)
    color(3)
    sleep(1)
    color(2)
    sleep(10)
    for i in range(4):
        color(0)
        sleep(0.5)
        color(2)
        sleep(0.5)
    color(3)
    sleep(1)
    

    