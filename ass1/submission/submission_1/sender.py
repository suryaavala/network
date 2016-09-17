from mysocket import *
import sys

r_host = str(sys.argv[1])
r_port = int(sys.argv[2])
file_name = sys.argv[3]
mws = int(sys.argv[4])
mss = int(sys.argv[5])
timeout = int(sys.argv[6])/1000
pdrop = float(sys.argv[7])
seed = int(sys.argv[8])

s = mysocket()
s.connect((r_host,r_port))
s.set_timeout(timeout)
s.set_param(mss, mws, pdrop, seed)

s.set_logfile('Sender_log.txt')
#s.print_all()
# p = packet()
# p.build_payload('surya')
# print(s._send(p))
#print (s.init_handshake())
#s.set_param(50, 200, 0, 50)
s.init_handshake()
#s.print_all
s.send_file(file_name)
#s.print_all()
s.close()

#print ('ran')
