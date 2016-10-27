#Surya Avinash Avala, z5096886
#PYTHON 3 ONLY, doesn't work with Python2
#Requires graph.py file
#hosted on bitbucket as a private repo, will be made public after one week on the assignment deadline
#git@bitbucket.org:saavala2/network.git


#Implementation of Dijkstra algorithm

from graph import *
import math


def dijkstra(u, graph):
    '''
    u = source node from which dijkstra is being applied
    c(x,y): link cost from nodextoy; =∞ifnot direct neighbors
    D[v]: current value of cost of path from source to dest. v
    p(v): predecessor node along path from source to v
    abs_N: set of nodes whose least cost path definitively known
    '''
    nodes = graph.getNodes()
    edges = graph.getEdges()
    #initialisation
    abs_N = [u]
    D = {}
    p = {}
    for n in nodes:
        if (n,u) in edges:
            D[n] = int(edges[(n,u)])
            p[n] = u
        elif (u,n) in edges:
            D[n] = int(edges[(u,n)])
            p[n] = u
        else:
            D[n] = float('inf')

    while set(abs_N) != set(nodes):
        w = u
        for i in D:
            if i not in abs_N  and D[i]<=D[w]:
                w = i
        #print (w)

        abs_N.append(w)
        for n in nodes:
            if n in abs_N:
                continue
            if (w,n) in edges:
                #D[n] = min(D[n],D[w]+edges[w,n])
                if D[w]+int(edges[w,n])<D[n]:
                    D[n] = D[w]+int(edges[w,n])
                    p[n] = w
            elif (n,w) in edges:
                #D[n] = min(D[n],D[w]+edges[n,w])
                if D[w]+int(edges[n,w])<D[n]:
                    D[n] = D[w]+int(edges[n,w])
                    p[n] = w
    #print (abs_N)
    return p

def shortest_path (src,dest, p):
    u = src
    v = dest
    path = []
    while True:
        try:
            n = p[v]
            path.append(n)
        except KeyError:
            break
        else:
            v = n
    path.reverse()
    return path

def routing_table(src,nodes,p):
    routing = {}
    for n in nodes:
        if n != src:
            sh_path = shortest_path(src, n, p)
            #print(n,src,p)
            if len(sh_path)==1:
                routing[n] = n
            else:
                routing[n] = sh_path[1]
    return routing

if __name__ == '__main__':
    g = Graph()
    N = ['A','B','C','D','E','F']
    E = [('A','B',2),('A','C',5),('A','D',1),('B','C',3),('B','D',2),('C','D',3),('C','E',1),('C','F',5),('D','E',1),('E','F',2)]

    for n in N:
        g.addNode(n)

    for e in E:
        g.addEdge(e[0:2],e[2])

    #print(g.getNodes(),g.getEdges())

    p = dijkstra('A', g)
    #print (p)
    #print (shortest_path('A', 'C', p))
    #print (shortest_path('A', 'B', p))
    r = routing_table('A',g.getNodes(),p)
    print ('{}:{}'.format('dest','foward_to'))
    keys = list(r.keys())
    keys.sort()
    for k in keys:
        print ('{}: {}'.format(k,r[k]))
