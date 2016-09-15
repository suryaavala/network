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
        self.seq_nb = str(int(random.random()*100))
        self.ack_nb = str(-1)
        #can implement self.sock_status to keep track of connection

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

    def init_handshake(self):
        '''
        Sender function initiating the hand shake and establishing the connection.
        Socket has to be opened (opened by __init__) and the connection to destination must have been established (done by connect())

        Input:  None
        Output: True or False depending on when the connection was established successfully
        '''
        #SYN + sequence number (X: sender's sequence number)
        #listen for SYNACK + ack number (x+1) + sequence number (Y: receiver's seq num)
        #Send ACK + acknum (Y+1)

        if not (self.sport and self.dip and self.dport and self.seq_nb and self.ack_nb):
            return False

        #sending SYN
        syn_sent = False
        while (not syn_sent):
            pack = packet()
            pack.build_header([self.sport,self.dport,self.seq_nb,self.ack_nb,0,1,0,0])
            pack.build_payload("")
            syn_sent = self._send(pack)

        #listen for ACK
        synack_received = False
        p = self._receive()
        print (p.get_packet())
        return

    def accept_handshake(self):
        '''
        Receiver function accepting the hand shake (which was initiated by Sender) and establishing the connection.
        Socket has to be opened (opened by __init__) and must have been bound to a port (done by bind())
        the connection to destination must have been NOT established (done by connect())

        Input:  None
        Output: True or False depending on when the connection was established successfully
        '''
        #Listen for SYN + sequence number (X: sender's sequence number)
        #Send SYNACK + ack number (x+1) + sequence number (Y: receiver's seq num)
        #Listen for ACK + acknum (Y+1)

        #Listening for SYN + seq_nb
        received_syn = False
        while (not received_syn):
            pack = self._receive()
            if pack:
                received_syn = True
        bits = pack.get_bits()
        receiver_seq_nb = pack.get_seq()
        self.ack_nb = receiver_seq_nb+1

        #sending SYNACK + ack number (X+1) + seq_nb (Y)
        synack_sent = False
        while (not synack_sent):
            pack = packet()
            pack.build_header([self.sport,self.dport,self.seq_nb,self.ack_nb,1,1,0,0])
            pack.build_payload("")
            synack_sent = self._send(pack)
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
    s.connect(('127.0.0.1',5967))
    # s.set_timeout(10)
    # s.print_all()
    # p = packet()
    # p.build_payload('surya')
    # print(s._send(p))
    s.init_handshake()
    s.close()

    print ('ran')
