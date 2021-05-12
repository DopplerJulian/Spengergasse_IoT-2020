from machine import Pin, Timer

#Angabe in ms
DURATION = 30000
OFF = 3000

led = Pin(2, Pin.OUT)
taster = Pin(13, Pin.IN, Pin.PULL_UP)
t_long = Timer(0)
t_short = Timer(1)
# 0 = Led aus | 1 = langer Timer an | 2 = beide Timer an
status = 0

def pin_on():
    global led, t_long, t_short, status, DURATION, OFF
    
    if not led():
        led.on()
    t_long.deinit()
    t_long.init(period=DURATION, mode=Timer.ONE_SHOT, callback=led_off)
    t_short.init(period=OFF, mode=Timer.ONE_SHOT, callback=led_off)
    status = 2
    
def pin_off():
    global t_short, status
    
    if status == 2:
        t_short.deinit()
        status = 1
    
def led_off(arg):
    global led, t_long, t_short, status
    
    led.off()
    t_long.deinit()
    t_short.deinit()
    status = 0

def taster_event(pin):
    if pin():
        pin_off()
    else:
        pin_on()
        
taster.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=taster_event)
