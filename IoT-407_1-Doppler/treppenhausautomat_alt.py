from machine import Pin
from utime import sleep, ticks_ms, ticks_add, ticks_diff
import _thread

led = Pin(2, Pin.OUT)
taster = Pin(13, Pin.IN, Pin.PULL_UP)
current_thread = None
lock = _thread.allocate_lock()

def led_on_for(led, time = 30):
    lock.acquire()
    rid = _thread.get_ident()
    global current_thread
    if current_thread is None:
        led.on()
    current_thread = rid
    lock.release()
    
    sleep(time)
    if rid == current_thread:
        led.off()
        current_thread = None


current_v = taster.value()
time_to_reach = None
t_press_state = 0

while True:
    # if als "taster changed" event gedacht 
    if not taster.value() == current_v:
        if taster.value() == t_press_state:
            _thread.start_new_thread(led_on_for, (led,))
            time_to_reach = ticks_add(ticks_ms(), 3000)
        current_v = taster.value()
    else:
        if taster.value() == t_press_state:
            if current_thread and ticks_diff(time_to_reach, ticks_ms()) <= 0:
                current_thread = None
                led.off()
                
                
            
            