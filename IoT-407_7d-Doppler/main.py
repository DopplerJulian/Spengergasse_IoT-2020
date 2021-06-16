import time
from machine import Pin, PWM
from rotary_irq_esp import RotaryIRQ

r = RotaryIRQ(pin_num_clk=35, 
              pin_num_dt=34, 
              min_val=1, 
              max_val=21, 
              reverse=True, 
              range_mode=RotaryIRQ.RANGE_BOUNDED)
              
pwm = PWM(Pin(13, Pin.OUT), freq=200, duty=307)

val_old = r.value()
while True:
    val_new = r.value()
    
    if val_old != val_new:
        val_old = val_new
        pwm.freq(val_old*200)
        print('result =', val_new)
        
    time.sleep_ms(50)