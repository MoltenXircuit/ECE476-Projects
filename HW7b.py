import LCD_24x32 as LCD

import machine, onewire, ds18x20
from machine import Pin, Timer
import time
ds_pin = machine.Pin(4, Pin.PULL_UP)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))


roms = ds_sensor.scan()
print('Found DS devices: ', roms)

file1 = open("TemperatureData2.txt", "wt")

#------------Timer Interrupt Setup----------
tim = Timer()
tim2 = Timer()
flag = 0
def toc(timer):
    global flag
    flag = 1
def tic(timer):
    tim2.init(period=750, mode=Timer.ONE_SHOT, callback=toc)
    ds_sensor.convert_temp()


tim.init(period=5_000, mode=Timer.PERIODIC, callback=tic)

#Temperature test loop
while 0:
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
        print(rom)
        tempC = ds_sensor.read_temp(rom)
        print(tempC)
    time.sleep(5)

#LCD Code

def StartLCD():
    LCD.Init()
    LCD.Clear(Navy)
Navy = LCD.RGB(0,0,10)
Yellow = LCD.RGB(150,150,0)
Grey = LCD.RGB(50,50,50)

Xmin = 50
Xmax = 470
Ymin = 10
Ymax = 280

Tamb = 21.5
#------------Code Start----------
StartLCD()
t = 0
dX = (Xmax - Xmin)/10
dY = (Ymax - Ymin)/10
for i in range(0,11):
    LCD.Line(Xmin, int(Ymin+i*dY), Xmax, int(Ymin+i*dY), Grey)
    LCD.Line(int(Xmin+i*dX), Ymin, int(Xmin+i*dX), Ymax, Grey)

samples = 360
dX = (Xmax - Xmin)/samples
dY = (Ymax - Ymin)/100
Y = [0] * (samples+1)

while (t<samples):
    if (flag == 1):
        t+=1
        flag = 0
        for rom in roms:
            tempC = ds_sensor.read_temp(rom)
            print(tempC)
        Y[t] = tempC
        Y[0] = Y[1]
        LCD.Line(Xmin+int((t-1)*dX), Ymax-int(Y[t-1]*dY), Xmin+int(t*dX), Ymax-int(Y[t]*dY), Yellow)
        file1.write(str(tempC))
        file1.write("\n")
file1.close()
print('File Closed')
