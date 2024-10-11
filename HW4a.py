from machine import ADC, Pin, PWM
from time import sleep_ms

a2d0 = ADC(0)
#a2d1 = ADC(1)
#Buzzer = Pin(13, Pin.OUT)
Button1 = Pin(14, Pin.IN, Pin.PULL_UP)
#Button2 = Pin(15, Pin.IN, Pin.PULL_UP)
#LED1 = Pin(16, Pin.OUT)
#LED2 = Pin(17, Pin.OUT)

Spkr = Pin(18, Pin.OUT)
Spkr = PWM(Pin(18))
Spkr.freq (1000)

freq = 220
i = 0
x = 0
k = 3.3 / 65520
V0 = 0
while(1):
    if (Button1.value() == 0):
        #set freq to analog in
        a0 = a2d0.read_u16()
        V0 = k * (a0 - 32767) + 1.65
        x = (a0 >> 4)/4028
        freq =  220 + int(x * 220)
        Spkr.freq (freq)
        Spkr.duty_u16 (32768)
        print(V0,freq)
    else:
        Spkr.duty_u16 (0)
    sleep_ms(25)
