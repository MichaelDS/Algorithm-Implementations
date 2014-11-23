# A set of data structures to represent graphs

class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name     
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        # Override the default hash method; simplifies use of dictionary
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):  #src and dest should be nodes
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)
        
class WeightedEdge(Edge):
    '''
    Subclass of edge; supports for context-specific edge weights.
    '''
    def __init__(self, src, dest, totalDist, outdoorDist):
        Edge.__init__(self, src, dest)
        self.totalDist = float(totalDist)
        self.outdoorDist = float(outdoorDist)
        
    def getTotalDistance(self):
        return self.totalDist
        
    def getOutdoorDistance(self):
        return self.outdoorDist
        
    def __str__(self):
        return '{0}->{1} ({2}, {3})'.format(self.src, self.dest, self.totalDist, self.outdoorDist)

class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates
        # Entries into a set must be hashable 
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list 
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.nodes = set([])
        self.edges = {}      # Python dictionary (hashtable); each key represents a node and they key's values represent adjacent nodes
    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, this to makes sure a duplicate
            # entry is not added for the same node in the self.edges list
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def removeNode(self, node):
        if node not in self.nodes:
            raise ValueError('Node not in graph')
        children = self.childrenOf(node)
        self.nodes.remove(node)                        # remove from set of nodes
        self.edges.pop(node)                           # remove as a key from the edges hashtable
        for v in children:                            # remove as a value from the edges hashtable
            self.edges[v] = [n for n in self.edges[v] if n != node]
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def addUndirectedEdge(self, edge):
        self.addEdge(edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        self.addEdge(rev)
    def removeEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.edges.keys() and dest in self.edges[src]):
            raise ValueError('Edge not in graph')
        self.edges[src].remove(dest)
    def removeUndirectedEdge(self, edge):
        self.removeEdge(edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        self.removeEdge(rev)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def countNodes(self):
        return len(self.nodes)
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[Node(k)]:         #Modified from str to Node
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]

        
class WeightedDigraph(Digraph):
    '''
    A subclass of Digraph; supports context-specific weighted edges
    '''
    def __init__(self):
        Digraph.__init__(self)
        self.weights = {}
        
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        totalDist = edge.getTotalDistance()
        outdoorDist = edge.getOutdoorDistance()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append([dest, (float(totalDist), float(outdoorDist))])  #Grader required this format
        self.weights[(src, dest)] = (totalDist, outdoorDist)
    
    def getDist(self, src, dest):
        return self.weights[(src, dest)][0]
        
    def getOutDist(self, src, dest):
        return self.weights[(src, dest)][1]
        
    def childrenOf(self, node):
        return [e[0] for e in self.edges[node]]
        
    def __str__(self):
        result = ''
        for node in self.edges:
            for e in self.edges[node]:
                # result += str(e) + '\n'  -- grader wanted floats AND had to change self.edges format
                result = '{0}{1}->{2} ({3}, {4})\n'.format(result, node, \
                e[0], e[1][0], e[1][1])
        return result[:-1]
        
class Graph(Digraph):
    '''
    An undirected graph; special instance of a digraph
    '''
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)
    def removeEdge(self, edge):
        Digraph.removeEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.removeEdge(self, rev)
        '''
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.edges.keys() and dest in self.edges[src]):
            raise ValueError('Edge not in graph')
        self.edges[src].remove(dest)
        self.edges[dest].remove[src]
        '''
