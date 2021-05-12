import time
from machine import Pin, PWM
import mfrc522

    
class Servo:
    def __init__(self, pin, minimum_cycle=1, maximum_cycle=2):
        self.pwm = PWM(pin, freq=50, duty=0)
    
    def rotate(self, degree):
        if not 0 <= degree <= 180:
            raise Exception("Rotate takes a number between 0 and 180")
        microsec = (degree/180)*1.63+0.5
        pwm = int(1023/(20/microsec))
        self.pwm.duty(pwm)

class Schranke:
    def __init__(self, servo, sck, mosi, miso, rst, cs, data = [0, 1, 2, 242, 4, 2, 166, 7, 8, 9, 4, 11, 12, 13, 1, 255]):
        self.ser = servo
        self.data = data
        self.rdr = mfrc522.MFRC522(sck, mosi, miso, rst, cs)
        
    
    def open_up(self):
        self.ser.rotate(90)
        
    def close_down(self):
        self.ser.rotate(0)
        
    def activate(self):
        rdr = self.rdr
        while True:
            (stat, tag_type) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print("  - uid : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")

                    if rdr.select_tag(raw_uid) == rdr.OK:
                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                            read = rdr.read(8)
                            print("Address 8 data: %s" % read)
                            rdr.stop_crypto1()
                            if read == self.data:
                                print("opens")
                                self.open_up()
                                time.sleep(5)
                                self.close_down()
                            else:
                                print("Data doesn´t match")
                        else:
                            print("Authentication error")
                    else:
                        print("Failed to select tag")