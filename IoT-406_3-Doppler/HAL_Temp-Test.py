import esp32
from time import sleep

while True:
    print("Hall: {}| Temp: {}".format(esp32.hall_sensor(), esp32.raw_temperature()))
    sleep(0.5)