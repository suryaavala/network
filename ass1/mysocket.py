#PYTHON 3 ONLY, doesn't work with Python2
#hosted on bitbucket as a private repo, will be made public after one week on the assignment deadline
#git@bitbucket.org:saavala2/network.git

#Difference between traditional TCP and mysocket
#1  #ACK and SYN numbers are little different that the TCP
    #ACK number "X" is sent to acknowledge Received pack with SEQ "X"
        #in tcp "X+1" would have been sent as an ACK
#2  #fast restransmission is sent after one duplicate acknowledgement
        #in tcp traditionally sent after 3 dup acks

from socket import *
import time
import random
from packet import *
import pickle


class mysocket:

    def __init__(self):
        self.sock = socket(AF_INET,SOCK_DGRAM)  #udp socket
        self.sock.setblocking(0)                #non blocking circuit
        self.sport = None                       #source port
        self.dip = None                         #destination ip
        self.dport = None                       #destination port
        self.timeout = None                     #timeout value in seconds
        self.seq_nb = str(int(random.random()*100)) #my sequence number
        self.ack_nb = -1                        #ack number I have sent
        self.received_acknb = str(0)            #ack number I have received
        self.isn = self.seq_nb                  #isn
#can implement self.sock_status to keep track of connection
        self.connection_established = None      #is connection established or not
        self.pdrop = None                       #probability of packet drop
        self.seed = None                        #seed for the random number
        self.mss =  None                        #mss in bytes
        self.mws = None                         #mws in bytes
        #time
        self.origin_time = None                 #time when handshake was started
        self.data_len = None                    #size of data I am about to send
        self.log_file = None                    #name of my log file
        self.log_nb = 1                         #current log number

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
            self.sock.bind(('',0))                  #letting the OS choose the port number randomly, for sender
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
        self.bind()                 #binding my port number
        return

    def set_timeout(self, timeout):
        '''
        Sender Function
        Input:  Takes timeout value in sec (int)
        Output: Sets the timeout of the socket
        '''
        self.timeout = int(timeout)
        self.sock.settimeout(self.timeout)
        return

    def set_param(self,mss,mws,pdrop,seed):
        '''
        Sender Function
        Input:  pdrop as an float for the probability of dropping packet
                seed as an int for generating the random number

        Output: Binds those values to appropriate variables
        '''
        self.mss = mss
        self.mws = mws
        self.pdrop = float(pdrop)
        self.seed = seed
#CHECK AGAIN
        random.seed(self.seed)              #seeding the random function already
        return

    def set_logfile(self, filename):
        '''
        Input:  Takes the filename for log_file
        Output: Assigns it to the appropriate variable and prints out the head of log file
        '''
        self.log_file = open(filename, 'w+')
        print ('no.\ts/r/d\ttm\t\ttype\tseq\tnbb\tack', file=self.log_file)

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
        Sender Function initiating the hand shake and establishing the connection.
        Socket has to be opened (opened by __init__) and the connection to destination must have been established (done by connect())

        Input:  None
        Output: True or False depending on when the connection was established successfully
        '''
        #SYN + sequence number (X: sender's sequence number)
        #listen for SYNACK + ack number (x) + sequence number (Y: receiver's seq num)
        #Send ACK + acknum (Y)
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
        self.ack_nb = str(int(receiver_seq_nb))

        #sending ACK + acknum (Y)
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
        Receiver Function accepting the hand shake (which was initiated by Sender) and establishing the connection.
        Socket has to be opened (opened by __init__) and must have been bound to a port (done by bind())
        the connection to destination must have been NOT established (done by connect())

        Input:  None
        Output: True or False depending on when the connection was established successfully
        '''
        self.origin_time = time.time()
        #Listen for SYN + sequence number (X: sender's sequence number)
        #Send SYNACK + ack number (x) + sequence number (Y: receiver's seq num)
        #Listen for ACK + acknum (Y)

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

        #sending SYNACK + ack number (X) + seq_nb (Y)
        synack_sent = False
        while (not synack_sent):
            pack = packet()
            pack.build_header([self.sport,self.dport,self.seq_nb,self.ack_nb,1,1,0,0])
            synack_sent = self._send(pack)
        self.seq_nb = int(self.seq_nb)+ 1

        #Listening for ACK + acknum (Y)
        synack = pack

        received_ack = False
        while (not received_ack):
            pack, addr = self._receive()
            if pack:
                bits = pack.get_bits()
                if bits == '1000':
                    received_ack = True
            else:
                synack_sent = self._send(synack)
        self.received_acknb = pack.get_ack()

        self.connection_established = received_syn and synack_sent and received_ack
        return

    def init_termination(self):
        '''
        Sender Function to initiate connection termination
        Input: None
        Output: Terminates connection with the receiver
        '''
        #send fin
        fin1 = False
        while not fin1:
            fin_pack = packet()
            fin_pack.build_header([self.sport,self.dport,self.seq_nb,self.ack_nb,0,0,1,0])
            fin1 = self._send(fin_pack)

        #listen for ack
        received_ack1 = False
        received_fin2 = False
        while (not received_ack1) and (not received_fin2):
            pack, addr = self._receive()
            if pack:
                bits = pack.get_bits()
                if bits == '1000':
                    received_ack1 = True
                elif bits == '0010':
                    received_fin2 = True

            else:
                fin1 = self._send(fin_pack)

        #listen for fin

        while not received_fin2:
            pack, addr = self._receive()
            if pack:
                bits = pack.get_bits()
                if bits == '0010':
                    received_fin2 = True
        self.ack_nb = pack.get_seq()

        #send ack2
        ack2 = False
        while not ack2:
            ack2_pack = packet()
            ack2_pack.build_header([self.sport,self.dport,self.seq_nb,self.ack_nb,1,0,0,0])
            ack2 = self._send(ack2_pack)

        return fin1 and  (received_ack1 or received_fin2) and ack2

    def accept_termination(self,fin_pack):
        '''
        Receiver function to accept termination. This function is called by receive_file function.
        Input:  Takes the Fin packet that came from the Sender
        Output: Terminates connection
        '''
        #receive fin1
        self.ack_nb = fin_pack.get_seq()
        received_fin1 = True

        #send ack1
        ack1 = False
        while not ack1:
            ack1_pack = packet()
            ack1_pack.build_header([self.sport,self.dport,self.seq_nb,self.ack_nb,1,0,0,0])
            ack1 = self._send(ack1_pack)

        #send fin2
        fin2 = False
        while not fin2:
            fin2_pack = packet()
            fin2_pack.build_header([self.sport,self.dport,self.seq_nb,self.ack_nb,0,0,1,0])
            fin2 = self._send(fin2_pack)

        #listen for ack2
        received_ack2 = False
        while not received_ack2:
            pack, addr = self._receive()
            if pack:
                bits = pack.get_bits()
                if bits == '1000':
                    received_ack2 = True
            else:
                fin2 = self._send(fin2_pack)

        return received_fin1 and ack1 and (fin2 or received_ack2)

    def send_file(self,sfile):
        '''
        Sender Function to transmit file, connection should have been established already and set_param() must have been called
        Input: Takes string <path>/file_name.txt as the input argument
        Output: Tries to reliably send the file Object accross to receiver by calling _transmit function
        '''

#error handling can be added
        send_file = open(sfile, 'rb')           #opening send_file
        file_data = send_file.read()            #reading data as bytes
        self.data_len = len(file_data)          #size of total file
        payloads = {}                           #payloads to be sent (divided in chunks of mss)

        #diving file into chuncks of mss size and assigning sequence numbers to it
        for i in range(0,len(file_data),self.mss):
            payload = file_data[i:i+self.mss]
            payloads[i+int(self.seq_nb)] = payload

        #building packets from payload chunks
        packets = self._build_packets(payloads)

        #transmitting those packets accross
        self._transmit(packets)
        self.seq_nb = int(self.received_acknb) + 1 #putting the sequence back to where it should be at this point

        send_file.close()               #closing sender file
        self.init_termination()
        return

    def _build_packets(self,payloads):
        '''
        Sender Function
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
        Sender Function
        Input:  Takes pakcets
        Output: Transmitss them reliably accross
        '''
        last_packet = self.data_len//self.mss*self.mss+int(self.isn)+1

        sent_time = {}          #dict keeping track of transmission times

        #loop while most recent ack received is less than sequence number of last packet
        while (int(self.received_acknb)<last_packet):

#event1:            #send packets until mws is reached
            while (int(self.seq_nb)-int(self.received_acknb)) <= self.mws and (int(self.seq_nb)<=last_packet):
                sent_time[self.seq_nb] = time.time()
                self._pld_send(packets[self.seq_nb])
                self.seq_nb += self.mss



#event2:            #listen for packets
            pack, addr = self._receive()
            if pack:        #if not timeouted
                if self.received_acknb == (int(pack.get_ack())):    #check for duplicate ack, then retransmit the next pack after dup ack
                    fast_retransmit = self.received_acknb+self.mss
                    sent_time[fast_retransmit] = time.time()
                    self._pld_send(packets[fast_retransmit])
                else:
                    self.received_acknb = (int(pack.get_ack()))


#event 3:           #check for timeouts
            timed_out = self._check_timeout(sent_time,last_packet)
            if timed_out:       #if there are timedout packets retransmit them
                for t in sorted(timed_out):
                    sent_time[t] = time.time()
                    self._pld_send(packets[t])

        return

    def _check_timeout(self,sent_time,last_packet):
        '''
        Checks for time outs in among the sent packets
        Input:  sent_time dict (with seq_nb as keys and sent times as respective values) and last_packet (seq_nb of last packet)
        Ouput:  Checks if packets (between last acked and last packet) are timed out. It returns a list of sequence numbers of all timedout packets.
        '''
        timed_out = []
        for t in sorted(sent_time):
            if t<=last_packet and t>self.received_acknb:
                if sent_time[t]+self.timeout<time.time():
                    timed_out.append(t)
        return timed_out or None

    def _pld_send(self,packet):
        '''
        Pld send would drop the pack or send it as per the assignment specs
        Input:  Takes packet object
        Ouput:  Decides whether or not to send it and executes the desicion
        '''
        rand = random.random()
        #send packet if rand > pdrop
        if rand > self.pdrop:
            self._send(packet)
            return
        self._log(packet, "drp")
        return


    def receive_file(self,rfile):
        '''
        Receiver function to receive the transmitted file. Connection should have been established already.

        Input: Takes string <path>/file_name.txt as the input argument
        Output: Writes the data it receives as to the file name
        '''
        receive_file = open(rfile, 'wb')     #receiver_file
        data = {}                            #data received will be stored here as per seq number
        expected_seq = 0                     #sequence number of next expected packet
        buff = {}                            #receivers buffer
        fin_pack = None                      #fin pack that is received from the sender

        #forever loop, breaks when a fin packet is received
        while True:
            pack, addr = self._receive()

            #if the packet received is FIN, then the loop breaks
            if pack.packet_type() == 'F':
                fin_pack = pack
                break

            if not data: #getting the expected packet size after receiving the first packet
                self.mss = int(len(pack.get_payload()))
                #expected_seq = int(self.ack_nb)+1
                expected_seq = int(pack.get_seq()) + self.mss

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
                        self.ack_nb = expected_seq          #cummulative ack
                        expected_seq += self.mss


            ack = packet()
            ack.build_header([self.sport,self.dport,self.seq_nb,int(self.ack_nb),'1','0','0','0'])
            self.seq_nb = str(int(self.seq_nb)+len(ack.get_payload()))
            self._send(ack)

        #writed data to receive_file
        for d in sorted(data):
            receive_file.write(data[d])

        receive_file.close() #closes receive file
        self.accept_termination(fin_pack)

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
        '''
        Logs data into the log file
        Input:  Takes packet object and status "snd/rcv/drp"
        Output: Logs accordingly
        '''
        print ('{:}\t{:}\t{:f}\t{:}\t{:}\t{:}\t{:}'.format(self.log_nb,status,round(time.time()-self.origin_time,7),pack.packet_type(),pack.get_seq(),len(pack.get_payload()),pack.get_ack()), file=self.log_file)
        self.log_nb += 1
        return

    def _receive(self):
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
                return (None, None)
            except Exception:
                #since the circuit is non-blocking, it returns and exception if it doesnt receive any data. so we are just ignoring all those (but timeout) and listending again
                continue
        self._log(pack, "rcv")
        return (pack, addr)




if __name__ == '__main__':

    #my tests
    s = mysocket()
    s.connect(('127.0.0.1',5967))
    s.set_timeout(10)
    s.set_param(50, 100, 0.5, 50)
    s.set_logfile('send.log')
    s.init_handshake()
    s.send_file('send_file.txt')
    s.close()
