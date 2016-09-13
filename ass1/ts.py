import time
from socket import *
import sys


host = sys.argv[1]
#port = sys.argv[2]
message = sys.argv[2]

sock = socket(AF_INET, SOCK_DGRAM)
sock.settimeout(1)
sock.bind((str(host),0))

#port = sock.getsockname()[1]
port = 5967
sock.sendto(message.encode('ascii'), (str(host), int(port)))

print (port, type(port), host, type(host))
