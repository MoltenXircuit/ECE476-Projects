from time import sleep 
from machine import Pin, I2C, Timer, bitstream
from math import sqrt
import LCD_16x24 as LCD

samplingFreq = 100
samplingSeconds = 3
samples = samplingSeconds * samplingFreq

Beeper = Pin(13, Pin.OUT)
Button14 = Pin(14, Pin.IN, Pin.PULL_UP)
Button15 = Pin(15, Pin.IN, Pin.PULL_UP)

def Beep():
    Beeper.value(1)
    sleep(0.1)
    Beeper.value(0)
#------------Timer Interrupt Setup----------
tim = Timer()
flag = 0
def tic(timer):
    global flag
    flag = 1

tim.init(freq=samplingFreq, mode=Timer.PERIODIC, callback=tic)

#-----------------NeoPixel Code--------------------
timing = [300, 900, 700, 500]
np = Pin(12, Pin.OUT)

N = 8
X = bytearray([0,0,0])

def addLight(A,color):
    if (color == 'Y'):
        A.extend(bytearray([20,20,0]))
    elif (color == 'G'):
        A.extend(bytearray([20,0,0]))
    elif (color == 'R'):
        A.extend(bytearray([0,20,0]))

#------------------I2C routines---------------------
def reg_write(i2c, addr, reg, data):
    msg = bytearray()
    msg.append(data)
    i2c.writeto_mem(addr, reg, msg)
    
def reg_read(i2c, addr, reg, nbytes=1):
    if nbytes < 1:
        return bytearray()
    data = i2c.readfrom_mem(addr, reg, nbytes)
    return data

def accel_read(reg):
    x = reg_read(i2c, addr, reg, 2)
    y = (x[0] << 8) + x[1]
    if(y > 0x8000):
        y = y - 0x10000
    y = y / 0x8000
    return(y)

i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))

# Print out any addresses found
devices = i2c.scan()
if devices:
    for d in devices:
        print('I2C Device Found:',hex(d))

addr = devices[0]
print('Communicating with ', hex(addr))

# set bandwidth
reg_write(i2c, 0x68, 0x1a, 3)
# set range
reg_write(i2c, 0x68, 0x1c, 0x00)
RANGE = 2
# set clock freq
reg_write(i2c, 0x68, 0x6b, 0)

sleep(1)

#-----------------LCD Code----------------------
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

#-----------------Main Code----------------------
StartLCD()
LCD.Title("HW9 - Jump Meter", White, Navy)
jump_3 = 0
jump_2 = 0
jump_1 = 0

npt = samples
#Data = [ [0]*npt, [0]*npt, [0]*npt, [0]*npt]
#t = [0]*npt

while(1):
    while(Button15.value() == 1):
        pass
    X = bytearray([20,20,0])
    sleep(0.2)
    bitstream(np, 0, timing, X)
    for neo in range(1,7):
        sleep(0.2)
        addLight(X,'Y')
        bitstream(np, 0, timing, X)
    sleep(0.2)
    addLight(X,'G')
    bitstream(np, 0, timing, X)
    Beep()
    jump_time = 0
    jump_dist = 0
    threshold_accum = int(samplingFreq * 0.1)
    accum = 0
    i = 0
    while(i<samples):
        if (flag == 1):
            flag = 0
            x = accel_read(0x3b) * RANGE
            y = accel_read(0x3d) * RANGE
            z = accel_read(0x3f) * RANGE
            print(i)
            accel = sqrt(x**2+y**2+z**2)
            #Data[0][i] = accel
            if (accel>1.5 and jump_time == 0):   #testing if starting jump
                #Data[1][i] = 1
                accum = accum+1
            elif (accel<0.8 and accum > threshold_accum):    #testing if jumping
                #Data[2][i] = 1 
                jump_time = jump_time + 1
            elif (accel>1 and jump_time != 0):   #disabling jump test if already jumped 
                #Data[3][i] = 1
                accum = 0
            #t[i] = i
            i = i+1
            
    #Data[0][0] = -RANGE
    #Data[0][1] = +RANGE
    X = bytearray([0,0,0]*8)
    bitstream(np, 0, timing, X)    
    LCD.Clear(Navy)
    #LCD.Plot(t,Data)
    #for i in range(0,npt):
        #print(Data[0][i], Data[1][i])
    jump_time = jump_time/samplingFreq
    a = 9.807   #accel is 9.807 m/s2
    jump_distance = (a/8) * (jump_time ** 2) # jump distance in meters
    jump_distance = jump_distance * 100
    if (jump_distance > jump_1):
        jump_3 = jump_2
        jump_2 = jump_1
        jump_1 = jump_distance
    elif (jump_distance > jump_2):
        jump_3 = jump_2
        jump_2 = jump_distance
    elif (jump_distance > jump_3):
        jump_3 = jump_distance

    LCD.Title("HW9 - Jump Meter", White, Navy)
    LCD.Text2('Best Jump Heights:',10, 30, DkGreen, Navy)
    LCD.Text2('1:',50, 80, DkGreen, Navy)
    LCD.Number2(jump_1,5,2,80, 80, White, Navy)
    LCD.Text2('cm',200, 80, DkGreen, Navy)
    
    LCD.Text2('2:',50, 130, DkGreen, Navy)
    LCD.Number2(jump_2,5,2,80, 130, White, Navy)
    LCD.Text2('cm',200, 130, DkGreen, Navy)

    LCD.Text2('3:',50, 180, DkGreen, Navy)
    LCD.Number2(jump_3,5,2,80, 180, White, Navy)
    LCD.Text2('cm',200, 180, DkGreen, Navy)
    
    LCD.Text2('Your Jump Height:',10, 250, LtGreen, Navy)
    LCD.Number2(jump_distance,5,2,280, 250, White, Navy)
    LCD.Text2('cm',400, 250, DkGreen, Navy)

    print("jump height is: ", (jump_distance*100), "cm")
    print("jump time is: ", jump_time, "seconds")

