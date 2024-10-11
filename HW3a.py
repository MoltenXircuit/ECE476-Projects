from machine import Pin
from time import sleep_ms

Button1 = Pin(14, Pin.IN, Pin.PULL_UP)
Button2 = Pin(15, Pin.IN, Pin.PULL_UP)
LED1 = Pin(16, Pin.OUT)
LED2 = Pin(17, Pin.OUT)

while(1):
    X = not Button1.value()
    Y = not Button2.value()
    sleep_ms(100)
    A = X & Y
    B = X ^ Y
    print(A,B)
    LED1.value(A)
    LED2.value(B)