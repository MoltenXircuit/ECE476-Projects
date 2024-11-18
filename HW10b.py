from machine import Pin, PWM
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral


#----------------Bluetooth Code----------------
ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble)

LED0 = Pin("LED", Pin.OUT)

def on_rx(data):
    numflag,negative, number = 0,0,0
    print("Data received: ", data[:-2])
    numbers = []
    for char in str(data[:-2]):
        if char == '-':
            #negate next number if there is one
            negative = 1
        elif char.isdigit():
            numflag = 1
            #shift number in
            number = number * 10
            number = number+int(char)
            if negative == 1:
                number = number * -1
            negative = 0
        else:
            #end of number
            if numflag == 1:
                numflag = 0
                numbers.append(number)
                number = 0
            #reset negative if no number
            negative = 0

    DriveMotor(MotorA,MotorB,numbers[0])
    sp.send("speed set to " +  str(numbers[0]) + "\r\n")
    print("speed set to :", numbers[0])
    
    if data == b'LED0\r\n':
        LED0.toggle()

#----------------Motor Code----------------

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

MotorEn = 20
MotorA = Pin(19, Pin.OUT)
MotorA = PWM(Pin(19))
MotorA.freq(100)
MotorB = Pin(18, Pin.OUT)
MotorB = PWM(Pin(18))
MotorB.freq(100)

#------------------Main Loop---------------------

while(1):
    if sp.is_connected():
        sp.on_write(on_rx)
    else:
        #disable motor
        DriveMotor(MotorA,MotorB,0)


