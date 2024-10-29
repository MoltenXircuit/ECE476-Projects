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


#LCD Code

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



# Initialize I2C communication
i2c = I2C(id=0, scl=Pin(1), sda=Pin(0), freq=10000)


B0 = Pin(15, Pin.IN, Pin.PULL_UP)



tempData = [0] * (samples+1)
humData = [0] * (samples+1)
presData = [0] * (samples+1)

StartLCD()
LCD.Title("HW8 - Weather Station", White, Navy)
LCD.Text2('Temperature: ',40, 50, DkGreen, Navy)
LCD.Text2('Humidity: ',40, 100, LtGreen, Navy)
LCD.Text2('Air Pressure: ',40, 150, Yellow, Navy)
# Initialize BME280 sensor
bme = BME280.BME280(i2c=i2c)
for i in range(0,samples+1):
    while (flag == 0):
        pass
    flag = 0
    # Read sensor data
    tempC = bme.temperature
    hum = bme.humidity
    pres = bme.pressure

    # Convert temperature to fahrenheit
    tempF = (bme.read_temperature()/100) * (9/5) + 32
    # Store sensor data
    tempData[i] = tempF
    humData[i] = float(bme.read_humidity())
    presData[i] = float((bme.read_pressure()-24_500_000)/10_000)

    tempF = str(round(tempF, 2)) + 'F'

    LCD.Text2(tempF, 240, 50, DkGreen, Navy)
    LCD.Text2(hum, 200, 100, LtGreen, Navy)
    LCD.Text2(pres, 260, 150, Yellow, Navy)
# Draw graph
LCD.Clear(Navy)
Xmin = 10
Xmax = 470
Ymin = 10
Ymax = 280
Divisions = 8
dX = (Xmax - Xmin)/Divisions
dY = (Ymax - Ymin)/Divisions
for i in range(0,Divisions+1):
    LCD.Line(Xmin, int(Ymin+i*dY), Xmax, int(Ymin+i*dY), Grey)
    LCD.Line(int(Xmin+i*dX), Ymin, int(Xmin+i*dX), Ymax, Grey)
LCD.Text("Temperature", 20, 290, DkGreen, Navy)
LCD.Text("Humidity", 180, 290, LtGreen, Navy)
LCD.Text("Air Pressure", 340, 290, Yellow, Navy)
# Draw data
kX = float((Xmax - Xmin)/samples)
kY = float((Ymax - Ymin)/100)

for t in range(1,samples+1):
    LCD.Line(Xmin+int((t-1)*kX), Ymax-int(tempData[t-1]*kY), Xmin+int(t*kX), Ymax-int(tempData[t]*kY), DkGreen)
    LCD.Line(Xmin+int((t-1)*kX), Ymax-int(humData[t-1]*kY), Xmin+int(t*kX), Ymax-int(humData[t]*kY), LtGreen)
    LCD.Line(Xmin+int((t-1)*kX), Ymax-int(presData[t-1]*kY), Xmin+int(t*kX), Ymax-int(presData[t]*kY), Yellow)
