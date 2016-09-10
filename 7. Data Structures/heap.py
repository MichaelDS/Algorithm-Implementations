from math import floor
from copy import deepcopy


class Heap(object):
    '''
    A heap.
    '''
    def __init__(self, elements = [], max_heap = False):
        self.locations = {}
        self.elements = deepcopy(elements)
        self.heapify(max_heap)
    def size(self):
        return len(self.elements)
    def swap_indices(self, i, j):
        self.elements[i], self.elements[j] = self.elements[j], self.elements[i]
        self.locations[self.elements[i]] = i
        self.locations[self.elements[j]] = j
    def is_heap(self, parent, child, max_heap = False):
        if not max_heap:
            return self.elements[parent-1] <= self.elements[child-1]
        else:
            return self.elements[parent-1] >= self.elements[child-1]
    def select_child(self, left, right, max_heap = False):
        '''
        This method is customized for use within the main while-loop of the
        bubble_down() function.  Use elsewhere cautiously.
        '''
        if right > self.size():
            return left
        if not max_heap and self.elements[left-1] <= self.elements[right-1] or \
        max_heap and self.elements[left-1] >= self.elements[right-1]:
            return left
        else:
            return right
    def bubble_up(self, index, max_heap = False):
        while index > 1:
            parent = floor(index/2)
            if self.is_heap(parent, index, max_heap):
                break
            self.swap_indices(parent-1, index-1)
            index = parent
    def bubble_down(self, index, max_heap = False):
        left = 2*index
        right = 2*index + 1
        while left <= self.size():
            m_child = self.select_child(left, right, max_heap)
            if self.is_heap(index, m_child, max_heap):
                break
            self.swap_indices(m_child-1, index-1)
            index = m_child
            left = 2*index
            right = 2*index + 1
    def heapify(self, max_heap = False):
        for i in range(len(self.elements), 0, -1):
            self.locations[self.elements[i-1]] = i - 1
            self.bubble_down(i, max_heap)


class MinHeap(Heap):
    def __init__(self, elements = []):
        super(MinHeap, self).__init__(elements)
    def insert(self, x):
        self.elements.append(x)
        self.locations[x] = len(self.elements) - 1
        super(MinHeap, self).bubble_up(index = len(self.elements))
    def delete(self, x, extract = False):
        if self.size() == 0:
            raise IndexError('deletion from empty heap')
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


class MaxHeap(Heap):
    def __init__(self, elements = []):
        super(MaxHeap, self).__init__(elements, True)
    def insert(self, x):
        self.elements.append(x)
        self.locations[x] = len(self.elements) - 1
        super(MaxHeap, self).bubble_up(len(self.elements), True)
    def delete(self, x, extract = False):
        if self.size() == 0:
            raise IndexError('deletion from empty heap')
        index = self.locations[x] + 1
        super(MaxHeap, self).swap_indices(index-1, self.size()-1)
        removed = self.elements.pop()
        self.locations.pop(removed)
        super(MaxHeap, self).bubble_up(index, True)
        super(MaxHeap, self).bubble_down(index, True)
        if extract:
            return removed
    def extract_max(self):
        return self.delete(self.elements[0], extract = True)
