from machine import Pin, PWM

taster = Pin(13, Pin.IN)
led_r = PWM(Pin(25, Pin.OUT), freq=100, duty=0)
led_g = PWM(Pin(26, Pin.OUT), freq=100, duty=0)
led_b = PWM(Pin(27, Pin.OUT), freq=100, duty=0)

power = 0


def power_up(arg):
    global power
    if power + 0.2 <= 1:
        power += 0.2
    else:
        power = 0
    led_power(round(1023*power))
    print("Power increased to:", power)


def led_power(amount=0):
    global led_r, led_g, led_b
    led_r.duty(amount)
    led_g.duty(amount)
    led_b.duty(amount)
    
taster.irq(trigger=Pin.IRQ_FALLING, handler=power_up)