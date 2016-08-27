# Import everything from `graph.py`
from graph import *
import random, math, copy

def kargerMinCut(g, reps, updateLabels = False):
    '''
    Input:  An undirected graph, the number of repetitions for which to run
    the contraction algorithm, and and optional flag indicating whether or not
    to re-label the contracted graph.
    Output: The min-cut (the minimum number of crossing edges) with O(1/n)
    chance of failure, where n is the number of nodes in the graph
    '''
    #n = g.countNodes()
    #reps = n**2 * math.log(n)  # this many repetitions of the contraction algorithm will upper bound the probability of failure by 1/n; very long run time
    minCut = float('inf')
    for i in range(int(math.ceil(reps))):
        print(('Iteration ' + str(i + 1)))
        if not updateLabels:
            gContracted = rContract(copy.deepcopy(g))  # pass a copy of the graph to the contraction algorithm in order to avoid modifying the original;
        else:
            gContracted = rContract2(copy.deepcopy(g)) # if specified, use rContract2 to re-label the nodes appropriately; significantly longer running time
        key = list(gContracted.edges.keys())[0]         # pick one of the two nodes in the contracted graph
        if len(gContracted.edges[key]) < minCut:
            minCut = len(gContracted.edges[key])  # if the number of edges between the two nodes is less than the minCut found so far, then replace the current minCut
    return minCut

def rContract(g):
    '''
    Input:  An undirected graph
    Output: The graph after contracting to 2 nodes
    '''

    while g.countNodes() > 2:
        edges = g.__str__().split()              # list every edge
        pick = random.choice(edges).split('->')  # pick one edge at random, split into [v1, v2]
        random.shuffle(pick)                     # shuffle the order of the nodes
        cNode = Node(pick[0])                    # pick the node to contract
        aNode = Node(pick[1])                    # the node absorbing cNode
        adjNodes = g.childrenOf(cNode)           # list of nodes adjacent to cNode
        for v in adjNodes[:]:
            cEdge = Edge(cNode, v)
            g.removeUndirectedEdge(cEdge)        # remove edges attached to the node being contracted
            if v != aNode:                       # the contracted edge and any edges parallel to it do not need to be re-inserted into the graph
                newEdge = Edge(aNode, v)
                g.addUndirectedEdge(newEdge)     # re-insert other deleted edges such that they originate from the merged node
        g.removeNode(cNode)                      # remove the contracted node
    return g

def rContract2(g):
    '''
    Input:  An undirected graph
    Output: The graph after contracting to 2 nodes with updated labels
    '''

    while g.countNodes() > 2:
        edges = g.__str__().split()              # list every edge
        pick = random.choice(edges).split('->')  # pick one edge at random, split into [v1, v2]
        random.shuffle(pick)                     # shuffle the order of the nodes
        cNode = Node(pick[0])                    # pick the node to contract
        aNode = Node(pick[1])                    # the node absorbing cNode
        mNode = Node('(' + pick[0] + ',' + pick[1] + ')')  # new node representing the merged node; for some reason, causes errors without parentheses.  Likely to do with Python string behavior.
        g.addNode(mNode)                         # add the merged node to the graph
        adjNodes = g.childrenOf(aNode)           # list of nodes adjacent to aNode
        for v in adjNodes[:]:                   # transfer all edges associated with aNode to mNode
            e = Edge(mNode, v)
            g.addUndirectedEdge(e)
        g.removeNode(aNode)
        adjNodes = g.childrenOf(cNode)           # list of nodes adjacent to cNode
        for v in adjNodes[:]:
            cEdge = Edge(cNode, v)
            g.removeUndirectedEdge(cEdge)        # remove edges attached to the node being contracted
            if v != mNode:                       # the contracted edge and any edges parallel to it do not need to be re-inserted into the graph
                newEdge = Edge(mNode, v)
                g.addUndirectedEdge(newEdge)     # re-insert other deleted edges such that they originate from the merged node
        g.removeNode(cNode)                      # remove the contracted node
    return g


def load_graph(filename):
    """
    Parses the map file and constructs an undirected graph

    Parameters:
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """

    print("Loading graph from file...")

    f = open(filename)
    data = f.read().split('\n')
    g = Digraph()   # Although the graph is undirected, kargerMinCut.txt is an adjancency list, so it is more convenient to construct using Digraph() instead of Graph()

    for line in data:
        values = line.split()
        if len(values) != 0:       # last line in kargerMinCut.txt is an empty string
            src = Node(values[0])
            try:
                g.addNode(src)
            except ValueError:
                pass
            for d in values[1:]:
                dest = Node(d)
                try:
                    g.addNode(dest)
                except ValueError:
                    pass
                e = Edge(src, dest)
                g.addEdge(e)
    return g
