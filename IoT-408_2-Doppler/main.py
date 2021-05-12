import network
from machine import Pin
from time import sleep
import utime
import usocket
import gc
import station
gc.collect()

date = utime.localtime(utime.time())
date = "{}:{} {}.{}.{}".format(date[3], date[4], date[2], date[1], date[0])

station.start()

ssid = b'ssid'
pw = "pw"

print("Connecting to WiFi...")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
for i in range(10):
    sleep(1)
    if wifi.active():
        break

wifi.config(dhcp_hostname = "ESP32")
wifi.connect(ssid, pw)
while not wifi.isconnected():
    pass
print("Connected.")
print("ESP32 online:", ssid, "IP:", wifi.ifconfig())



html = ""
with open("index.html", "r") as file:
    html = file.read()
    file.close()
    
def web_page():
    global html, date
    lm = station.measurements[station.hour][station.last_measurement]
    la = station.last_avg()
    ta = "["+", ".join(station.temp_a)+"]"
    ha = "["+", ".join(station.hum_a)+"]"
    st = html.format(start_d=date, temp_n=lm[0], temp_a=la[0], hum_n=lm[1], hum_a=la[1], temp_val=ta, hum_val=ha)
    return st



s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)  #Socket Stream TCP
s.bind(('', 80))                                          #Socket auf IP,Port gebunden
s.listen(5)                                               #max Anzahl queued connections

while True:
  if gc.mem_free() < 102000:
    gc.collect()  
  conn, addr = s.accept()
  conn.settimeout(3.0)
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  conn.settimeout(None)
  request = str(request)
  print('Content = %s' % request)  #wer mehr Info auf der Console möchte...
  
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()
