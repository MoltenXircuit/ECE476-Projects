from machine import UART, Pin
from time import sleep
import LCD
from math import sin, cos, pi

uart0 = UART(0, 9600)
uart0.init(9600, bits=8, parity=None, stop=1, tx=0, rx=1)

Button14 = Pin(14, Pin.IN, Pin.PULL_UP)
Button15 = Pin(15, Pin.IN, Pin.PULL_UP)
Beeper = Pin(13, Pin.OUT)

FileName = 'Speedometer.txt'
Error_Flag = 0

def Beep():
    Beeper.value(1)
    sleep(0.1)
    Beeper.value(0)
    
def Str2Num(X):
    global Error_Flag
    n = len(X)
    y = 0
    flag = 0
    k = 0
    for i in range(0,n):
        z = X[i]
        if(z in {'0','1','2','3','4','5','6','7','8','9','0','.'}):
            if(z == '.'):
                flag = 1
            else:
                if(flag == 0):
                    y = 10*y + int(z)
                else:
                    k -= 1
                    y = y + int(z) * (10 ** k)
        else:
            Error_Flag = 1
    return(y)

def GPS_Read_Line(chan):
    flag = 0
    n = 0
    msg = ''
    if(chan == 0):
        x = str(uart0.read())
    else:
        x = uart1.read(1)
    if(x != None):
        msg = x.split("$")
    return(msg[1:])

    
def GPS_Read(chan):
    flag = 0
    
    while(flag == 0):
        msgs = GPS_Read_Line(chan)
        time = 0
        LatD = 0
        LatM = 0
        LonD = 0
        LonM = 0
        speed = 0
        for x in msgs:
            if( x.startswith("GPRMC") ): 
                if (x.find("V") != -1):
                    print("initializing")
                    break
                flag = 1   
                time = int(Str2Num(x[7:16]))
                LatD = Str2Num(x[19:21])
                LatM = Str2Num(x[21:29])
                LonD = Str2Num(x[32:35])
                LonM = Str2Num(x[35:43])
                speed = Str2Num(x[46:51])
    return([time, LatD, LatM, LonD, LonM, speed])


while(0):
    msg = GPS_Read_Line(0)
    
    for i in msg:
        print(i)
    sleep(0.5)
    
while(0):
    [t, Yd, Ym, Xd, Xm, v] = GPS_Read(0)
    print(t, Ym, Xm, v)

def DisplayRanking(data_in):
    global data_3, data_2, data_1
    if (data_in > data_1):
        data_3 = data_2
        data_2 = data_1
        data_1 = data_in
    elif (data_in > data_2):
        data_3 = data_2
        data_2 = data_in
    elif (data_in > data_3):
        data_3 = data_in

    LCD.Title("HW10 - Speedometer", White, Navy)
    LCD.Text2('Max Speeds:',10, 30, DkGreen, Navy)
    LCD.Text2('1:',50, 80, DkGreen, Navy)
    LCD.Number2(data_1,5,2,80, 80, White, Navy)
    LCD.Text2('mph',200, 80, DkGreen, Navy)
    
    LCD.Text2('2:',50, 130, DkGreen, Navy)
    LCD.Number2(data_2,5,2,80, 130, White, Navy)
    LCD.Text2('mph',200, 130, DkGreen, Navy)

    LCD.Text2('3:',50, 180, DkGreen, Navy)
    LCD.Number2(data_3,5,2,80, 180, White, Navy)
    LCD.Text2('mph',200, 180, DkGreen, Navy)
    
    LCD.Text2('Recent Max Speed:',10, 250, LtGreen, Navy)
    LCD.Number2(data_in,5,2,280, 250, White, Navy)
    LCD.Text2('mph',400, 250, DkGreen, Navy)
    
Navy = LCD.RGB(0, 0, 5)
White = LCD.RGB(150,150,150)
LtGreen = LCD.RGB(50,150,50)
DkGreen = LCD.RGB(0,100,0)
Yellow = LCD.RGB(150,150,0)
Pink = LCD.RGB(150,50,100)
Grey = LCD.RGB(50,50,50)
LCD.Init()
LCD.Clear(Navy)


data_3, data_2, data_1 = 0,0,0
DisplayRanking(0)

xref = 49.55054
yref = 52.11679
max_v = 0

f = open(FileName, "a")
Record_Flag = 0
while(1):
    [t, yd, ym, xd, xm, v] = GPS_Read(0)
    if(Button15.value() == 0):
        xref = xm
        yref = ym
        print('Home = Current GPS Position')
    if(Button14.value() == 0):
        Record_Flag = not Record_Flag
        if(Record_Flag):
            Beep()
            f = open(FileName, "a")
            print('File Open')
            max_v = 0
        else:
            Beep()
            sleep(0.1)
            Beep()
            f.close()
            print('File Closed')
            DisplayRanking(max_v)
            max_v = 0
        while(Button14.value() == 0):
            pass
        
    #msg = v  # meters
    v = v*1.15078
    if (max_v < v):
        max_v = v

    print(v)
    print(max_v)
    
    if(Record_Flag):
        f.write(str(v) + '\n')

    