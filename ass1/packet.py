#STP packet
#header fields ["sport","dport","seq_nb","ack_nb","ACK","SYN","FIN","DATA"]
#payload as string

class packet:

    def __init__(self):

        self.fields = ["sport","dport","seq_nb","ack_nb","ACK","SYN","FIN","DATA"]
        self.head = {}
        self.payload = ""

        for f in self.fields:
            self.head[f] = "0"
        return

    def get_hfield_all(self):
        '''
        Input:  None
        Output: Returns a list of feild names in the header
        '''
        return self.fields

    def get_hfield(self,field):
        '''
        Input:  Takes header field name string
        Value:  Return header values for the inputed field as string
        '''
        return self.head[field]

    def get_header(self):
        '''
        Input:  None
        Output: Returns a list of head values in the same order as default fields
        '''
        header = []
        for f in self.fields:
            header.append(self.head[f])
        return header

    def get_payload(self):
        '''
        Input:  None
        Output: Returns payload as a string
        '''
        return self.payload

    def get_packet(self,fields=None):
        '''
        Input:
                Optional:   Can select the fields to be returns as well
        Output: Returns tuple (headerValues,payload,[fields])
        '''
        if fields:
            return ((self.get_header(),self.get_payload(),self.get_hfield_all()))
        return ((self.get_header(),self.get_payload()))

    def get_bits(self):
        '''
        Input:  None
        Output: Returns a string concatenated from the bits in header field in the default order (ACK,SYN,FIN,DATA)
        '''
        head_values = self.get_header()
        bits = "".join(head_values[4:])
        return bits

    def get_seq(self):
        '''
        Input:  None
        Output: Returns seq_nb from packet header as a string
        '''
        return str(self.get_header()[2])

    def get_ack(self):
        '''
        Input:  None
        Output: Returns ack_nb from packet header as a string
        '''
        return str(self.get_header()[3])


    def build_header(self,values):
        '''
        Input:  Takes list of header values as Input
        Output: Builds header using the input values
        '''
        for i in range(0, len(self.fields)):
            self.head[self.fields[i]] = str(values[i])
        return

    def build_payload(self,payload):
        '''
        Input:  Takes payload as string though input argument
        Output: Builds payload
        '''
        self.payload = str(payload)
        return

    def build_packet(self,values,payload):
        '''
        Input:  Takes tuple (values,payload)
                values:     list of header values
                payload:    string of payload
        '''
        self.build_header(values)
        self.build_payload(payload)
        return

    def update_hfield(self,field,value):
        '''
        Input:  Takes two strings field and value as input arguments
                field:  Name of the field to be updated
                value:  Value with which it has to be updated
        '''
        self.head[str(field)] = str(value)
        return

if __name__ == '__main__':
    print ("testing")
    h = packet()
    print ("get_hfields,get_header,get_payload,get_packet,get_packet(True)")
    print (h.get_hfield_all(),h.get_header(),h.get_payload(),h.get_packet(),h.get_packet(True))

    h.build_header(['1234','4321','5000',9000,1,0,1,0])
    h.build_payload('surya')
    print (h.get_packet())

    h.build_packet(['0000','1111',10,45,0,1,0,1],'surya avinash avala')
    print(h.get_packet())

    print("done")
