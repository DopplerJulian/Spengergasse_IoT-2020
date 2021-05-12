from machine import Pin, Timer
from time import sleep, time
import utime
import dht

sensor = dht.DHT11(Pin(33, Pin.IN))
t = Timer(0)
# Struktur {hour:{time:(temp, hum), ...}, ...}
measurements = {}
# ändert sich nur jede nächste Stunde
temp_a = []
hum_a = []

last_measurement = None
day = None
hour = None

def measure(arg):
    global sensor, measurements, last_measurement, day, temp_a, hum_a, hour
    try:
        sensor.measure()
        last_measurement = time()
        m = sensor.temperature(), sensor.humidity()
           
        if not hour == utime.localtime(last_measurement)[3]:
            if not day == utime.localtime(last_measurement)[2]:
                measurments = {}
                temp_a = []
                hum_a = []
                # schneller fix
                hour = utime.localtime(last_measurement)[3]
                if hour > 0:
                    for i in range(hour):
                        temp_a.append("0")
                        hum_a.append("0")
            else:
                la = last_avg_h()
                temp_a.append(la[0])
                hum_a.append(la[1])
            hour = utime.localtime(last_measurement)[3]
            measurements[hour] = {}
            
        measurements[hour][last_measurement] = m
    except OSError as e:
        print('Failed to read sensor.')


def last_avg():
    global measurements, hour
    temp = 0
    hum = 0
    count = 0
    for it in range(hour,24):
        print(measurements, it)
        for i in measurements[it].values():
            count += 1
            temp += i[0]
            hum += i[1]
    return round(temp/len(measurements[hour])), round(hum/len(measurements[hour]))
            
def last_avg_h():
    global measurements, hour
    temp = 0
    hum = 0
    for i in measurements[hour].values():
        temp += i[0]
        hum += i[1]
    return round(temp/len(measurements[hour])), round(hum/len(measurements[hour]))
    

def start():
    t.init(period=2000, mode=Timer.PERIODIC, callback=measure)
    
def p(arg):
    print(measurements)