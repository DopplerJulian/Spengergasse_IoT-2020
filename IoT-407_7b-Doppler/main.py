# import read, write
# write.do_write()
# read.do_read()

import schranke

schr = schranke.Schranke(Servo(Pin(27)), 18,13,12,25,26)
schr.activate()