import time
from socket import *
import sys


ip = "127.0.0.1"
port = 5967

sock = socket(AF_INET, # Internet
                     SOCK_DGRAM) # UDP
sock.bind((ip, port))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #print ("received message:", data.decode('ascii'))
    #print ("from address:", addr)
    data = data.decode('ascii')
    print ("received message: {} to address {}".format(data,addr))

    if ('final message' in  data):
        #time.sleep(5)
        sock.sendto("received final".encode('ascii'),addr)
        print ("sent ack for final to {}".format(addr))
        break
