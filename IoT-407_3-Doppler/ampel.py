from machine import Pin, PWM
from time import sleep_ms
from utime import ticks_us, sleep_us, ticks_diff
from ujson import loads

led_r = PWM(Pin(25, Pin.OUT), freq=100, duty=0)
led_g = PWM(Pin(26, Pin.OUT), freq=100, duty=0)
led_b = PWM(Pin(27, Pin.OUT), freq=100, duty=0)


# color_list - list of instructions. atleast 2 items. layout = [((R,G,B), duration in ms), ...]
# mode - 0 = once | 1 = repeat loop | 2 = repeat reverse
# interpolation - function... parameter = number in range 0-1 ... return number in range 0-1 | None = step
def rgb_sequence(color_list, mode=1, interpolation=None):
    repeat = True
    list_now = color_list
    list_switch = False
    
    while repeat:
        for next_index, item in enumerate(list_now, start=1):
            col, dur = item
            
            if next_index >= len(list_now):
                if mode == 1:
                    next_item = list_now[0]
                elif mode == 2:
                    next_item = list_now[1] if list_switch else list_now[-2]
            else:
                next_item = list_now[next_index]
            
            if interpolation:
                change_color(col, next_item[0], dur//10, interpolation)
            else:
                step_color(col)
                sleep_ms(dur)
                
                
        if mode == 0:
            repeat = False
        elif mode == 2:
            list_switch = not list_switch
            list_now = color_list[-2::-1] if list_switch else color_list[1:]


#duration in centiseconds (0.01s)
def change_color(color_b, color_a, duration, inter):
    time = ticks_us()
    color_d = list(map(lambda a,b: a-b, color_a, color_b))
    for i in range(1, duration+1):
        current_step = inter(i/duration)
        led_r.duty(round(color_d[0]*current_step+color_b[0]))
        led_g.duty(round(color_d[1]*current_step+color_b[1]))
        led_b.duty(round(color_d[2]*current_step+color_b[2]))
        sleep_us(10000-ticks_diff(ticks_us(),time))
        time = ticks_us()
    
    
def step_color(color):
    r, g, b = color
    
    led_r.duty(r)
    led_g.duty(g)
    led_b.duty(b)
    
    
string = ""
with open("config.json", "r") as file:
    string = file.read()
    file.close()
instructions = loads(string)

# rgb_sequence(instructions["RGB"], interpolation=lambda a:a)
rgb_sequence(instructions["Ampel"])
# rgb_sequence([((1023,0,0), 10000), ((1023,1023,0), 1000), ((0,1023,0), 10000), ((0,0,0), 500), ((0,1023,0), 500), ((0,0,0), 500), ((0,1023,0), 500), ((0,0,0), 500), ((0,1023,0), 500), ((0,0,0), 500), ((0,1023,0), 500), ((1023,1023,0), 1000)], interpolation=lambda a:a)