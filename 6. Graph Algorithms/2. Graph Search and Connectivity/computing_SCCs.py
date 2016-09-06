from graph import *

def load_graph(filename):
    '''
    Parses the graph's edge list and constructs an directed

    Parameters:
        filename : name of the edge list file
    Assumes:
    Every row indicates an edge, the vertex label in first column is the tail
    and the vertex label in second column is the head (recall the graph is
    directed, and the edges are directed from the first column vertex to the
    second column vertex).
        e.g.
            2 47646
        Indicates an edge from node 2 directed at node 47646

    Returns:
        A directed graph based on the edge list.
    '''

    print("Loading graph from file...")

    f = open(filename)
    data = f.read().split('\n')
    g = Digraph()

    for line in data:
        values = line.split()
        if len(values) != 0:
            src = Node(values[0])
            dest = Node(values[1])
            try:
                g.addNode(src)
            except ValueError:
                pass
            try:
                g.addNode(dest)
            except ValueError:
                pass
            e = Edge(src, dest)
            g.addEdge(e)
    return g

g = load_graph('SCC.txt')
print('Computing SCCs...')
scc = g.computeSCCs()      # compute all SCCs using Kosaraju's 2-pass algorithm
scc_sizes = sorted([len(scc[i]) for i in scc.keys()])
top5 = scc_sizes[len(scc_sizes) - 5:len(scc_sizes)]
top5                       # print the sizes of the five larges SCCs
