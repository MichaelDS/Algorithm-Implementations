from math import floor

class heap(object):
    '''
    A heap.
    '''
    def __init__(self):
        self.elements = []
    def size(self):
        return len(self.elements)
    def insert(self, x):
        self.elements.append(x)
        index = len(self.elements)
        while index > 1:
            parent = floor(index/2)
            if self.elements[parent-1] <= self.elements[index-1]:
                break
            self.elements[parent-1], self.elements[index-1] = \
            self.elements[index-1], self.elements[parent-1]
            index = parent
    def extract(self):
        if self.size() == 0:
            raise IndexError('extract from empty heap')
        self.elements[0], self.elements[self.size()-1] = \
        self.elements[self.size()-1], self.elements[0]
        minimum = self.elements.pop()
        index = 1
        left = 2*index
        right = 2*index + 1
        while left <= self.size():
            if right > self.size() or self.elements[left-1] <= self.elements[right-1]:
                min_child = left
            else:
                min_child = right
            if self.elements[min_child-1] >= self.elements[index-1]:
                break
            self.elements[min_child-1], self.elements[index-1] = \
            self.elements[index-1], self.elements[min_child-1]
            index = min_child
            left = 2*index
            right = 2*index + 1
        return minimum
