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

#getting input arguments
node_ID = sys.argv[1]
node_Port = int(sys.argv[2])
config_name = sys.argv[3]

#other necessary variables
update_interval = 1
sock = socket(AF_INET,SOCK_DGRAM)  #udp socket
ip = '127.0.0.1'
sock.bind((ip,node_Port))

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

#E = [('A','B',2),('A','C',5),('A','D',1),('B','C',3),('B','D',2),('C','D',3),('C','E',1),('C','F',5),('D','E',1),('E','F',2)]

lsr = {}
link = []
for k in sorted(neighbour.keys()):
    link.append((node_ID,k,neighbour[k][0]))
lsr[node_ID] = link



if __name__ == '__main__':
    print (node_ID,node_Port,config_name,nb_neighbour)

    #lines = file_date.split("\n")
    #for line in lines:
    #    print (line.split())
    print (file_data)
    print (neighbour)
    print(lsr)
