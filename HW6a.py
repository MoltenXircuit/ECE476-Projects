import LCD_24x32 as LCD
from machine import Pin, Timer
import time

buzz = Pin(13, Pin.OUT)
tim = Timer()
tim2 = Timer()
flag,N = 0,0
T0,T1,T2 = 0,0,0

def StartLCD():
    LCD.Init()
    LCD.Clear(Navy)

Navy = LCD.RGB(0,0,10)
Yellow = LCD.RGB(150,150,0)

#Timer Interrupt Setup
def toc(timer):
    global N,flag,T1
    buzz.value(0)
    T1 = time.ticks_us()

def tic(timer):
    tim2.init(freq=100, mode=Timer.ONE_SHOT, callback=toc)
    global N,flag,T0
    buzz.value(1)
    N += 1
    flag = 1
    T0 = time.ticks_us()



tim.init(freq=1, mode=Timer.PERIODIC, callback=tic)
  
#Code Start
StartLCD()
LCD.Box(30, 80, 330, 150, Yellow)
LCD.Text4('N=', 50, 100, Yellow, Navy)
    
while(1):
    #Draw text on update
    if (flag):
        print(N)
        flag = 0
        LCD.Number4(abs(N), 5, 3, 140, 100, Yellow, Navy)
        print('pulse_us =',T1-T0)
        print('cycle_us =',T0-T2)
        T2 = T0



