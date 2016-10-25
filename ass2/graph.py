##urya Avinash Avala, z5096886
#PYTHON 3 ONLY, doesn't work with Python2
#hosted on bitbucket as a private repo, will be made public after one week on the assignment deadline
#git@bitbucket.org:saavala2/network.git

#Class for implementation of Graphs

class Node:
    '''
    Node object hold the name of the Node
    '''
    def __init__(self,name):
        '''
        Name is a string with the name of the node
        '''
        self.name = name

    def getName(self):
        '''
        Returns the name of the Node
        '''
        return self.name

    def __str__(self):
        '''
        Prints name
        '''
        return self.name

class Edge:
    '''
    Assumes src, dst are nodes
    Edge from src->dst
    '''
    def __init__(self,src,dst):
        self.src = src
        self.dst = dst

    def getSource(self):
        return self.src

    def getDestination(self):
        return self.dst

    def __str__(self):
        return self.src.getName() + '->' + self.dst.getName()



class Graph:
    '''
    Edge is a dict with key as node name and value as a list of adj nodes
    '''

    def __init__(self):
        '''
        Initiates dict edges
        '''
        self.edges = {}

    def addNode(self, node):
        if node in self.edges:
            raise ValueError ("Duplicate Error")
        else:
            self.edges[node] = []

    def addEdge(self, node, edge):
        pass


if __name__ == "__main__":
    src = Node('src')
    dst = Node('dst')
    e = Edge(src,dst)
    print(e)
