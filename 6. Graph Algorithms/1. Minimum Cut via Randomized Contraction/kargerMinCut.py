# Michael D. Salerno

from graph import *
import random
import math
import copy


def kargerMinCut(g, reps=float('inf')):
    '''
    My implementation of Karger's randomized O(n^2 * m) algorithm for computing
    a minimum cut (that is, a cut with the fewest number of crossing edges) of
    an undirected graph.

    Input:  An undirected graph as defined in my graph.py script
    (parallel edges allowed) and the number of trials of Karger's contraction
    algorithm to run.
    Output: A tuple containing the size of the best cut discovered during the
    repeated trials and a two-node graph representation of the graph after this
    cut is applied.

    The contraction algorithm has a low success probability, lower bounded by
    1/n^2, however, it can be repeated for an arbitrary number of independent
    trials in order to increase the probability that a minimum cut is
    discovered.

    If the "reps" argument is left unspecified, then the contraction algorithm
    is run n^2 * log(n) times, which upper bounds the probability of failure by
    1/n.  This can take a very long time and, for the example data provided
    here, a much smaller of repetitions appeared to be sufficient.
    '''
    if reps == float('inf'):
        n = g.countNodes()
        reps = n**2 * math.log(n)  # this many repetitions of the contraction algorithm will upper bound the probability of failure by 1/n; very long run time
    minCut = float('inf')
    gMin = g
    for i in range(int(math.ceil(reps))):
        random.seed(i)
        gContracted = rContract(copy.deepcopy(g))  # pass a copy of the graph to the contraction algorithm in order to avoid modifying the original
        key = list(gContracted.edges.keys())[0]        # pick one of the two nodes in the contracted graph
        cut = len(gContracted.edges[key])
        if cut < minCut:
            minCut = cut        # if the number of edges between the two nodes is less than the minCut found so far, then replace the current minCut
            gMin = gContracted  # set gMin to the new best contracted graph
    return (minCut, gMin)


def rContract(g):
    '''
    Sub-procedure containing Karger's randomized contraction algorithm.

    Input:  An undirected graph as defined in my graph.py script
    (parallel edges allowed)
    Output:  A two-node graph representation of the original graph after
    repeated random contractions.
    '''
    while g.countNodes() > 2:
        edges = g.__str__().split()                # list every edge
        choice = random.choice(edges).split('->')  # pick one edge at random, split into [v1, v2]
        random.shuffle(choice)                     # shuffle order nodes
        aNode = Node(choice[0])                    # set absorbing node
        cNode = Node(choice[1])                    # set node to contract
        mNode = Node('(' + choice[0] + ',' + choice[1] + ')')  # new node representing the merged node
        g.addNode(mNode)                           # add supernode to graph
        transferNodes = g.childrenOf(aNode)        # list of aNode's neighbors
        for v in transferNodes:                    # transfer all of aNodes edges to the supernode mNode
            e = Edge(mNode, v)
            g.addUndirectedEdge(e)
        g.removeNode(aNode)                        # remove aNode; we can now use relabeled mNode
        adjNodes = g.childrenOf(cNode)             # list of cNode's neighbors
        for v in adjNodes:
            if v != mNode:                         # transfer edges to supernode
                newEdge = Edge(mNode, v)
                g.addUndirectedEdge(newEdge)
        g.removeNode(cNode)                        # removes the contracted node and all edges it participates in
        try:
            g.removeUndirectedEdge(Edge(mNode, mNode))   # remove self-loops, if any
        except ValueError:
            pass
    return g

def load_graph(filename):
    """
    Parses the graph adjacency and constructs an undirected graph

    Parameters:
        filename : name of the adjacency list file

    Assumes:
        The first column in the file represents the vertex label, and the
        particular row (other entries except the first column) tells all the
        vertices that the vertex is adjacent to.
        Each entry in the adjacency list consists of positive integers
        separated by a blank space.
        e.g.
            32 76 54 23
        This indicates edges from 32 to 76, 32 to 54, and 32 to 23.

    Returns:
        a directed graph based on the adjacency list.
    """

    print("Loading graph from file...")

    f = open(filename)
    data = f.read().split('\n')
    g = Digraph()   # Although the graph is undirected, kargerMinCut.txt is an adjancency list,
                    # to it is more convenient to construct using Digraph() instead of Graph()

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
