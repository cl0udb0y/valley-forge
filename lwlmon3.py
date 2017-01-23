import socket
import json
import urllib, urllib2
import time
import logging

import logging
logger = logging.getLogger('lwlmon')
hdlr = logging.FileHandler('/var/tmp/lwlmon.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

UDP_IP_LISTEN = "172.16.44.110"
UDP_PORT_LISTEN = 9761

serverIP = "172.16.44.120/emoncms"
apikeyRW = "f3e47cf1f7867c4b6dc3fec84ce905ba"

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP_LISTEN, UDP_PORT_LISTEN))

def send2emon():
	try:
		urllib2.urlopen("http://" + serverIP + "/input/post.json?node=" + nodeID + "&json=" + params + "&apikey=" + apikeyRW)
	except: 
		logger.error("can't send to server")
	return

while True:
     data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
     print "Received:" + data
     nodeID = "100"
     if 'cTemp' in (data):
	json_string = data[2:]
        parsed_json = json.loads(json_string)
        prod = parsed_json["prod"]

        if prod == 'valve':
	 nodeID = "101"
         print nodeID

        elif prod == 'tmr1ch':
         nodeID = "100"
         print nodeID

        else:
         nodeID = 999
         print nodeID

        cTemp = parsed_json["cTemp"]
        prod = parsed_json["prod"]
        serial = parsed_json["serial"]
        type = parsed_json["type"]
	lwl_time = parsed_json["time"]
        batt = parsed_json["batt"]
        cTarg = parsed_json["cTarg"]
        output = parsed_json["output"]

        params = ("{" + "Current" + ":"  + str(cTemp) + "," + "Target" + ":"  + str(cTarg) + "," + "Output" + ":"  + str(output) + "," + "Battery" + ":"  + str(batt) + "}" )

        #print "Sent:" + "http://" + serverIP + "/input/post.json?node=" + nodeID + "&json=" + params + "&apikey=" + apikeyRW
        send2emon()

	#urllib2.urlopen("http://" + serverIP + "/input/post.json?node=" + nodeID + "&json=" + params + "&apikey=" + apikeyRW)

# + str(prod) + "-" + str(serial) + "-" + str(type) + ":"
