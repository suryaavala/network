#Surya Avinash Avala, z5096886
#PYTHON 3 ONLY, doesn't work with Python2
#Requires graph.py file
#hosted on bitbucket as a private repo, will be made public after one week on the assignment deadline
#git@bitbucket.org:saavala2/network.git
#Requires dijkstra.py and graph.py files to run

#Lsr.py

#python Lsr.py A 2000 config.txt

import sys
import time
import pickle
from socket import *
from graph import *

#getting input arguments
node_ID = sys.argv[1]
node_Port = int(sys.argv[2])
config_name = sys.argv[3]

#other necessary variables
update_interval = 1
sock = socket(AF_INET,SOCK_DGRAM)  #udp socket
ip = '127.0.0.1'
sock.bind((ip,node_Port))
sock.setblocking(0)

#extracting data out of config file
try:
    config_file = open(config_name, 'r')
except Exception:
    print ('Something wrong with config file, exiting...')
    sys.exit()

file_data = config_file.read().split('\n')

nb_neighbour = int(file_data[0])
neighbour = {}                      #dict neighbour[name] = (cost,port)

for line in range(1,nb_neighbour+1):
    name, cost, port = file_data[line].split()
    #print (name,cost,port)
    neighbour[name] = (cost,port)



#Network graph from the neighbours
net_graph = Graph()
net_graph.addNode(node_ID)
for k in sorted(neighbour.keys()):
    net_graph.addNode(k)
    e = (node_ID,k,neighbour[k][0])
    net_graph.addEdge(e[0:2],e[2])



#building LSR packets
#E = [('A','B',2),('A','C',5),('A','D',1),('B','C',3),('B','D',2),('C','D',3),('C','E',1),('C','F',5),('D','E',1),('E','F',2)]

##-> Potential function here
my_lsr = {}
link = []
for k in sorted(neighbour.keys()):
    link.append((node_ID,k,neighbour[k][0]))
my_lsr[node_ID] = link

lsr = {} #recieved lsrs
#broadcasting
encoded_lsr = pickle.dumps(my_lsr)

def broadcast(packet,audience,all=False):
    if all:
        for a in audience:
            sock.sendto(packet,(ip,int(audience[a][1])))
            #print ('sendmy',a)
        return
    encoded_packet = pickle.dumps(packet)
    for a in audience:
        sock.sendto(packet,(ip,int(a)))
        #print ('sendto',a)
    return

def update_graph(lsr,net_graph):
    for l in lsr:
        try:
            net_graph.addNode(l)
        except Exception:
            continue
        try:
            net_graph.addEdge(lsr[l])
        except Exception:
            continue
    return

start_broadcast = time.time()
while True:
    if time.time()-start_broadcast>=update_interval:
        #then broadcast lsr-packet to neighbours
        #print('broadcasting')
        broadcast(encoded_lsr,neighbour,True)
        start_broadcast = time.time()

    #listen for packets
    try:
        msg, addr = sock.recvfrom(1024)
        pack = pickle.loads(msg)
        for p in pack:
            if p in lsr:
                print(net_graph.getEdges())
                continue
            else:
                lsr[p] = pack[p]
                update_graph(lsr,net_graph)
                audience = []
                for n in neighbour:
                    if n != p:
                        audience.append(n)
                print('sending received to',audience)
                broadcast(pack, audience)

        #print ('received:',time.time(),pack)
        #print (net_graph.getEdges())
    except Exception:
        #since the circuit is non-blocking, it returns and exception if it doesnt receive any data. so we are just ignoring all those (but timeout) and listending again
        continue



if __name__ == '__main__':
    print (node_ID,node_Port,config_name,nb_neighbour)

    #lines = file_date.split("\n")
    #for line in lines:
    #    print (line.split())
    print (file_data)
    print (neighbour)
    print(lsr)
