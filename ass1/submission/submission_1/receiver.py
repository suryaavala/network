from mysocket import *
import sys


port = int(sys.argv[1])
file_name = sys.argv[2]


s = mysocket()
s.bind(port)
s.set_logfile('Receive_log.txt')
#s.print_all()
s.accept_handshake()
#
# p = packet()
# p.build_header(['5967','5967','1',int(s.ack_nb)+1,'1','0','0','0'])
# s._send(p)
s.receive_file(file_name)
#print (int(s.ack_nb)+1, p.get_ack())
s.close()
