#Bug1: Receiver has to be started/run first otherwise sync sent by the sender is lost and
#   the sender is stuck in an infinite loop waiting for sycnack
#   the receiver is stuck in an infinite loop waiting for sync

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
        self.seq_nb = str(int(random.random()*100)) #my sequence number transmitted
        self.ack_nb = str(-1) #ack number sent
        self.received_acknb = None #ack received
        self.isn = self.seq_nb
        #can implement self.sock_status to keep track of connection
        self.connection_established = None

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
        print("sock: {}\nsource port: {}\ndest ip: {}\ndest port {}\ntimeout: {}\nseq_nb: {}\nack_nb: {}\nisn: {}\nack_received_for: {}\nconnection established: {}".format(self.sock, self.sport,self.dip,self.dport,self.timeout,self.seq_nb,self.ack_nb,self.isn,self.received_acknb,self.connection_established))
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
            syn_sent = self._send(pack)
###can be improved keep sending syn requests until we receive an syncack back from receiver
        #listen for SYNACK
        received_synack = False
        while (not received_synack):
            pack, addr = self._receive()
            if pack:
                bits = pack.get_bits()
                if bits == '1100':
                    received_synack = True
        receiver_seq_nb = pack.get_seq()
        self.received_acknb = int(pack.get_ack())
        self.ack_nb = str(int(receiver_seq_nb)+1)

        #sending ACK + acknum (Y+1)
        ack_sent = False
        while (not ack_sent):
            pack = packet()
            pack.build_header([self.sport,self.dport,self.seq_nb,self.ack_nb,1,0,0,0])
            ack_sent = self._send(pack)

        self.connection_established = syn_sent and received_synack and ack_sent
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
            pack, addr = self._receive()
            if pack:
                bits = pack.get_bits()
                if bits == '0100':
                    received_syn = True
        receiver_seq_nb = pack.get_seq()
        self.ack_nb = str(int(receiver_seq_nb)+1)
        self.dip, self.dport = addr[0], str(addr[1])
        #sending SYNACK + ack number (X+1) + seq_nb (Y)
        synack_sent = False
        while (not synack_sent):
            pack = packet()
            pack.build_header([self.sport,self.dport,self.seq_nb,self.ack_nb,1,1,0,0])
            synack_sent = self._send(pack)
        #Listening for ACK + acknum (Y+1)
#improvement: keep sending syncack until ack is received back
        received_ack = False
        while (not received_ack):
            pack, addr = self._receive()
            if pack:
                bits = pack.get_bits()
                if bits == '1000':
                    received_ack = True
        self.received_acknb = pack.get_ack()

        self.connection_established = received_syn and synack_sent and received_ack
        return

    def send_file(self,file):
        '''
        Sender function to transmit file, connection should have been established already
        '''


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
        Output: Returns a tuple of packet object (which was received) and addr
        '''
        try:
            msg, addr = self.sock.recvfrom(1024)
            pack = pickle.loads(msg)
        except timeout:
            return None
        return (pack, addr)



###########have to implement a custom buffer function for out of order packets##






if __name__ == '__main__':

    print ("running")
    s = mysocket()
    s.connect(('127.0.0.1',5967))
    # s.set_timeout(10)
    s.print_all()
    # p = packet()
    # p.build_payload('surya')
    # print(s._send(p))
    print (s.init_handshake())
    s.print_all()
    s.close()

    print ('ran')
