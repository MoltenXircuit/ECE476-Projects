import LCD_24x32 as LCD

from machine import ADC
from time import sleep_ms

a2dx = machine.ADC(0)
a2dy = machine.ADC(1)

Navy = LCD.RGB(0,0,10)
Yellow = LCD.RGB(150,150,0)


def joystickRead():
    x = a2dx.read_u16() 
    y = a2dy.read_u16() 
    return(x,y)

def SpeedControl(deadband):
    kn = 200 / 65535
    x,y = joystickRead()
    speed = (kn * y) - 100
    if (-deadband < speed and speed < deadband):
        speed = 0
    return(speed)

while(0):
    Speed = SpeedControl(10)
    print(Speed)
    sleep_ms(200)

def StartLCD():
    LCD.Init()
    LCD.Clear(Navy)


#Code Start
by = int(0)
StartLCD()
LCD.Box(30, 80, 330, 210, Yellow)

while(1):
    Speed = SpeedControl(10)
    #Draw text
    if (Speed >= 0):
        direction = 'CW '
    else:
        direction = 'CCW'
    LCD.Text4('Motor Speed:', 50, 100, Yellow, Navy)
    LCD.Text4(direction, 60, 170, Yellow, Navy)
    LCD.Number4(abs(Speed), 5, 3, 140, 170, Yellow, Navy)

    #Draw bar graph
    LCD.Box(422,150,442,by,Navy)
    by = int(150-Speed)
    LCD.Box(422,150,442,by,Yellow)

    print(Speed)
    sleep_ms(200)
