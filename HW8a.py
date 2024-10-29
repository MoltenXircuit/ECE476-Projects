import LCD_24x32 as LCD
import machine
from machine import Pin, ADC, Timer
#import time
from time import ticks_ms
a2d2 = ADC(2)
kV = 3.3 / 65535

samplingFreq = 100
samplingSeconds = 10
samples = samplingSeconds * samplingFreq

#------------Timer Interrupt Setup----------
tim = Timer()
flag= 0
#tim2 = Timer()
#def toc(timer):
#    global flag2
#    flag2 = 1
def tic(timer):
    global flag
    flag = 1


tim.init(freq=samplingFreq, mode=Timer.PERIODIC, callback=tic)


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

Xmin = 10
Xmax = 470
Ymin = 40
Ymax = 280

#------------Code Start----------
StartLCD()
LCD.Title("HW8 - Heart Sensor", White, Navy)
t = 0
T1 = 1
Divisions = 8
dX = (Xmax - Xmin)/Divisions
dY = (Ymax - Ymin)/Divisions
for i in range(0,Divisions+1):
    LCD.Line(Xmin, int(Ymin+i*dY), Xmax, int(Ymin+i*dY), Grey)
    LCD.Line(int(Xmin+i*dX), Ymin, int(Xmin+i*dX), Ymax, Grey)

dX = (Xmax - Xmin)/samples
dY = (Ymax - Ymin)/100
Y = [0] * (samples+1)

while (t<samples):
    if (flag == 1):
        t+=1
        flag = 0
        Volts = (30*a2d2.read_u16() * kV)
        print(Volts)
        Y[t] = Volts
        Y[0] = Y[1]
        LCD.Line(Xmin+int((t-1)*dX), Ymax-int(Y[t-1]*dY), Xmin+int(t*dX), Ymax-int(Y[t]*dY), Yellow)
tim.deinit()