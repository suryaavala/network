#Surya Avinash Avala, z5096886
#PYTHON 3 ONLY, doesn't work with Python2
#Requires graph.py file
#hosted on bitbucket as a private repo, will be made public after one week on the assignment deadline
#git@bitbucket.org:saavala2/network.git


#Implementation of Dijkstra algorithm

from graph import *

if __name__ == '__main__':
    g = Graph()
    N = ['A','B','C','D','E','F']
    E = [('A','B',2),('A','C',5),('A','D',1),('B','C',3),('B','D',2),('C','D',3),('C','E',1),('C','F',5),('D','E',1),('E','F',2)]

    for n in N:
        g.addNode(n)

    for e in E:
        g.addEdge(e[0:2],e[2])

    print(g.getNodes(),g.getEdges())
