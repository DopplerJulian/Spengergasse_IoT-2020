from machine import Pin, PWM, Timer

taster = Pin(13, Pin.IN)
led_r = PWM(Pin(25, Pin.OUT), freq=100, duty=0)
led_g = PWM(Pin(26, Pin.OUT), freq=100, duty=0)
led_b = PWM(Pin(27, Pin.OUT), freq=100, duty=0)

# False: Dunkel -> Hell | True: Hell -> Dunkel
direction = False
# True wenn es ein doppelter Tastendruck passiert
p_double = False
power = 0
t_1 = Timer(0)
t_2 = Timer(1)
t_3 = Timer(2)
# 0 = Anfangs Stadium | 1 = Knopf 1 Mal gedrückt | 2 = Knopf mehrmals gedrückt
status = 0
# Prozent/Sekunde (je höher, je genauer)
pps = 33
# um wie viel die Helligkeit alle 10 ms geändert wird
step_size = int((1024*(pps/100))//100)


def pin_on():
    global t_2, t_3
    t_3.deinit()
    t_2.init(period=50, mode=Timer.ONE_SHOT, callback=press_short)
    
def pin_off():
    global t_1, t_2, t_3
    t_1.deinit()
    t_2.deinit()
    t_3.init(period=1000, mode=Timer.ONE_SHOT, callback=reset)
        
def reset(arg):
    global status
    status = 0
    
        
def press_short(arg):
    global t_1, status
    if status == 0:
        t_1.init(period=650, mode=Timer.ONE_SHOT, callback=long_press)
        status = 1
    else:
        t_1.init(period=650, mode=Timer.ONE_SHOT, callback=long_press)
        status = 2
        
        
def long_press(arg):
    global status, p_double, t_1
    if not status == 0:
        if status == 2:
            p_double = True
        else:
            p_double = False
        t_1.init(period=10, mode=Timer.PERIODIC, callback=color_changer)


def color_changer(arg):
    global direction, p_double, step_size, power
    if direction == p_double:
        print("Dunkel -> Hell")
        # Dunkel -> Hell
        n = power+step_size
        print(n)
        if n > 1023:
            direction = not direction
            power = 1023 -(n - 1023)
        else:
            power = n
    else:
        print("Hell -> Dunkel")
        # Hell -> Dunkel
        n = power-step_size
        print(n)
        if n < 0:
            direction = not direction
            power = -n
        else:
            power = n
    print("Values:",n,direction,p_double)
    led_power(power)


def led_power(amount=0):
    global led_r, led_g, led_b
    led_r.duty(amount)
    led_g.duty(amount)
    led_b.duty(amount)
    

def taster_event(pin):
    if pin():
        pin_off()
    else:
        pin_on()
        
taster.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=taster_event)