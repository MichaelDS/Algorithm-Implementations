
# TODO: Implement doubley-linked version and set up class heirarchy
class LLNode(object):
    __slots__ = ('key', 'value', 'next')
    def __init__(self, key = None, value = None, next = None):
        self.key = key
        self.value = value
        self.next = next
    def get_key(self):
        return self.key
    def get_value(self):
        return self.value
    def get_next(self):
        return self.next
    def set_next(self, x):
        self.next = x
    def set_value(self, x):
        self.value = x
    def __str__(self):
        return str(self.key) + ':' + str(self.value)

class LinkedList(object):
    '''
    A simple singley-linked list.
    '''
    __slots__ = ('head', )
    def __init__(self, head = None):
        self.head = head
    def __len__(self):
        if self.head == None:
            return 0
        node = self.head
        size = 1
        while node.get_next():
            node = node.get_next()
            size += 1
        return size
    def __contains__(self, key):
        try:
            self.search(key)
            return True
        except KeyError:
            return False
    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.get_next()
    def insert(self, k, v = None):      # Perhaps use this default behavior to create a set
        if self.__contains__(k):
            node = self.search(k)
            node.set_value(v)
        else:
            node = LLNode(k, v, self.head)
            self.head = node
    def search(self, k):
        current = self.head
        while current:
            if current.key == k:
                return current
            current = current.get_next()
        raise KeyError(str(k))
    def pop(self, k):
        current = self.head
        previous = None
        while current:
            if current.key == k:
                if not previous:
                    self.head = current.get_next()
                else:
                    previous.set_next(current.get_next())
                    current.set_next(None)
                return current
            previous = current
            current = current.get_next()
        raise KeyError(str(k))
    def reverse(self):
        def _reverse(node):
            if not node.get_next():
                self.head = node
                return node
            else:
                tail = _reverse(node.get_next())
                node.set_next(None)
                tail.set_next(node)
                return node
        _reverse(self.head)
    def __str__(self):
        if not self.head:
            return ''
        def _str(node):
            if not node.get_next():
                return '{0}'.format(node.get_key())
            else:
                return '{0}->'.format(node.get_key()) + _str(node.get_next())
        return _str(self.head)
