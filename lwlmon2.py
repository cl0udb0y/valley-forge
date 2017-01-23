import socket
import json
UDP_IP_LISTEN = "172.16.44.149"
UDP_PORT_LISTEN = 9761

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP_LISTEN, UDP_PORT_LISTEN))

#json_string = data 
#def is_jason(json_string):

counter = 0
while True:
     data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
     if data[0][0] != "*":
       print "!"
     else:
       json_string = data[2:]
       if 'prod' in (data):
	parsed_json = json.loads(json_string)
	print parsed_json


#data = json.loads(data)
#if data["prod"] == "tmr1ch":
# print data




