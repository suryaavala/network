#All functions for stp protocol reside here
from socket import *

class stp_socket:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sip, self.sport = self.sock.getsockname()
        self.dip = None
        self.dport = None

    def connect(self,*dest):
        self.dip = str(dest[0])
        self.dport = str(dest[1])

    def send(self,message):
        self.sock.sendto(message.encode('ascii'),(str(self.dip),int(self.dport)))
        return

    #def hand_shake():
    def print_all(self):
        print (self.sock, self.sip,self.sport,self.dip,self.dport,sep="***")

    def close(self):
        self.sock.close()
        return



#def hand_shake(sip,sport,dip,dport,sockname):
if __name__ == '__main__':
    s = stp_socket()
    s.connect('127.0.0.1',5967)
    s.print_all()
    for i in range(10):
        s.send(str(i)+" testing my socket")
    s.close()
