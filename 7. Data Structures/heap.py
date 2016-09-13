from math import floor
from copy import copy

class Heap(object):
    '''
    A heap.
    '''
    def __init__(self, elements = [], key = lambda x:x, max_heap = False):
        self.locations = {}
        self.elements = copy(elements)
        self.key = key
        self.heapify(self.key, max_heap)
    def __contains__(self, x):
        return x in self.locations
    def size(self):
        return len(self.elements)
    def is_empty(self):
        return self.size() == 0
    #def contains(self, x):
        #return x in self.locations
    def swap_indices(self, i, j):
        self.elements[i], self.elements[j] = self.elements[j], self.elements[i]
        self.locations[self.elements[i]] = i
        self.locations[self.elements[j]] = j
    def is_heap(self, parent, child, key, max_heap = False):
        if not max_heap:
            return key(self.elements[parent-1]) <= key(self.elements[child-1])
        else:
            return key(self.elements[parent-1]) >= key(self.elements[child-1])
    def select_child(self, left, right, key, max_heap = False):
        '''
        This method is designed for use within the main while-loop of the
        bubble_down() function.  Use elsewhere cautiously.
        '''
        if right > self.size():
            return left
        if not max_heap and key(self.elements[left-1]) <= key(self.elements[right-1]) or \
        max_heap and key(self.elements[left-1]) >= key(self.elements[right-1]):
            return left
        else:
            return right
    def bubble_up(self, index, key, max_heap = False):
        while index > 1:
            parent = floor(index/2)
            if self.is_heap(parent, index, key, max_heap):
                break
            self.swap_indices(parent-1, index-1)
            index = parent
    def bubble_down(self, index, key, max_heap = False):
        left = 2*index
        right = 2*index + 1
        while left <= self.size():
            m_child = self.select_child(left, right, key, max_heap)
            if self.is_heap(index, m_child, key, max_heap):
                break
            self.swap_indices(m_child-1, index-1)
            index = m_child
            left = 2*index
            right = 2*index + 1
    def heapify(self, key, max_heap = False):
        for i in range(len(self.elements), 0, -1):
            self.locations[self.elements[i-1]] = i - 1
            self.bubble_down(i, key, max_heap)


class MinHeap(Heap):
    def __init__(self, elements = [], key = lambda x:x):
        super(MinHeap, self).__init__(elements, key)
    def insert(self, x):
        self.elements.append(x)
        self.locations[x] = len(self.elements) - 1
        super(MinHeap, self).bubble_up(index = len(self.elements), key = self.key)
    def delete(self, x, extract = False):
        if self.size() == 0:
            raise IndexError('deletion from empty heap')
        index = self.locations[x] + 1
        super(MinHeap, self).swap_indices(index-1, self.size()-1)  #make consistent
        removed = self.elements.pop()
        self.locations.pop(removed)
        if index <= len(self.elements):   # skip bubbling when deleting the right-most element
            super(MinHeap, self).bubble_up(index, self.key)
            super(MinHeap, self).bubble_down(index, self.key)
        if extract:
            return removed
    def extract_min(self):
        return self.delete(self.elements[0], extract = True)


class MaxHeap(Heap):
    def __init__(self, elements = [], key = lambda x:x):
        super(MaxHeap, self).__init__(elements, key, True)
    def insert(self, x):
        self.elements.append(x)
        self.locations[x] = len(self.elements) - 1
        super(MaxHeap, self).bubble_up(len(self.elements), self.key, True)
    def delete(self, x, extract = False):
        if self.size() == 0:
            raise IndexError('deletion from empty heap')
        index = self.locations[x] + 1
        super(MaxHeap, self).swap_indices(index-1, self.size()-1)
        removed = self.elements.pop()
        self.locations.pop(removed)
        if index <= len(self.elements):   # skip bubbling when deleting the right-most element
            super(MaxHeap, self).bubble_up(index, self.key, True)
            super(MaxHeap, self).bubble_down(index, self.key, True)
        if extract:
            return removed
    def extract_max(self):
        return self.delete(self.elements[0], extract = True)
