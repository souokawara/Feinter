'''
Inspired by the paper arXiv:2311.13034 by Julián David Candela, and 1311.3897 by Mathew D. Penrose. This code will be a little lab to enhance the theory to my theoretical interest.
'''
import torch
from itertools import combinations
'''
As the introduction, I encode the theory of the P.Erdos and A.Renyi "On the Evolution of Random Graph" to python.
'''

# random graph class
class RandomGraph:
    # a random graph has at least two parameters n, N
    # n for the number of the vertices
    # N for the number of the edges
    def __init__(self,n,N):
        self.vertices = [[Vertex(i)] for i in range(1,n)]
        self.edges = [[Edge(edge[0],edge[1])] for edge in combinations(self.vertices, 2)]
        
        # the all available graphs on self.vertices
        self.c = []
        for r in range(1, len(self.edges)+1):
            self.c.extend(combinations(self.edges, r))
        
    # defining the property on the graphs a
    def define(self, a):
        return 0
    
    # regular threshold function
    
    # threshold distribution function
    
    # sharp threshold
    
    # sharp-threshold distribution function of the property a
            
         
# vetex on the random graph  
class Vertex(RandomGraph):
    # the vertex on the random graph has a label
    # and the own degree
    def __init__(self,id):
        self.id = id
    
    def get_degree(self):
        super()


# edge on the random graph
class Edge:
    # an edge needs the two vetex to exist
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        
graph = RandomGraph(5,3)
        

