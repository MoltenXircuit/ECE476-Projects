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



#x = [0]*samples

StartLCD()
LCD.Title("HW8 - Weather Station", White, Navy)
LCD.Text2('Temperature: ',40, 50, DkGreen, Navy)
LCD.Text2('Humidity: ',40, 100, LtGreen, Navy)
LCD.Text2('Air Pressure: ',40, 150, Yellow, Navy)
# Initialize BME280 sensor
bme = BME280.BME280(i2c=i2c)
while(1):
    #for i in x:
    while (flag == 0):
        pass
    flag = 0
    # Read sensor data
    tempC = bme.temperature
    hum = bme.humidity
    pres = bme.pressure
    
    # Convert temperature to fahrenheit
    tempF = (bme.read_temperature()/100) * (9/5) + 32
    tempF = str(round(tempF, 2)) + 'F'
    
    LCD.Text2(tempF, 240, 50, DkGreen, Navy)
    LCD.Text2(hum, 200, 100, LtGreen, Navy)
    LCD.Text2(pres, 260, 150, Yellow, Navy)

