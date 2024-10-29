import machine, onewire, ds18x20, time
from machine import Pin
ds_pin = machine.Pin(4, Pin.PULL_UP)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
print('Found DS devices: ', roms)

file1 = open("TemperatureData.txt", "wt")
t = 0

#Temperature test loop
while 1:
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
        print(rom)
        tempC = ds_sensor.read_temp(rom)
        print(tempC)
    time.sleep(5)

samples = 30
while (t<samples):
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
        print(rom)
        tempC = ds_sensor.read_temp(rom)
        print(tempC)
    time.sleep(5)
    file1.write(str(tempC))
    file1.write("\n")
    t+=1

file1.close()
print('File Closed')