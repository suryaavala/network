#Surya Avinash Avala, z5096886
#required classes mysocket.py, packet.py
from mysocket import *
import sys


port = int(sys.argv[1])
file_name = sys.argv[2]


r = mysocket()
r.bind(port)

r.set_logfile('Receiver_log.txt')

r.accept_handshake()

r.receive_file(file_name)

r.close()
