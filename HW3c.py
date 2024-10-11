from machine import Pin, SPI
from time import sleep, sleep_ms, sleep_us
from random import randrange
#from binascii import hexlify

spi = SPI(1, baudrate=10_000, polarity=0, phase=0, bits=8, sck=10, mosi=11, miso=12)

Button = Pin(20, Pin.IN, Pin.PULL_UP)
LATCH = Pin(9, Pin.OUT)
Beeper = Pin(13, Pin.OUT)
Beeper.value(0)

def randNum(min,max):
    num = int(randrange(min,max+1))
    return(num)

def readShift():
    LATCH.value(1)
    sleep_us(10)
    LATCH.value(0)
    sleep_us(10)
    LATCH.value(1)
    # data is latched - now shift it in
    rxdata = spi.read(1, 0x42)
    return(rxdata)


Button1 = Pin(14, Pin.IN, Pin.PULL_UP)
Button2 = Pin(15, Pin.IN, Pin.PULL_UP)
LED1 = Pin(16, Pin.OUT)
LED2 = Pin(17, Pin.OUT)

A = 1
B = 1
N = randNum(0,255)
guess = 0
win = 0
while(0):		#randnum test loop
    zA = A
    A = Button1.value()
    if( (A==1) & (zA==0) ):
        N = randNum(0,255)
        print(N,type(N))
    sleep_ms(80)
while(0):		#shift register test loop
    zB = B
    B = Button2.value()
    if( (B==1) & (zB==0) ):
        N = int.from_bytes(readShift(),"little")
        print(N,type(N))
    sleep_ms(80)

while(1):
    zA = A
    A = Button2.value()
    if( (A==1) & (zA==0) ):
        guess = int.from_bytes(readShift(),"little")
        print(guess)
        if( (N == guess) & (win == 0) ):
            print('win')
            win = 1
        elif( (N > guess) & (win == 0) ):
            print('guess too low')
            win = 0
        elif( (N < guess) & (win == 0) ):
            print('guess too high')
            win = 0
        LED1.value(win)
    sleep_ms(80)



