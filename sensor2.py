#!/usr/bin/env python2.7

import RPi.GPIO as GPIO
import time
import sys
import signal
import datetime
import Adafruit_BMP.BMP085 as BMP085
import urllib, urllib2

# emoncms details

serverIP = "172.16.44.120/emoncms"
apikeyRW = "f3e47cf1f7867c4b6dc3fec84ce905ba"
nodeID = "103"

# Default constructor will pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
# For the Beaglebone Black the library will assume bus 1 by default, which is
# exposed with SCL = P9_19 and SDA = P9_20.

# sensor = BMP085.BMP085()

# Optionally you can override the bus number:
#sensor = BMP085.BMP085(busnum=2)

# You can also optionally change the BMP085 mode to one of BMP085_ULTRALOWPOWER,
# BMP085_STANDARD, BMP085_HIGHRES, or BMP085_ULTRAHIGHRES.  See the BMP085
# datasheet for more details on the meanings of each mode (accuracy and power
# consumption are primarily the differences).  The default mode is STANDARD.

#sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

# Setup GPIO for pulse detection
GPIO.setmode(GPIO.BCM)

# Define global paramerters for exchanging in and out of interupt subroutine

counter = 0
litre = 0
value = 0
litrert = 0

# GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.
# Both ports are wired to connect to GND on button press.
# So we'll be setting up falling edge detection for both

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def printusage(progname):
        print progname + ' <filename> '
        print 'Example usage: ' 
        print progname + ' /path/to/mylogfile'
        sys.exit(-1)


#### get input parameters:

try:
        logfile = sys.argv[1]
#	print "your using this logifile > " +logfile
except:
        printusage(sys.argv[0])

# now we'll define two threaded callback functions
# these will run in another thread when our events are detected

def readvalue(myworkfile):
	try:
		f = open(myworkfile, 'ab+')             # open for reading. If it does not exist, create it
                value = float(f.readline().rstrip())
        except:
                value = 0

		f.close()       # close for reading

        return value


def writevalue(myworkfile,litre):
	f = open(myworkfile, 'w')
        f.write((str(litre)+ '\n'))                     # the value
        f.write((str(datetime.datetime.now())+ '\n'))   # timestamp
        f.close()


def signal_handler(signal, frame): 
   #      print('You pressed Ctrl+C, so exiting')
	 #writevalue(logfile, litre) 
	 GPIO.cleanup() 
         sys.exit(0)           

def my_callback(channel):
#	print "my_callback" + str(litre)
	global counter
	global litre
	global litrert		
#	print "my_callback" + str(litre)
	if counter == 66:
		litre += 0.2
		litrert += 0.2 
		counter = 0
	else:
		counter += 1
    	return litre, counter, litrert

def send2emon():
	global litrert
	try:
		urllib2.urlopen("http://" + serverIP + "/input/post.json?node=" + nodeID + "&json=" + params + "&apikey=" + apikeyRW)
	except:
		print "can't send - check server"
	litrert = 0
	return


litre = readvalue(logfile) # read in the value (or create)
GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback)
signal.signal(signal.SIGINT, signal_handler)    # SIGINT = interrupt by CTRL-C
 
while True: 
	print "litres so far: " +str(litre),
	print "counter is: " +str(counter) 
	bmp180_temp = 22.2 #sensor.read_temperature()
	bmp180_pressure = 1035 #sensor.read_pressure()
		
	params = ("{" + "Water(Lt)" + ":"  + str(litre) + "," + "Water(Lt)RT" + ":"  + str(litrert) + "," + "Temp(C)" + ":"  + str(bmp180_temp) + "," + "Pressure(Pa)" + ":"  + str(bmp180_pressure) + "}" )
	send2emon()
	print "Sent:" + "http://" + serverIP + "/input/post.json?node=" + nodeID + "&json=" + params + "&apikey=" + apikeyRW
	
	# write value to file
        writevalue(logfile,litre)
#	print "writing to" + logfile + " " + str(litre)
   	time.sleep(5)


