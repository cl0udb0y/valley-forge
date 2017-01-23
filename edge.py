#!/usr/bin/env python2.7
# script by Alex Eames http://RasPi.tv
# http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3
import RPi.GPIO as GPIO
import time
import sys
import signal
import datetime

GPIO.setmode(GPIO.BCM)

litre = 0
counter = 0

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
except:
        printusage(sys.argv[0])

# now we'll define two threaded callback functions
# these will run in another thread when our events are detected

def readvalue(myworkfile):
        global litre
	try:
                f = open(myworkfile, 'ab+')             # open for reading. If it does not exist, create it
                litre = int(f.readline().rstrip())      # read the first line; it should be an integer value
        except:
                litre = 0                               # if something went wrong, reset to 0
        #print "old value is", value
        f.close()       # close for reading
        return value


def writevalue(myworkfile,value):
        f = open(myworkfile, 'w')
        f.write((str(litre)+ '\n'))                     # the value
        f.write((str(datetime.datetime.now())+ '\n'))   # timestamp
        f.close()


def signal_handler(signal, frame): 
         print('You pressed Ctrl+C, so exiting')
	 GPIO.cleanup() 
         sys.exit(0)           

def my_callback(channel):
	global counter
	global litre		
	if counter == 66:
		litre += 0.2
		counter = 0
	else:
		counter += 1
    	return litre

GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback)

while True: 
	print "litres so far: " +str(litre)

        # write value to file
        writevalue(logfile,litre)
   	time.sleep(5)


