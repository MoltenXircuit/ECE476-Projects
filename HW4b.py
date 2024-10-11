from machine import ADC, Pin, PWM
from time import sleep_ms

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

# GP14 = push button (decrease angle)
# GP15 = push button (increae angle)
# GP16 = control input to digital servo motor
a2d0 = ADC(2)


Up = Pin(15, Pin.IN, Pin.PULL_UP)
Down = Pin(14, Pin.IN, Pin.PULL_UP)

Control = Pin(19, Pin.OUT)
Control = PWM(Pin(19))
Control.freq(50)

lightMax = 0
servoMax = 1_500_000
servoCurrent = 1_500_000
scale = 4200
k = 3.3 / 65520
def lightRead():
    a = a2d0.read_u16() >> 4
    b = clamp((a/scale),0,1)
    V0 = a * k
    #print(a, b, V0)
    return(b)

while(0):
    print(lightRead())
    sleep_ms(1000)
    
def Scan():
    global lightMax
    global servoMax
    servoCurrent = servoMax
    lightMax = 0
    lightCurrent = lightRead()
    while(servoCurrent < 2_500_000):
        servoCurrent += 20_000
        Control.duty_ns(servoCurrent)
        sleep_ms(20)
        #print(servoCurrent)
    sleep_ms(500)
    while(servoCurrent > 500_000):
        servoCurrent -= 10_000
        Control.duty_ns(servoCurrent)
        lightCurrent = lightRead()
        if(lightMax < lightCurrent):
            lightMax = lightCurrent
            servoMax = servoCurrent
        sleep_ms(20)
        #print(lightMax,servoMax)
    return


while(1):
    lightMax = 0
    Scan()
    t = 0
    print(lightMax,servoMax)
    while(t < 3000):        
        Control.duty_ns(servoMax)
        sleep_ms(1)
        t += 1

