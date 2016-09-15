from socket import *
import time
import random
from packet import *
import pickle


class mysocket:

    def __init__(self):
        self.sock = socket(AF_INET,SOCK_DGRAM)
        self.sock.bind(('',0))
        self.sport = self.sock.getsockname()[1]
        self.dip = None
        self.dport = None
        self.timeout = None
        #self.seq_nb, self.ack_nb

#socket send, receive, handshake, change param.

    def connect(self,addr):
        '''
        Input:  Takes a tuple (ip,port)
        Output: Assign those values to the appropriate variables
        '''
        self.dip = str(addr[0])
        self.dport = str(addr[1])
        return

    def set_timeout(self, timeout):
        '''
        Input:  Takes timeout value in sec (int)
        Output: Sets the timeout of the socket
        '''
        self.timeout = int(timeout)
        self.sock.settimeout(self.timeout)
        return

    def close(self):
        '''
        Input:  None
        Output: Closes circuit
        '''
        self.sock.close()
        return

    def print_all(self):
        '''
        Input:  None
        Output: Prints values of all socket variable
        '''
        print("sock: {}\nsource port: {}\ndest ip: {}\ndest port {}\ntimeout: {}".format(self.sock, self.sport,self.dip,self.dport,self.timeout))
        return



if __name__ == '__main__':

    print ("running")
    s = mysocket()
    s.connect(('127.0.0.1',5678))
    s.set_timeout(10)
    s.print_all()
    s.get_param('sport')
    s.close()

    print ('ran')
