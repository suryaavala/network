import time
from socket import *
import sys


host = sys.argv[1]
#port = sys.argv[2]
#message = sys.argv[2]

sock = socket(AF_INET, SOCK_DGRAM)
sock.settimeout(1)
sock.bind((str(host),0))

print(sock.getsockname(),sock.getsockname()[1])
port = 5967

for message in 'abcdefghijklmnopqrstuvwxyz':
    sock.sendto(message.encode('ascii'), (str(host), int(port)))
    print ("sent message: {} to address {}".format(message, (host,port)))

print('*******sleeping*********')
#time.sleep(10)
print ('*********woke up**********')

for message in 'abcdefghijklmnopqrstuvwxyz':
    sock.sendto(message.encode('ascii'), (str(host), int(port)))
    print ("sent message: {} to address {}".format(message, (host,port)))

#message_list = ["souce#","dest#","seq_nb","ack nb","ACK","SYN","FIN","RST",str("surya avinash avala data sfkjgd tjgt df".encode('ascii'))]
pay_load = "surya avinash avala data sfkjgd tjgt df"
header = ["souce#","dest#","seq_nb","ack nb","ACK","SYN","FIN","RST"]
message = ("+".join(header)+"+"+pay_load)
print("final message: {}".format(message))

sock.sendto(message.encode("ascii"), (str(host), int(port)))
print ("sent message: {} to address {}".format(message, (host,port)))
