# A set of data structures to represent graphs

from queue import Queue
import sys
sys.setrecursionlimit(1000000)

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
    def __init__(self, src, dest):  # src and dest should be nodes
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
    def __init__(self, src, dest, weight):  # src and dest should be nodes
        Edge.__init__(self, src, dest, weight)
        self.weight = float(weight)

    def getWeight(self):
        return self.weight

    def __str__(self):
        return '{0}->{1} ({2})'.format(self.src, self.dest, self.weight)

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
        self.edges = {}      # Python dictionary (hashtable); each key represents a node and the key's values represent adjacent nodes
    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, this makes sure a duplicate
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
        for v in children:                             # remove as a value from the edges hashtable
            self.edges[v] = [n for n in self.edges[v] if n != node]  # can this be optimized?  Consider directed vs undirected cases.  Case for: parallel  edges
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
        if not(src in list(self.edges.keys()) and dest in self.edges[src]):
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
    def bfs(self, s):               # FINISH IMPLEMENTING THIS
        explored = set([s])
        q = Queue([s])
        while q:
            v = q.dequeue()
    def reverse_edges(self, overwrite = True):
        rev = {}
        for k in self.edges:
            for v in self.edges[k]:
                if v in rev:
                    rev[v].append(k)
                else:
                    rev[v] = [k]
        if overwrite:
            self.edges = rev
        else:
            return rev
    def computeSCCs(self):
        '''
        NOTE: Kosaraju's 2-pass algorithm requires that nodes be labeled
        1 to n, where n is the number of nodes in the graph.
        '''
        g_rev = self.reverse_edges(overwrite = False) # reversed edges
        scc = {}                  # for mapping leader(scc) labels (2nd pass)
        order = {}                # for mapping finishing times (1st pass)
        explored = set()          # keeps track of explored nodes
        t = 0                     # keeps track of finishing times (1st pass)
        s = None                  # keeps track of leader node (2nd pass)
        
# This recursive version of dfs appears to work correctly, however, on larger
# graphs it causes a maximum recursion depth error because Python does
# not support tail recursion.  For this reason, I implemented an iterative
# version using a stack.
#
#        def dfs(g_edges, v):
#            explored.add(v)
#            scc[s].append(v)
#            if v in g_edges:
#                for i in g_edges[v]:
#                    if i not in explored:
#                        dfs(g_edges, i)
#            nonlocal t
#            t += 1
#            order[t] = v

        def dfs(g_edges, v):
            '''
            Iterative version of depth-first search customized for Kosaraju's
            2-pass algorithm.
            Input: A dictionary representation of the graph's adjacency list
            and a starting vertex.
            Output: No output.
            '''
            stack = [v]
            while stack:
                current = stack.pop()
                if current not in explored:
                    explored.add(current)
                    scc[s].append(current)
                if current not in g_edges or all(i in explored for i in g_edges[current]):
                    nonlocal t
                    t += 1
                    order[t] = current
                else:
                    stack.append(current)
                    for e in g_edges[current]:
                        if e not in explored:
                            stack.append(e)
                            break
        def dfs_loop(edges, preprocessing = False):
            '''
            A procedure for searching over all components of a graph using
            depth-first search, customized for Kosaraju's 2-pass algorithm.
            Input: A dictionary representation of the graph's adjacency list
            and a boolean indicating whether the procedure is being called for
            the first or second pass of Kosaraju's algorithm.
            Output: No output.
            '''
            nonlocal s
            for i in range(self.countNodes(), 0, -1):
                if preprocessing:
                    v = Node(i)
                else:
                    v = order[i]
                if v not in explored:
                    s = v
                    scc[s] = []
                    dfs(edges, v)
        dfs_loop(g_rev, preprocessing = True)   # 1st pass
        scc = {}
        explored = set()
        dfs_loop(self.edges)                    # 2nd pass
        return scc
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[Node(k)]:         # Modified from str to Node
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
        weight = edge.getWeight()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append((dest, weight))
        self.weights[(src, dest)] = weight

    def getWeight(self, src, dest):
        return self.weights[(src, dest)]

    def childrenOf(self, node):
        return [e[0] for e in self.edges[node]]  # accessing 0th element because the adjacency list is a list of tuples in the weighted digraph

    def __str__(self):
        result = ''
        for node in self.edges:
            for e in self.edges[node]:
                result = '{0}{1}->{2} ({3})\n'.format(result, node, e[0], e[1])
        return result[:-1]

class Graph(Digraph):
    '''
    An undirected graph; special instance of a digraph
    '''
    def addEdge(self, edge):
        Digraph.addUndirectedEdge(self, edge)
    def removeEdge(self, edge):
        Digraph.removeUndirectedEdge(self, edge)
