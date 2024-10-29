from math import log
import Matrix as matrix
import machine, onewire, ds18x20
from machine import Pin, Timer
ds_pin = machine.Pin(4, Pin.PULL_UP)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))


roms = ds_sensor.scan()
print('Found DS devices: ', roms)

file1 = open("TemperatureData2.txt", "wt")

#------------Timer Interrupt Setup----------
tim = Timer()
tim2 = Timer()
flag = 0
t,ptr = 0,0
def toc(timer):
    global flag
    flag = 1
def tic(timer):
    global t,ptr
    tim2.init(period=750, mode=Timer.ONE_SHOT, callback=toc)
    ds_sensor.convert_temp()
    ptr = (ptr + 1) % 100
    t += 1



tim.init(period=1_000, mode=Timer.PERIODIC, callback=tic)


#------------Code Start----------

Tamb = 21.5
B = [[0.01,0],[0,0.01]]
Y = [[-0.01],[0]]
decay = 0.99
x = 0
tempC = Tamb
while(x<=300):
    if(flag == 1):
        flag = 0
        tempC = ds_sensor.read_temp(roms[0])
        x += 1
        y = log(tempC - Tamb)
        #B = matrix.mult_k(B, decay)
        #Y = matrix.mult_k(Y, decay)
        B = matrix.add(B, [[x*x, x], [x, 1]])
        Y = matrix.add(Y, [[x*y], [y]])
        Bi = matrix.inv(B)
        A = matrix.mult(Bi, Y)
        if(A[0][0] != 0):
            a = -1 / A[0][0]
        else:
            a = 1_000_000
        b = A[1][0]
        print(x, a, b)

        