import joystick from joystick_driver as jos

joys = jos(32,33,27)

radio = {}
radio[]

while True:
    time.sleep(0.1)
    joys.update()
    print("x:",joys.x,"y:",joys.y,"pressed:",joys.button)
    
def do():
    