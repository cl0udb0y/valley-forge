#!/usr/bin/env python

import RPi.GPIO as GPIO
import datetime
import sys
import signal
import time
import urllib, urllib2

serverIP = "172.16.44.120/emoncms"
apikeyRW = "f3e47cf1f7867c4b6dc3fec84ce905ba"
nodeID = "102"

#verbose = True		# global variable

############################################################################################################
############################################################################################################

def printusage(progname):
        print progname + ' <gpio-pin-number> <filename> [debug]'
        print 'Example usage: ' 
	print progname + ' 23 /path/to/mylogfile'
        print progname + ' 23 /path/to/mylogfile debug'
	sys.exit(-1)

def signal_handler(signal, frame):
        if verbose:
		print('You pressed Ctrl+C, so exiting')
	GPIO.cleanup()
        sys.exit(0)


def readvalue(myworkfile):
	try:
		f = open(myworkfile, 'ab+')		# open for reading. If it does not exist, create it
		value = int(f.readline().rstrip())	# read the first line; it should be an integer value
	except:
		value = 0				# if something went wrong, reset to 0
	#print "old value is", value
	f.close()	# close for reading
	return value


############################################################################################################

######### Initialization
######### Initialization


#### get input parameters:

try:
	mygpiopin = int(sys.argv[1])
	logfile = sys.argv[2]
except:
	printusage(sys.argv[0])

verbose = False
try:
	if sys.argv[3] == 'debug':
		verbose = True
		print "Verbose is On"
	else:
		printusage(sys.argv[0])
except:
	pass

#### if verbose, print some info to stdout

if verbose:
	print "GPIO is " + str(mygpiopin)
	print "Logfile is " + logfile
	print "Current value is " + str(readvalue(logfile))

#### Setup

signal.signal(signal.SIGINT, signal_handler)	# SIGINT = interrupt by CTRL-C


########## Main Loop 

while True:
	counter=readvalue(logfile)
	params = ("{" + "Pulses" + ":"  + str(counter) + "}" )

        #print "Sent:" + "http://" + serverIP + "/input/post.json?node=" + nodeID + "&json=" + params + "&apikey=" + apikeyRW
        urllib2.urlopen("http://" + serverIP + "/input/post.json?node=" + nodeID + "&json=" + params + "&apikey=" + apikeyRW)
	time.sleep( 30 )	
	
############################################################################################################
############################################################################################################



