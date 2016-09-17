import time
from socket import *
import sys

nb_ping  = 1
host = sys.argv[1]
port = sys.argv[2]

#print (host, port)

while nb_ping < 11:

    sock = socket(AF_INET, SOCK_DGRAM)

    sock.settimeout(1)

    start_time, l_start_time = time.time(), time.localtime()

    timestamp = str(l_start_time.tm_year) +str(l_start_time.tm_mon) + \
                str(l_start_time.tm_mday) + str(l_start_time.tm_hour) +\
                str(l_start_time.tm_min) + str(l_start_time.tm_sec)

    message = 'PING'+ ' ' + str(nb_ping) + ' ' + timestamp + '\r\n'

    address = (str(host), int(port))


    sock.sendto(message.encode('ascii'), address)


    try:
        r_message, server = sock.recvfrom(1024)
        end_time = time.time()
        rtt = end_time-start_time
        r_message = r_message.decode('ascii')
        #print (r_message  + ' ' + str(nb_ping) + ' from server ' + str(server))
        print ('ping to ' + host+', seq = '+ str(nb_ping) +\
               ', rtt = ' +str(round(rtt*1000,2))+' ms')
    except timeout:
        print ('REQUEST TIMED OUT')

    nb_ping += 1
