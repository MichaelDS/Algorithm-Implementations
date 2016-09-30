from heap import MinHeap, MaxHeap
from binarySearchTrees import RBTree
from math import ceil

f = open('Median.txt')
data = f.read().split('\n')
data.pop()                   # last line was an empty string; discard
data = list(map(int, data))

def median_maintenance(data):
    yield data[0]
    if data[0] < data[1]:
        h_high, h_low = MinHeap([data[1]]), MaxHeap([data[0]])
    else:
        h_high, h_low = MinHeap([data[0]]), MaxHeap([data[1]])
    median = h_low.extract_max()
    h_low.insert(median)
    yield median
    for k in data[2:]:
        lower, upper = h_low.extract_max(), h_high.extract_min()
        if k <= lower:
            h_low.insert(k)
        else:
            h_high.insert(k)
        h_low.insert(lower)
        h_high.insert(upper)
        if abs(h_high.size() - h_low.size()) > 1:
            if h_high.size() > h_low.size():
                h_low.insert(h_high.extract_min())
            else:
                h_high.insert(h_low.extract_max())
        if (h_high.size() + h_low.size()) % 2 == 0 or h_low.size() > h_high.size():
            median = h_low.extract_max()
            h_low.insert(median)
            yield median
        else:
            median = h_high.extract_min()
            h_high.insert(median)
            yield median

def tree_median_maintenance(data):
    rbt = RBTree()
    for k in data:
        rbt.insert(k)
        yield rbt.select(ceil(rbt.size()/2))


g = median_maintenance(data)
m = [k for k in g]
sum(m) % 10000

# The select function for binary search trees is implemented recursively;
# fails due to lack of tail recursion
# g2 = tree_median_maintenance(data)
# m2 = [k for k in g2]
# sum(m2) % 10000
