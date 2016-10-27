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
from threading import *
from dijkstra import *

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
    #print ('Something wrong with config file, exiting...')
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

def broadcast(packet,audience,sock,nei=False):
    if nei:
        for a in audience:
            sock.sendto(packet,(ip,int(audience[a][1])))
            #print ('sendmy',a)
        return
    else:
        encoded_packet = pickle.dumps(packet)

        for i in audience:
            #print ("here ", audience)
            sock.sendto(encoded_packet,(ip,int(i)))
            #print ('there')
        return

def update_graph(lsr,net_graph):
    for l in lsr:
        try:
            net_graph.addNode(l)
        except Exception:
            continue
    for l in lsr:
        #print ('l:{}'.format(l))
        for e in lsr[l]:
            try:
                #print (e)
                net_graph.addEdge(e[0:2],e[2])
            except Exception:
                continue
    return

def ls_advertisement():

    start_broadcast = time.time()
    while True:
        # if len(net_graph.getEdges()) == 10:
        #     print ('{} is done!'.format(node_ID))
        if time.time()-start_broadcast>=update_interval:
            broadcast(encoded_lsr,neighbour, sock, True)
            start_broadcast = time.time()

def listen():
    while True:
        # if len(net_graph.getEdges()) == 10:
        #     print ('{} is done!'.format(node_ID))
        try:
            msg, addr = sock.recvfrom(1024)
            pack = pickle.loads(msg)
            #print ('{} Received lsr: {}'.format(node_ID,pack))
            for p in pack:
                if p in lsr:

                    continue
                else:
                    lsr[p] = pack[p]
                    #print('lsr:{}\npack:{}\nlsr[p]:{}\npack[p]:{}'.format(lsr,pack,lsr[p],pack[p]))
                    update_graph(lsr,net_graph)
                    #print('{} Updated network graph: {}'.format(node_ID,net_graph.getEdges()))
                    audience = []
                    for n in neighbour:
                        if n != p:
                            audience.append(neighbour[n][1])
                            #print('\n{} sending lsr {} to {}'.format(node_ID, pack.keys(), n))
                    #print('audience: ',audience)
                    broadcast(pack, audience,sock)


            #print ('received:',time.time(),pack)
            #print (net_graph.getEdges())
        except Exception:
            #since the circuit is non-blocking, it returns and exception if it doesnt receive any data. so we are just ignoring all those (but timeout) and listending again
            continue
def lcp_print():
    start_lcp = time.time()
    #print ('all_nodes : {}'.format(all_nodes))
    while True:
        if time.time()-start_lcp >= 30:
            paths = dijkstra(node_ID, net_graph)
            all_nodes = net_graph.getNodes()

            for n in net_graph.getNodes():
                #print ('claculating shortest path for {}'.format(n))
                if n != node_ID:
                    short_path = ''.join(shortest_path(node_ID,n,paths))+n
                    print('Lcp from {} to {} is {}'.format(node_ID,n,short_path))
                    start_lcp = time.time()


t1 = Thread(target=ls_advertisement)
t2 = Thread(target=listen)
t3 = Thread(target=lcp_print)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

if __name__ == '__main__':
    #print (node_ID,node_Port,config_name,nb_neighbour)

    #lines = file_date.split("\n")
    #for line in lines:
    #    print (line.split())
    #print (file_data)
    #print (neighbour)
    #print(lsr)
    pass
