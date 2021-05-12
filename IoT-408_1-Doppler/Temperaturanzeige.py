from machine import Pin, PWM, Timer
from time import sleep
from utime import ticks_us, sleep_us, ticks_diff
import dht

t = Timer(0)
sensor = dht.DHT11(Pin(33, Pin.IN))
led_r = PWM(Pin(25, Pin.OUT), freq=100, duty=0)
led_g = PWM(Pin(26, Pin.OUT), freq=100, duty=0)
led_b = PWM(Pin(27, Pin.OUT), freq=100, duty=0)

min_max = (20, 27)
min_max_colors = ((0, 0, 1023), (1023, 0, 0))
color_dif = list(map(lambda a,b: a-b, min_max_colors[1], min_max_colors[0]))
c_col = (0,0,0)
c_temp = None
interpolation = lambda a: a


#duration in centiseconds (0.01s)
def change_color(color_b, color_a, duration, inter):
    global led_r, led_g, led_b
    
    time = ticks_us()
    color_d = list(map(lambda a,b: a-b, color_a, color_b))
    for i in range(1, duration+1):
        current_step = inter(i/duration)
        led_r.duty(round(color_d[0]*current_step+color_b[0]))
        led_g.duty(round(color_d[1]*current_step+color_b[1]))
        led_b.duty(round(color_d[2]*current_step+color_b[2]))
        sleep_us(10000-ticks_diff(ticks_us(),time))
        time = ticks_us()
        

def loop(arg):
    global sensor, c_temp, c_col, min_max, min_max_colors, color_dif, interpolation
    
    sensor.measure()
    n_temp = sensor.temperature()
    if n_temp > min_max[1]:
        n_temp = min_max[1]
    elif n_temp < min_max[0]:
        n_temp = min_max[0]
    
    
    if not c_temp == n_temp:
        c_step = (n_temp-min_max[0])/(min_max[1]-min_max[0])
        n_col = list(map(lambda a,b: round(a*c_step+b)+, color_dif, min_max_colors[0]))
        print("values:",c_step, n_col, "Colors:", c_col, n_col)
        change_color(c_col, n_col, 190, interpolation)
        c_col = n_col
        c_temp = n_temp
    print('Temperatur:          ' + str(c_temp)+ 'C')


t.init(period=2000, mode=Timer.PERIODIC, callback=loop)