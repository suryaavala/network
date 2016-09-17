#hard coded
# delim = '+:|'

#All functions for stp protocol reside here
from socket import *
import time
import random

#importing header file
from stp_header import *


class stp_socket:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sip, self.sport = self.sock.getsockname()
        self.dip = None
        self.dport = None
        self.timeout = None
        self.seq_nb = int(random.random()*100) #seq number of the last message sent
        self.ack_nb = -1 #seq number of the last message whose ack was received
        self.timeout = 10
        self.sock.settimeout(self.timeout)


    def _send(self,message):
        '''
        Input: encoded message
        Output: sends the message to dip, dport
        '''
        if (type(message)==str):
            message = message.encode('ascii')
        self.sock.sendto(message,(str(self.dip),int(self.dport)))
        self.sip, self.sport = self.sock.getsockname()
        return

    def _receive(self):
        '''
        Input: listens at source port for a message
        '''
        self.sip, self.sport = self.sock.getsockname()
        try:
            received_msg, received_addr = self.sock.recvfrom(1024)
            received_msg = received_msg.decode('ascii')
        except timeout:
            return ("timeout", "timeout")
        return (received_msg,received_addr)

    def _build_message(self,header,payload):
        '''
        Input:  Takes header OBJECT and payload as input arguments
                payload is a BYTE string
        Output: string of header_values+payload
                header_values are seperated by delim char +
                header and payload are seperated by delim char +:|
        '''
        head_list = header.get_values()
        head_bstring = ("+".join(head_list)).encode('ascii')
        delim = "+:|".encode('ascii')
        message = head_bstring + delim + payload
        return message

    def print_all(self):
        print (self.sock, self.sip,self.sport,self.dip,self.dport,sep="***")

    def close(self):
        self.sock.close()
        return

    def connect(self,*dest):
        self.dip = str(dest[0])
        self.dport = str(dest[1])
        #self.init_hshake()

    def init_hshake(self):
        #send SYN + sequence number
        #listen for SYNACK + ack number
        #send ACK + acknum

        ########seding SYN#########
        head = header()
        head_values = list(map(str,[self.sip,self.dip,self.seq_nb,self.ack_nb,0,1,0,0]))
        head.set_all(head_values)
        pay = "".encode('ascii')
        message = self._build_message(head,pay)
        self._send(message)


        ###########listening for SYNACK###########
        r_message, r_addr = self._receive()
        print ("#########",r_message)
        return


#def hand_shake(sip,sport,dip,dport,sockname):
if __name__ == '__main__':
    s = stp_socket()
    s.connect('127.0.0.1',5967)
    s.print_all()
    for i in range(10):
        s._send(str(i)+" testing my socket")

    print ("sleeping...")
    time.sleep(5)
    print ("waking up...")
    for i in range(10,0,-1):
        s._send(str(i)+" testing my socket")
    h = header()
    pay = "surya avinash avala".encode('ascii')
    message = s._build_message(h,pay)
    s._send(message)
    # s._send("final message")
    # r_msg = ""
    # while (not r_msg):
    #     r_msg, r_add = s._receive()
    # print ("received_msg: {} from address {}".format(r_msg,r_add))
    #
    # print ("\n\n\n")
    # s.print_all()

    s.init_hshake()
    s.close()
