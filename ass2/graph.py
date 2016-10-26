##urya Avinash Avala, z5096886
#PYTHON 3 ONLY, doesn't work with Python2
#hosted on bitbucket as a private repo, will be made public after one week on the assignment deadline
#git@bitbucket.org:saavala2/network.git

#Class for implementation of Graphs

# class Node:
#     def __init__(self,name):
#         '''
#         Name as a string, for the name of the router
#         '''
#         self.name = name
#
#     def getName(self):
#         return self.name
#
#     def __str__(self):
#         return self.name

# class Edge:
#     def __init__(self,node,adjNodes):
#         '''
#         Input:  Node is the origin node
#                 adjNode is the list of node which are adjacent to origin
#         '''
#         self.src = node
#         self.dst = []
#         for d in adjNodes:
#             self.dst.append(d)
#
#     def getSource(self):
#         return self.src
#
#     def getDestination(self):
#         return self.dst
#
#     def __str__(self):
#         return self.src + '->' + str(self.dst)

class Graph:
    def __init__(self):
        self.graph = {}

    def addNode(self,node):
        if node in self.graph:
            raise ValueError ('Duplicate Node')
        else:
            self.graph[node] = []

    def addEdge(self,node,neighbour,cost=0):
        if node not in self.graph:
            raise ValueError ('Node not in Graph')
        elif neighbour in self.graph[node]:
            raise ValueError ('Duplicate neighbour')
        else:
            edge = (neighbour,cost)
            self.graph[node].append(edge)





if __name__ == "__main__":
    N = ['u','v','w','x','y','z']
    E = [('u','v'), ('u','x'), ('v','x'), ('v','w'), ('x','w'), ('x','y'), ('w','y'), ('w','z'), ('y','z')]
    g = Graph()
    for n in N:
        g.addNode(n)
        for e in E:
            if e[0] == n:
                g.addEdge(n, e[1])

    print(g.graph)
