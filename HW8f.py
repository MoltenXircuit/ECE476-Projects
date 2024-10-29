from machine import Pin, Timer, I2C
from time import sleep
import LCD_24x32 as LCD
import BME280
samplingFreq = 1
samplingSeconds = 60
samples = samplingSeconds * samplingFreq

#------------Timer Interrupt Setup----------
tim = Timer()
flag = 0

def tic(timer):
    global flag
    flag = 1


tim.init(freq=samplingFreq, mode=Timer.PERIODIC, callback=tic)


pin = Pin(15, Pin.IN, Pin.PULL_UP)

state = 0
interrupt_flag = 0
def IntServe(pin):
    global state, interrupt_flag
    interrupt_flag=1
    state = (state + 1) % 3

pin.irq(trigger=Pin.IRQ_FALLING, handler=IntServe)
#LCD Code

def StartLCD():
    LCD.Init()
    LCD.Clear(Navy)
Navy = LCD.RGB(0, 0, 5)
LtBlue = LCD.RGB(100, 100, 150)
White = LCD.RGB(150,150,150)
LtGreen = LCD.RGB(50,150,50)
DkGreen = LCD.RGB(0,100,0)
Yellow = LCD.RGB(150,150,0)
Pink = LCD.RGB(150,50,100)
Grey = LCD.RGB(50,50,50)

Xmin = 10
Xmax = 470
Ymin = 30
Ymax = 280
kX = float((Xmax - Xmin)/samples)
kY = float((Ymax - Ymin)/100)
def DrawGraph():
    LCD.Clear(Navy)
    LCD.Title("HW8 - Weather Station", White, Navy)
    Divisions = 8
    dX = (Xmax - Xmin)/Divisions
    dY = (Ymax - Ymin)/Divisions
    for i in range(0,Divisions+1):
        LCD.Line(Xmin, int(Ymin+i*dY), Xmax, int(Ymin+i*dY), Grey)
        LCD.Line(int(Xmin+i*dX), Ymin, int(Xmin+i*dX), Ymax, Grey)

# Initialize I2C communication
i2c = I2C(id=0, scl=Pin(1), sda=Pin(0), freq=10000)

tempData = [0] * (samples+1)
humData = [0] * (samples+1)
presData = [0] * (samples+1)

StartLCD()
DrawGraph()
LCD.Text("Temperature", 20, 290, Pink, Navy)
LCD.Text("Humidity", 180, 290, Grey, Navy)
LCD.Text("Air Pressure", 340, 290, Grey, Navy)
# Initialize BME280 sensor
bme = BME280.BME280(i2c=i2c)
time = 0
while (time <= samples):
    if (flag == 1):
        flag = 0

        # Convert temperature to fahrenheit
        tempF = (bme.read_temperature()/100) * (9/5) + 32
        # Read and Store sensor data
        tempData[time] = tempF
        humData[time] = float(bme.read_humidity())
        presData[time] = float((bme.read_pressure()-24_500_000)/10_000)


        if (state == 0 and time>0):
            LCD.Line(Xmin+int((time-1)*kX), Ymax-int(tempData[time-1]*kY), Xmin+int(time*kX), Ymax-int(tempData[time]*kY), Pink)
        elif state == 1:
            LCD.Line(Xmin+int((time-1)*kX), Ymax-int(humData[time-1]*kY), Xmin+int(time*kX), Ymax-int(humData[time]*kY), LtBlue)
        elif state == 2:
            LCD.Line(Xmin+int((time-1)*kX), Ymax-int(presData[time-1]*kY), Xmin+int(time*kX), Ymax-int(presData[time]*kY), Yellow)
        time = time+1
    #redraw graph for new data type
    if (interrupt_flag == 1):
        interrupt_flag = 0
        DrawGraph()
        if state == 0:
            LCD.Text("Temperature", 20, 290, Pink, Navy)
            LCD.Text("Humidity", 180, 290, Grey, Navy)
            LCD.Text("Air Pressure", 340, 290, Grey, Navy)
            for t in range(1,time):
                LCD.Line(Xmin+int((t-1)*kX), Ymax-int(tempData[t-1]*kY), Xmin+int(t*kX), Ymax-int(tempData[t]*kY), Pink)
        elif state == 1:
            LCD.Text("Temperature", 20, 290, Grey, Navy)
            LCD.Text("Humidity", 180, 290, LtBlue, Navy)
            LCD.Text("Air Pressure", 340, 290, Grey, Navy)
            for t in range(1,time):
                LCD.Line(Xmin+int((t-1)*kX), Ymax-int(humData[t-1]*kY), Xmin+int(t*kX), Ymax-int(humData[t]*kY), LtBlue)
        elif state == 2:
            LCD.Text("Temperature", 20, 290, Grey, Navy)
            LCD.Text("Humidity", 180, 290, Grey, Navy)
            LCD.Text("Air Pressure", 340, 290, Yellow, Navy)
            for t in range(1,time):
                LCD.Line(Xmin+int((t-1)*kX), Ymax-int(presData[t-1]*kY), Xmin+int(t*kX), Ymax-int(presData[t]*kY), Yellow)
    
DrawGraph()
LCD.Text("Temperature", 20, 290, Pink, Navy)
LCD.Text("Humidity", 180, 290, LtBlue, Navy)
LCD.Text("Air Pressure", 340, 290, Yellow, Navy)
# Draw data


for t in range(1,samples+1):
    LCD.Line(Xmin+int((t-1)*kX), Ymax-int(tempData[t-1]*kY), Xmin+int(t*kX), Ymax-int(tempData[t]*kY), Pink)
    LCD.Line(Xmin+int((t-1)*kX), Ymax-int(humData[t-1]*kY), Xmin+int(t*kX), Ymax-int(humData[t]*kY), LtBlue)
    LCD.Line(Xmin+int((t-1)*kX), Ymax-int(presData[t-1]*kY), Xmin+int(t*kX), Ymax-int(presData[t]*kY), Yellow)

