import LCD_24x32 as LCD
import machine, _thread
from machine import Pin, ADC, Timer
#import time
from time import ticks_us
a2d2 = ADC(2)
kV = 3.3 / 65535
beep = Pin(13, Pin.OUT)
led = Pin(16, Pin.OUT)

samplingFreq = 1_000
samplingSeconds = 7
samples = samplingSeconds * samplingFreq

#------------Timer Interrupt Setup----------
tim = Timer()
tim2 = Timer()
flag,flag1,flag2 = 0,0,0
def toc(timer):
    global flag2
    flag2 = 1
def tic(timer):
    global flag
    flag = 1




#LCD Code

def StartLCD():
    LCD.Init()
    LCD.Clear(Navy)
Navy = LCD.RGB(0, 0, 5)
White = LCD.RGB(150,150,150)
LtGreen = LCD.RGB(50,150,50)
DkGreen = LCD.RGB(0,100,0)
Yellow = LCD.RGB(150,150,0)
Pink = LCD.RGB(150,50,100)
Grey = LCD.RGB(50,50,50)

Xmin = 180
Xmax = 470
Ymin = 40
Ymax = 280

def runLCD():
    global t,Y1,bpm,beatTime, flag1, beat
    Xtemp = 0
    Ytemp = 10
    while(t<samples):
        # if Y has changed, update dx&dy and get temp variables of x and y
        if Ytemp != Y1:
            dx = t-Xtemp
            dy  = Y1 - Ytemp
            Xtemp = t
            Ytemp = Y1
            #print(int(Ytemp))
            LCD.Line(Xmin+int((Xtemp-dx)*kX), Ymax-int((Y1-dy)*kY), Xmin+int(Xtemp*kX), Ymax-int(Y1*kY), Yellow)
            #LCD.Line(Xmin+int((Xtemp-dx)*kX), Ymax-int(20*beat), Xmin+int(Xtemp*kX), Ymax-int(20*beat), Pink)

        # if bpm and beatTime has changed, update numbers
        if flag1 == 1:            
            flag1 = 0
            LCD.Number(bpm,5,2,10, 50, White, Navy)
            #print(int(bpm), int(beatTime))
            LCD.Number(beatTime,5,1,10, 100, White, Navy)
    
    
#------------Code Start----------
StartLCD()
LCD.Title("HW8 - Heart Sensor", White, Navy)
LCD.Text('Beats Per Minute',10, 30, DkGreen, Navy)
LCD.Text('mS Between Beats',10, 80, LtGreen, Navy)
t = 0
index = 0
beat = 0
T0,T1 = 1,1
Divisions = 8
dX = (Xmax - Xmin)/Divisions
dY = (Ymax - Ymin)/Divisions
for i in range(0,Divisions+1):
    LCD.Line(Xmin, int(Ymin+i*dY), Xmax, int(Ymin+i*dY), Grey)
    LCD.Line(int(Xmin+i*dX), Ymin, int(Xmin+i*dX), Ymax, Grey)

kX = (Xmax - Xmin)/samples
kY = (Ymax - Ymin)/200
Y = [int(0)] * (100+1)
Y[0] = 1
Y0,Y1 = 0,0
tim.init(freq=samplingFreq, mode=Timer.PERIODIC, callback=tic)

#core two handles lcd update
_thread.start_new_thread(runLCD,())

while (t<samples):
    if (flag == 1):
        index = t%100
        index1 = (t-1)%100
        t+=1
        flag = 0
        Volts = (a2d2.read_u16() * kV)
#        print(Volts)
        Y[index] = int(20*Volts*kY)
        Y1 = Y[index]

    if (Y[index] > 70 and Y[index1] <= 70):
        tempT = ticks_us()
        if (tempT-T1) > 200_000:
            beat = 1
            beep.value(1)
            led.value(1)
            tim2.init(period=100, mode=Timer.ONE_SHOT, callback=toc)
            T0 = T1
            T1 = tempT
            beatTime = (T1-T0)/1_000
            bpm = 60/(beatTime/1_000)
            flag1 = 1
    if (flag2 == 1):
        flag2 = 0
        beat = 0
        beep.value(0)
        led.value(0)
beep.value(0)
led.value(0)
