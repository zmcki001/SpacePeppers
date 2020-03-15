import os
import glob
import time
import bme280 
import smbus2
from datetime import datetime
import csv


########################
# Set up all variables #
########################

#allows use of the sensors
port = 1
address = 0x77
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus,address)
bme280_data = bme280.sample(bus,address)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'

#name the CSV file for the data log
out_filename = '/home/pi/Desktop/temp.csv'

#initialize variables for counting hot readings
i1 = 0
i2 = 0
i3 = 0
i4 = 0

#insert device serial numbers here
sn1 = '28-0119127372e0'
sn2 = '28-0119127433c0'
sn3 = '28-011912741c54'
sn4 = '28-0119127601db'

#initialize all of the directories for the sensors
device_file1 = glob.glob(base_dir + sn1)[0] + '/w1_slave'
device_file2 = glob.glob(base_dir + sn2)[0] + '/w1_slave'
device_file3 = glob.glob(base_dir + sn3)[0] + '/w1_slave'
device_file4 = glob.glob(base_dir + sn4)[0] + '/w1_slave'

################################
# Routines to read each sensor #
################################
#Read Sensor 1
def read_temp_raw1():
	f = open(device_file1, 'r')
	lines1 = f.readlines()
	f.close()
	return lines1

def read_temp1():
	lines1 = read_temp_raw1()
	while lines1[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines1 = read_temp_raw1()
	equals_pos = lines1[1].find('t=')
	if equals_pos != -1:
		temp_string1 = lines1[1][equals_pos+2:]
		temp_c1 = float(temp_string1) / 1000.0
		return temp_c1

#Read Sensor 2
def read_temp_raw2():
	f = open(device_file2, 'r')
	lines2 = f.readlines()
	f.close()
	return lines2

def read_temp2():
	lines2 = read_temp_raw2()
	while lines2[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines2 = read_temp_raw2()
	equals_pos = lines2[1].find('t=')
	if equals_pos != -1:
		temp_string2 = lines2[1][equals_pos+2:]
		temp_c2 = float(temp_string2) / 1000.0
		return temp_c2

#Read Sensor 3
def read_temp_raw3():
        f = open(device_file3, 'r')
        lines3 = f.readlines()
        f.close()
        return lines3

def read_temp3():
        lines3 = read_temp_raw3()
        while lines3[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines3 = read_temp_raw3()
        equals_pos = lines3[1].find('t=')
        if equals_pos != -1:
                temp_string3 = lines3[1][equals_pos+2:]
                temp_c3 = float(temp_string3) / 1000.0
                return temp_c3

#Read Sensor 4
def read_temp_raw4():
        f = open(device_file4, 'r')
        lines4 = f.readlines()
        f.close()
        return lines4

def read_temp4():
        lines4 = read_temp_raw4()
        while lines4[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines4 = read_temp_raw4()
        equals_pos = lines4[1].find('t=')
        if equals_pos != -1:
                temp_string4 = lines4[1][equals_pos+2:]
                temp_c4 = float(temp_string4) / 1000.0
                return temp_c4


#############
# Main Loop #
#############

while True:
	
    currenttime = time.ctime()
    temp1 = read_temp1()
    temp2 = read_temp2()
    temp3 = read_temp3()
    temp4 = read_temp4()
    humidity = bme280_data.humidity
    pressure = bme280_data.pressure

    with open(out_filename, 'a') as f:
    	writer = csv.writer(f)
    	writer.writerow((
    	    currenttime,
    	    temp1,
    	    temp2,
    	    temp3,
            temp4,
            humidity,
            pressure,
	))
    open(out_filename).close()
	
    print("Room:    " + str(temp1) + "\nPlant 1: " + str(temp2) + "\nPlant 2: " + str(temp3) + "\nPlant 3: " + str(temp4) + "\nRH: " + str(humidity) + "\nPressure: " + str(pressure) + "\n" + currenttime + "\n\n")

    time.sleep(60)