from graph import *

def load_graph(filename):
    '''
    Parses the graph adjacency and constructs a weighted directed graph.

    Parameters:
        filename : name of the adjacency list file

    Assumes:
    Each row consists of the node tuples that are adjacent to that particular
    vertex along with the weight of that edge. For example, if the 6th row has
    6 as the first entry, this indicates that this row corresponds to the vertex
    labeled 6. If the next entry of this row "141,8200" then there is an edge
    between vertex 6 and vertex 141 that has weight 8200. The rest of the pairs
    of this row indicate the other vertices adjacent to vertex 6 and the
    weights of the corresponding edges.
        e.g.
            1	80,982	163,8164	170,2620	145,648
        This indicates edges from 1 to 80, 163, 170, and 145 with respective
        weights of 982, 8164, 2620, and 648.

    Returns:
        A weighted directed graph based on the adjacency list.
    '''

    print("Loading graph from file...")

    f = open(filename)
    data = f.read().split('\n')
    g = WeightedDigraph()

    for line in data:
        values = line.split()
        if len(values) != 0:
            src = Node(values[0])
            try:
                g.addNode(src)
            except ValueError:
                pass
            for t in map(lambda x:x.split(','), values[1:]):
                dest = Node(t[0])
                try:
                    g.addNode(dest)
                except ValueError:
                    pass
                weight = t[1]
                e = WeightedEdge(src, dest, weight)
                g.addEdge(e)
    return g

g = load_graph('dijkstraData.txt')
distances = g.shortest_paths(Node(1))  # compute all geodesics originating at node 1
nodes = [Node(i) for i in [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]]
print([distances[d] for d in nodes])
