#STP header feilds
#dict containing following key,value pairs
#1. source port #
#2. dest port #
#3. seq_nb
#4. ack_nb
#5. ACK
#6. SYN
#7. FIN
#8. RST
#example ['1234', '1234', '100000', '4294967295', '4294967295', '0', '1', '1', '1']
#max len of header = 46 bytes
#b'1234+1234+100000+4294967295+4294967295+0+1+1+1'


class header:

    def __init__(self):
        self.fields = ["sport","dport","seq_nb","ack_nb","ACK","SYN","FIN","RST"]
        #self.head = {"sport":None, "dport":None, "seq_nb":None, "ack_nb":None, "ACK":"0", "SYN":"0", "FIN":"0", "RST":"0"}
        self.head = {}
        for f in self.fields:
            self.head[f] = "0"
        return

    def get_head(self):
        return self.head

    def get_fields(self):
        return self.fields

    def get_values(self):
        values = []
        for i in self.get_fields():
            values.append(self.head[i])
        return values

    def get_item(self,item):
        return self.head[str(item)]

    def set_item(self,item,value):
        self.head[item] = str(value)
        return


if __name__ == '__main__':
    h = header()
    print (h.get_head())
    h.set_item("sport",1234)
    h.set_item("dport",4321)
    h.set_item("seq_nb","0000")
    h.set_item("ack_nb",1111)

    print (h.get_head())
    print (h.get_fields())
    print (h.get_values())
