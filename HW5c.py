import LCD_24x32 as LCD

from machine import ADC, Pin, PWM
from time import sleep_ms

a2dx = machine.ADC(0)
a2dy = machine.ADC(1)


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

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

def MotorEnable(MotorPin):
    MotorPin = 1
    return

def MotorDisable(MotorPin):
    MotorPin = 0
    return    
    
def DriveMotor(MotorPinA,MotorPinB,PowerIn):
    PowerIn = clamp(PowerIn,-100,100)
    sign = 1
    if (PowerIn <= 0):
        PowerIn = -PowerIn
        sign = 0
    Power = int(PowerIn*655.35)
    if (Power==0):
        MotorPinA.duty_u16(0)
        MotorPinB.duty_u16(0)
    elif (sign==1):
        MotorPinA.duty_u16(Power)
        MotorPinB.duty_u16(0)
    elif (sign==0):
        MotorPinA.duty_u16(0)
        MotorPinB.duty_u16(Power)
    return(Power,sign)

def StartLCD():
    LCD.Init()
    LCD.Clear(Navy)

Navy = LCD.RGB(0,0,10)
Yellow = LCD.RGB(150,150,0)

MotorEn = 20
MotorA = Pin(19, Pin.OUT)
MotorA = PWM(Pin(19))
MotorA.freq(100)
MotorB = Pin(18, Pin.OUT)
MotorB = PWM(Pin(18))
MotorB.freq(100)

#Code Start
by = int(0)
StartLCD()
LCD.Box(30, 80, 330, 210, Yellow)
LCD.Text4('Motor Speed:', 50, 100, Yellow, Navy)
    
while(1):
    Speed = SpeedControl(5)
    #Draw text
    if (Speed >= 0):
        direction = 'CW '
    else:
        direction = 'CCW'
    LCD.Text4(direction, 60, 170, Yellow, Navy)
    LCD.Number4(abs(Speed), 5, 3, 140, 170, Yellow, Navy)
    
    #Draw bar graph
    LCD.Box(422,150,442,by,Navy)
    by = int(150-Speed)
    LCD.Box(422,150,442,by,Yellow)

    #print(Speed)
    DriveMotor(MotorA,MotorB,Speed)
    sleep_ms(10)