##urya Avinash Avala, z5096886
#PYTHON 3 ONLY, doesn't work with Python2
#hosted on bitbucket as a private repo, will be made public after one week on the assignment deadline
#git@bitbucket.org:saavala2/network.git

#Class for implementation of Graphs

class Node:
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
