import LCD_24x32 as LCD
from machine import Pin, Timer
import time

buzz = Pin(13, Pin.OUT)
tim = Timer()
tim2 = Timer()
flag,N = 0,1000
T0,T1,T2 = 0,0,0

B1 = Pin(15,Pin.IN,Pin.PULL_UP)
B2 = Pin(14,Pin.IN,Pin.PULL_UP)

#-----------Edge Interrupt Setup-----------
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
def StartLCD():
    LCD.Init()
    LCD.Clear(Navy)

Navy = LCD.RGB(0,0,10)
Yellow = LCD.RGB(150,150,0)


#------------Timer Interrupt Setup----------
def toc(timer):
    global N,T1
    buzz.value(0)
    T1 = time.ticks_us()

def tic(timer):
    global N,flag,T0
    tim.init(period=int(N), mode=Timer.ONE_SHOT, callback=tic)
    tim2.init(period=10, mode=Timer.ONE_SHOT, callback=toc)
    buzz.value(1)
    flag = 1
    T0 = time.ticks_us()


tim.init(period=N, mode=Timer.ONE_SHOT, callback=tic)
  
#--------------Code Start--------------
StartLCD()
LCD.Box(30, 80, 400, 200, Yellow)
LCD.Text4('Beats Per Minute', 50, 100, Yellow, Navy)
    
while(1):
    #Draw text on update
    if (flag):
        print('N = ',N)
        flag = 0
        LCD.Number4(60000/N, 5, 3, 140, 150, Yellow, Navy)
        print('pulse_us =',T1-T0)
        print('cycle_us =',T0-T2)
        T2 = T0
