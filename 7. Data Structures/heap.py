from math import floor
from copy import deepcopy

#TODO Parameterize bubble functions for multiple inheritance
class Heap(object):
    '''
    A heap.
    '''
    def __init__(self, elements = []):
        self.locations = {}
        self.elements = deepcopy(elements)
        self.heapify()
    def size(self):
        return len(self.elements)
    def swap_indices(self, i, j):
        self.elements[i], self.elements[j] = self.elements[j], self.elements[i]
        self.locations[self.elements[i]] = i
        self.locations[self.elements[j]] = j
    def bubble_up(self, index):
        while index > 1:
            parent = floor(index/2)
            if self.elements[parent-1] <= self.elements[index-1]:
                break
            self.swap_indices(parent-1, index-1)
            index = parent
    def bubble_down(self, index):
        left = 2*index
        right = 2*index + 1
        while left <= self.size():
            if right > self.size() or \
            self.elements[left-1] <= self.elements[right-1]:
                min_child = left
            else:
                min_child = right
            if self.elements[min_child-1] >= self.elements[index-1]:
                break
            self.swap_indices(min_child-1, index-1)
            index = min_child
            left = 2*index
            right = 2*index + 1
    def heapify(self):
        for i in range(len(self.elements), 0, -1):
            self.locations[self.elements[i-1]] = i - 1
            self.bubble_down(i)


class MinHeap(Heap):
    def __init__(self, elements = []):
        super(MinHeap, self).__init__(elements)
    def insert(self, x):
        self.elements.append(x)
        self.locations[x] = len(self.elements) - 1
        super(MinHeap, self).bubble_up(index = len(self.elements))
    def delete(self, x, extract = False):
        if self.size() == 0:
            raise IndexError('extract from empty heap')
        index = self.locations[x] + 1
        super(MinHeap, self).swap_indices(index-1, self.size()-1)
        removed = self.elements.pop()
        self.locations.pop(removed)
        super(MinHeap, self).bubble_up(index)
        super(MinHeap, self).bubble_down(index)
        if extract:
            return removed
    def extract_min(self):
        return self.delete(self.elements[0], extract = True)
