import socket
import json
import time
import socket
import json

#list of devices
devices = ['R1Dh', 'R2Dh', 'R3Dh','R4Dh']
# 'R3Dh', 'R4Dh']

#this is the code you received when pairing this device
LWL_PAIR_CODE = "666"
RANDOM = "123"
BANG = "!"
LWL_REQ = "F*r"

#Send
UDP_IP_SEND = "172.16.44.148"
UDP_PORT_SEND = 9760

while True:
 for device in devices:
  MESSAGE = LWL_PAIR_CODE + "," + RANDOM + "," + BANG + device + LWL_REQ
  print "message:", MESSAGE
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.sendto(MESSAGE, (UDP_IP_SEND, UDP_PORT_SEND))
  print "sleeping..."
  time.sleep(30)



