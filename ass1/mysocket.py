from socket import *
import time
import random
from packet import *
import pickle


class mysocket:

    def __init__(self):
        self.sock = socket(AF_INET,SOCK_DGRAM)
        #self.sock.bind(('',0))
        self.sport = None
        self.dip = None
        self.dport = None
        self.timeout = None
        #self.seq_nb, self.ack_nb

#socket send, receive, handshake, change param.
    def bind(self,port=None):
        '''
        Input:  Optional:   Takes port number
        Output: Binds the socket to the port given,
                                    randomly assigned by OS if none
        Note: Sender binds automatically when we call connect. But we have to bind manually for receiver.
        '''
        if port:
            self.sock.bind(('',port))
        else:
            self.sock.bind(('',0))
        self.sport = self.sock.getsockname()[1]
        return


    def connect(self,addr):
        '''
        Sender function
        Input:  Takes a tuple (ip,port)
        Output: Assign those values to the appropriate variables
        '''
        self.dip = str(addr[0])
        self.dport = str(addr[1])
        self.bind()
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

    def _send(self,pack):
        '''
        Input:  Takes final packet object
        Output: Sends the payload accross
        Note:   Packet has to be built
        '''
        encoded_pack = pickle.dumps(pack)
        sent_bytes = self.sock.sendto(encoded_pack, (str(self.dip),int(self.dport)))
        if (len(encoded_pack) != sent_bytes):
                return False
        return True

    def _receive(self):
        '''
        Input:  None
        Output: Returns the packet object which was received
        '''
        try:
            msg, addr = self.sock.recvfrom(1024)
            pack = pickle.loads(msg)
        except timeout:
            return None
        return pack

###########have to implement a custom buffer function for out of order packets##






if __name__ == '__main__':

    print ("running")
    s = mysocket()
    s.connect(('127.0.0.1',5678))
    s.set_timeout(10)
    s.print_all()
    p = packet()
    p.build_payload('surya')
    print(s._send(p))
    s.close()

    print ('ran')
