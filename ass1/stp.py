#hard coded
# delim = '+:|'

#All functions for stp protocol reside here
from socket import *
import time

#importing header file
from stp_header import *


class stp_socket:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sip, self.sport = self.sock.getsockname()
        self.dip = None
        self.dport = None
        self.timeout = None
        self.seq_nb = 0 #seq number of the last message sent
        self.ack_nb = 0 #seq number of the last message whose ack was received

    def connect(self,*dest):
        self.dip = str(dest[0])
        self.dport = str(dest[1])

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
        received_msg, received_addr = self.sock.recvfrom(1024)
        received_msg = received_msg.decode('ascii')
        self.sip, self.sport = self.sock.getsockname()
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

    def init_hshake(self):
        #send SYN + sequence number
        #receive SYNACK +
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
    s._send("final message")
    r_msg = ""
    while (not r_msg):
        r_msg, r_add = s._receive()
    print ("received_msg: {} from address {}".format(r_msg,r_add))

    print ("\n\n\n")
    s.print_all()
    s.close()
