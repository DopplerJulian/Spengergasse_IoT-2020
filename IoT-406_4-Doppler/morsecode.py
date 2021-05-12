from machine import Pin
from time import sleep

def string_to_tuple(string):
    string = string.upper()
    dic = {"A":(1,2), "B":(2,1,1,1), "C":(2,1,2,1), "D":(2,1,1), "E":(1),
           "F":(1,1,2,1), "G":(2,2,1), "H":(1,1,1,1), "I":(1,1), "J":(1,2,2,2),
           "K":(2,1,2), "L":(1,2,1,1), "M":(2,2), "N":(2,1), "O":(2,2,2),
           "P":(1,2,2,1), "Q":(2,2,1,2), "R":(1,2,1), "S":(1,1,1), "T":(2),
           "U":(1,1,2), "V":(1,1,1,2), "W":(1,2,2), "X":(2,1,1,2), "Y":(2,1,2,2),
           "Z":(2,2,1,1), "0":(2,2,2,2,2), "1":(1,2,2,2,2), "2":(1,1,2,2,2),
           "3":(1,1,1,2,2), "4":(1,1,1,1,2), "5":(1,1,1,1,1), "6":(2,1,1,1,1),
           "7":(2,2,1,1,1), "8":(2,2,2,1,1), "9":(2,2,2,2,1), " ":(3,)}
    result = []
    for i in string:
        result.append(dic[i])
    return result


def morse_blinker(morsecode, led = Pin(2,Pin.OUT), dit_length = 0.25):
    last = 0
    for i in range(len(morsecode)):
        for it in morsecode[i]:
            if not last == i:
                sleep(dit_length*2)
                last = i
            if it == 1:
                led.on()
                sleep(dit_length)
                led.off()
            elif it == 2:
                led.on()
                sleep(dit_length*3)
                led.off()
            elif it == 3:
                sleep(dit_length)
            else:
                raise Exception("Unerlaubtes Zeichen an index: {}".format(i))
            sleep(dit_length)
    

morse_blinker(string_to_tuple("sos hallo"))