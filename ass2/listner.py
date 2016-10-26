from socket import *
import pickle
import time
ip = '127.0.0.1'
sock = socket(AF_INET,SOCK_DGRAM)
sock.bind((ip,2003))
while True:
    msg, addr = sock.recvfrom(1024)
    pack = pickle.loads(msg)
    print (time.time(),pack)
