#Bug1: Receiver has to be started/run first otherwise sync sent by the sender is lost and
#   the sender is stuck in an infinite loop waiting for sycnack
#   the receiver is stuck in an infinite loop waiting for sync
#Bug1: Fixed sender and receiver can be started in any order
#ACK and SYN numbers are little different that the TCP
#ACK number "X" is sent to acknowledge Received pack with SEQ "X"
    #in tcp "X+1" would have been sent as an ACK

from socket import *
import time
import random
from packet import *
import pickle


class mysocket:

    def __init__(self):
        self.sock = socket(AF_INET,SOCK_DGRAM)
        self.sock.setblocking(0) #non blocking circuit
        #self.sock.bind(('',0))
        self.sport = None
        self.dip = None
        self.dport = None
        self.timeout = None
        self.seq_nb = str(int(random.random()*100)) #my sequence number transmitted
        self.ack_nb = -1 #ack number sent
        self.received_acknb = str(0) #ack received
        self.isn = self.seq_nb
        #can implement self.sock_status to keep track of connection
        self.connection_established = None
        self.pdrop = None
        self.seed = None
        self.mss =  None #bytes
        self.mws = None #bytes
        #time
        self.origin_time = None
        self.data_len = None
        self.log_file = None
        self.log_nb = 1
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

    def set_param(self,mss,mws,pdrop,seed):
        '''
        Input:  pdrop as an float for the probability of dropping packet
                seed as an int for generating the random number

        Output: Binds those values to appropriate variables
        '''
        self.mss = mss
        self.mws = mws
        self.pdrop = pdrop
        self.seed = seed
        random.seed(self.seed)
        return

    def set_logfile(self, filename):
        self.log_file = open(filename, 'w+')
        print ('no.\ts/r/d\ttm\ttype\tseq_snt\tnbb\tack_rcv', file=self.log_file)

        return



    def close(self):
        '''
        Input:  None
        Output: Closes circuit
        '''
        self.sock.close()
        self.log_file.close()
        return

    def print_all(self):
        '''
        Input:  None
        Output: Prints values of all socket variable
        '''
        print("sock: {}\nsource port: {}\ndest ip: {}\ndest port {}\ntimeout: {}\nseq_nb: {}\nack_nb: {}\nisn: {}\nack_received_for: {}\nconnection established: {}\ndata_len: {}".format(self.sock, self.sport,self.dip,self.dport,self.timeout,self.seq_nb,self.ack_nb,self.isn,self.received_acknb,self.connection_established,self.data_len))
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
        self.origin_time = time.time()

        if not (self.sport and self.dip and self.dport and self.seq_nb and self.ack_nb):
            return False

        #sending SYN
        syn_sent = False
        while (not syn_sent):
            pack = packet()
            pack.build_header([self.sport,self.dport,self.seq_nb,self.ack_nb,0,1,0,0])
            syn_sent = self._send(pack)

        sync = pack
###can be improved keep sending syn requests until we receive an syncack back from receiver
        #listen for SYNACK
        received_synack = False
        while (not received_synack):
            pack, addr = self._receive()
            if pack:
                bits = pack.get_bits()
                if bits == '1100':
                    received_synack = True
            else:
                syn_sent = self._send(sync)
        receiver_seq_nb = pack.get_seq()
        self.received_acknb = int(pack.get_ack())-1
        self.ack_nb = str(int(receiver_seq_nb)+1)


        #sending ACK + acknum (Y+1)
        ack_sent = False
        while (not ack_sent):
            pack = packet()
            pack.build_header([self.sport,self.dport,self.seq_nb,self.ack_nb,1,0,0,0])
            ack_sent = self._send(pack)

        self.seq_nb = int(self.seq_nb)+1
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
        self.origin_time = time.time()
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
        self.ack_nb = str(int(receiver_seq_nb)) #+1
        self.dip, self.dport = addr[0], str(addr[1])
        #sending SYNACK + ack number (X+1) + seq_nb (Y)
        synack_sent = False
        while (not synack_sent):
            pack = packet()
            pack.build_header([self.sport,self.dport,self.seq_nb,self.ack_nb,1,1,0,0])
            synack_sent = self._send(pack)
        self.seq_nb = int(self.seq_nb)+ 1
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
        Sender function to transmit file, connection should have been established already and set_param() must have been called
        Input: Takes string <path>/file_name.txt as the input argument
        Output: Tries to reliably send the file Object accross to receiver by calling _transmit function
        '''


        #loop for sending
        #if rand > pdrop: transmit
            #else: drop packet
        #mws
            #self.seq_nb-(self.received_acknb-1) <= mws
        #mss
            #len(pack.payload()) <= mss

#error handling can be added
        send_file = open(file, 'rb')
        file_data = send_file.read()
        self.data_len = len(file_data)
        payloads = {}
        self.print_all()
        print (self.seq_nb,self.ack_nb, self.received_acknb)
        for i in range(0,len(file_data),self.mss):
            payload = file_data[i:i+self.mss]
            payloads[i+int(self.seq_nb)] = payload
        packets = self._build_packets(payloads)
        self._transmit(packets)

        fin_pack = packet()
        fin_pack.build_header([self.sport,self.dport,self.received_acknb+1,self.ack_nb,0,0,1,0])
        self._send(fin_pack)
        return

    def _build_packets(self,payloads):
        '''
        Input: Takes paylaods
        Output: Builds packets
        '''
        packets = {}
        for i in sorted(payloads):
            p = packet()
            p.build_header([self.sport,self.dport, i,self.ack_nb,0,0,0,1])
            p.build_payload (payloads[i])
            packets[i] = p
        return packets

    def _transmit(self, packets):
        '''
        Input:  Takes pakcets
        Output: Sends them reliably accross
        '''
        first_packet = int(self.isn)+1
        last_packet = self.data_len//self.mss*self.mss+int(self.isn)+1
        #print (first_packet,last_packet)
        for i in sorted(packets):
            print (i, packets[i].get_packet(),file=self.log_file)
        sent_time = {} #dict keeping track of transmission times
        while (int(self.received_acknb)<last_packet):
            while (int(self.seq_nb)-int(self.received_acknb)) <= self.mws and (int(self.seq_nb)<=last_packet):
                #drop = self._pld()
                # if drop:
                #     #print ("dropping: {}, at: {}".format(packets[self.seq_nb].get_packet(),time.time()))
                #     sent_time[self.seq_nb] = time.time()
                #     #self._send(packets[self.seq_nb])
                #     print ("dropping packet, seq_nb: {}, rcv ack: {}".format(self.seq_nb,self.received_acknb))
                #     self._log(packets[self.seq_nb], "drp")
                #     self.seq_nb += self.mss
                # else:
                #     #print ("transmitting: {}, at: {}".format(packets[self.seq_nb].get_packet(),time.time()))
                #     sent_time[self.seq_nb] = time.time()
                #     self._send(packets[self.seq_nb])
                #     self.seq_nb += self.mss
                sent_time[self.seq_nb] = time.time()
                self._pld_send(packets[self.seq_nb])
                self.seq_nb += self.mss


            #print ("listening at : {}".format(time.time()))
            pack, addr = self._receive()
            #print ("done listening at : {}".format(time.time()))
            if pack:
                #print ("received: {}, at: {}".format(pack.get_packet(),addr))
                self.received_acknb = (int(pack.get_ack()))
                #print ("ACK NB RECEIVED: {}, last_packet: {}, sequence number: {}".format(self.received_acknb, last_packet,self.seq_nb))
                print ("received:\t{}".format(pack.get_ack()))

            timed_out = self._check_timeout(sent_time,last_packet)
            if timed_out:
                for t in sorted(timed_out):
                    #print("retransmitting: {}, at: {}".format(packets[t].get_packet(),time.time()))
                    sent_time[t] = time.time()
                    self._pld_send(packets[t])
        print ("last_received ack: {}, last_packet: {}".format(self.received_acknb,last_packet))
        return

    def _check_timeout(self,sent_time,last_packet):
        timed_out = []
        for t in sorted(sent_time):
            if t<=last_packet and t>self.received_acknb:
                #print ("here: {}",sorted(sent_time))
                if sent_time[t]+self.timeout<time.time():
                    timed_out.append(t)
        return timed_out or None

    def _pld_send(self,packet):

        rand = random.random()
        #print (rand)
        if rand > self.pdrop/100:
            print ("sending:\t{}".format(packet.get_seq()))
            self._send(packet)
            return
        #print ("asked to drop")
        print ("drpopping:\t{}".format(packet.get_seq()))
        #print ("dropped: {}, and ack pack is {}".format(packet.get_packet(),packet.get_seq()))
        self._log(packet, "drp")
        return


    # def receive_file(self,file):
    #     receive_file = open(file, 'wb')
    #     nb_packets = 70
    #     data = {}
    #     pack = True
    #     while nb_packets:
    #         pack, addr = self._receive()
    #         print (pack.get_packet())
    #         self.ack_nb = int(pack.get_seq())
    #         data [self.ack_nb] = pack.get_payload()
    #         ack = packet()
    #         ack.build_header([self.sport,self.dport,self.seq_nb,int(self.ack_nb),'1','0','0','0'])
    #         self._send(ack)
    #         print ("sent ack with num: {}, and ack pack is {}".format(int(self.ack_nb), ack.get_packet()))
    #         #print (pack.get_packet())
    #         nb_packets -= 1
    #
    #     for d in sorted(data):
    #         receive_file.write(data[d])
    #
    #
    #     return
    def receive_file(self,file):
        receive_file = open(file, 'wb')
        data = {}
        size = True
        expected_seq = self.ack_nb
        buff = {}
        while True:
            pack, addr = self._receive()
            #print (pack.get_packet())
            if pack.packet_type() == 'F':
                break
            if not data: #getting the expected packet size after receiving the first packet
                #print (type(self.ack_nb),type(int(len(pack.get_payload()))) )
                self.mss = int(len(pack.get_payload()))
                expected_seq = int(self.ack_nb)+1

            if int(pack.get_seq()) == expected_seq: #the seq received is expected then go ahead append to data and send an ack for it
                expected_seq += self.mss
                self.ack_nb = int(pack.get_seq())
                data [self.ack_nb] = pack.get_payload()
            else: #if there is not buffer then add the packet to buffer
                buff[int(pack.get_seq())] = pack.get_payload()



            if buff: #if buffer then check all the items in the buffer if expected pack is there in the buffer
                for b in sorted(buff):
                    if b == expected_seq:
                        data[b] = buff.pop(b, None)
                        self.ack_nb = expected_seq
                        expected_seq += self.mss


            ack = packet()
            ack.build_header([self.sport,self.dport,self.seq_nb,int(self.ack_nb),'1','0','0','0'])
            self.seq_nb = str(int(self.seq_nb)+len(ack.get_payload()))
            self._send(ack)
            print ("received:\t{}".format(int(pack.get_seq())))
            print ("sent ack:\t{}".format(int(self.ack_nb)))

            #print (pack.get_packet())

        for d in sorted(data):
            receive_file.write(data[d])


        return


    def _send(self,pack):
        '''
        Input:  Takes final packet object
        Output: Sends the payload accross
        Note:   Packet has to be built
        '''
        encoded_pack = pickle.dumps(pack)
        sent_bytes = self.sock.sendto(encoded_pack, (str(self.dip),int(self.dport)))


        #logging

        self._log(pack, "snd")
        if (len(encoded_pack) != sent_bytes):
                return False
        return True

    def _log(self,pack,status):

        # print ('{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(self.log_nb,status,round(time.time()-self.origin_time,7),pack.packet_type(),self.seq_nb,len(pack.get_payload()),self.received_acknb), file=self.log_file)
        # if status == 'rcv':
        #     print ('{:}\t{:}\t{:f}\t{:}\t{:}\t{:}\t{:}'.format(self.log_nb,status,round(time.time()-self.origin_time,7),pack.packet_type(),pack.get_seq(),len(pack.get_payload()),int(self.received_acknb)+1), file=self.log_file)
        #     self.log_nb += 1
        #     return
        # print ('{:}\t{:}\t{:f}\t{:}\t{:}\t{:}\t{:}'.format(self.log_nb,status,round(time.time()-self.origin_time,7),pack.packet_type(),self.seq_nb,len(pack.get_payload()),self.received_acknb), file=self.log_file)
        print ('{:}\t{:}\t{:f}\t{:}\t{:}\t{:}\t{:}'.format(self.log_nb,status,round(time.time()-self.origin_time,7),pack.packet_type(),pack.get_seq(),len(pack.get_payload()),pack.get_ack()), file=self.log_file)
        self.log_nb += 1
        return

    def _receive(self,f=False):
        '''
        Input:  None
        Output: Returns a tuple of packet object (which was received) and addr
        '''
        pack = ''
        while (not pack):
            try:
                msg, addr = self.sock.recvfrom(4096)
                pack = pickle.loads(msg)
            except timeout:
                #print ("timeout#4358356")
                return (None, None)
            except Exception:
                #print (Exception)
                continue
        #print (pack)
        self._log(pack, "rcv")
        return (pack, addr)



###########have to implement a custom buffer function for out of order packets##






if __name__ == '__main__':

    #print ("running")
    s = mysocket()
    s.connect(('127.0.0.1',5967))
    s.set_timeout(10)
    s.set_param(50, 100, 50, 50)
    s.set_logfile('send.log')
    s.print_all()
    # p = packet()
    # p.build_payload('surya')
    # print(s._send(p))
    #print (s.init_handshake())
    #s.set_param(50, 200, 0, 50)
    s.init_handshake()
    s.print_all
    print (s.send_file('send_file.txt'))
    s.print_all()
    s.close()

    #print ('ran')
