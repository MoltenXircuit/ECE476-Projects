from machine import ADC, Pin, PWM
from time import sleep_ms

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

a2d0 = ADC(1)

Button1 = Pin(14, Pin.IN, Pin.PULL_UP)
Button2 = Pin(15, Pin.IN, Pin.PULL_UP)
MotorEn = 20
MotorA = Pin(19, Pin.OUT)
MotorA = PWM(Pin(19))
MotorA.freq(100)
MotorB = Pin(18, Pin.OUT)
MotorB = PWM(Pin(18))
MotorB.freq(100)

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

while(1):
    if (Button1.value()==0):
        print(DriveMotor(MotorA,MotorB,90))
        sleep_ms(100)
    #print(DriveMotor(MotorA,MotorB,0))
    #sleep_ms(1000)
    if (Button2.value()==0):
        print(DriveMotor(MotorA,MotorB,-90))
        sleep_ms(100)



