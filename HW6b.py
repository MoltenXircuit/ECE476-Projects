from machine import Pin
import time

beeper = Pin(13, Pin.OUT)
B1 = Pin(15,Pin.IN,Pin.PULL_UP)
B2 = Pin(14,Pin.IN,Pin.PULL_UP)

N = 1000
flag = 0

#Edge Interrupt Setup
def Button15(B1):
    global N, flag
    N = 1.01*N
    flag = 1

def Button14(B2):
    global N, flag
    N = 0.99*N
    flag = 1
    
# options are RISING, FALLING, LOW_LEVEL, HIGH_LEVEL
B1.irq(trigger=Pin.IRQ_FALLING, handler=Button15)
B2.irq(trigger=Pin.IRQ_FALLING, handler=Button14)


while(1):
    if (flag):
        print('N = ',N)
        flag = 0
