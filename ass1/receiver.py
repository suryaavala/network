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
