import board
import busio
import adafruit_tsl2591
import time
import csv

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tsl2591.TSL2591(i2c)

out_filename = "/home/pi/Desktop/lux.csv"

while True:
    
    localtime =time.asctime( time.localtime(time.time()) )
    luxvalue = format(sensor.lux)
    
    with open(out_filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow((
            localtime,
            luxvalue,
    ))
    open(out_filename).close()

    print('Light: ' + str(luxvalue))
    time.sleep(30)
