import socket
import json
import urllib, urllib2
import time

UDP_IP_LISTEN = "172.16.44.150"
UDP_PORT_LISTEN = 9761

serverIP = "172.16.44.150"
nodeID = "123"
apikeyRW = "a02e6afadbe6a08eae4b327ef46f2ab3"
interval = 60

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP_LISTEN, UDP_PORT_LISTEN))

while True:
     data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
     print "Received:" + data
     if 'cTemp' in (data):
	json_string = data[2:]
        parsed_json = json.loads(json_string)
#	print data
        cTemp = parsed_json["cTemp"]
        prod = parsed_json["prod"]
        serial = parsed_json["serial"]
        type = parsed_json["type"]  
#        print parsed_json["cTarg"]
        params = "{" + str(prod) + "-" + str(serial) + "-" + str(type) + ":"  + str(cTemp) + "}"
        print "Sent:" + "http://" + serverIP + "/input/post.json?node=" + nodeID + "&json=" + params + "&apikey=" + apikeyRW
        urllib2.urlopen("http://" + serverIP + "/input/post.json?node=" + nodeID + "&json=" + params + "&apikey=" + apikeyRW)
        time.sleep(interval)



#data = json.loads(data)
#if data["prod"] == "tmr1ch":
# print data




