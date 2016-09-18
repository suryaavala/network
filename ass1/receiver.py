from mysocket import *
import sys


port = int(sys.argv[1])
file_name = sys.argv[2]


s = mysocket()
s.bind(port)
s.set_logfile('Receive_log.txt')

s.accept_handshake()

s.receive_file(file_name)

s.close()
