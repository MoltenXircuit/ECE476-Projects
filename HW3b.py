from machine import Pin
from time import sleep_ms

Button1 = Pin(14, Pin.IN, Pin.PULL_UP)
Button2 = Pin(15, Pin.IN, Pin.PULL_UP)
LED1 = Pin(16, Pin.OUT)
LED2 = Pin(17, Pin.OUT)

A = 1
B = 1
N = 0
while(1):
    zA = A
    A = Button1.value()
    zB = B
    B = Button2.value()
    if( (A==1) & (zA==0) ):
        N += 1
    if( (B==1) & (zB==0) ):
        N += 10
    print('Score',N)
    sleep_ms(80)