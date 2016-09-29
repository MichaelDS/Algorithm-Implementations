from primes import search_for_primes
from linkedList import LinkedList
from collections import MutableMapping

# TODO: Optimize len (iter?), implement set
class HashTable(MutableMapping):
    MINSIZE = 8
    __slots__ = ('n', 'table', 'size')
    def __init__(self, **kwargs):
        self.n = next(search_for_primes(self.MINSIZE))
        self.table = [LinkedList() for _ in range(self.n)]
        self.size = 0
        for k, v in kwargs.items():
            self.__setitem__(k, v)
    def __len__(self):     # returns the number of keys in the hash table
        return sum(map(len, self.table))   # can speed this up with self.size
    def __setitem__(self, key, value):
        if self.load_factor >= 0.75:
            self._resize(self.n * 4)
        if key not in self:
            self.size += 1
        self.table[self._hash(key, self.n)].insert(key, value)
    def __getitem__(self, key):
        return self.table[self._hash(key, self.n)].search(key).get_value()
    def __delitem__(self, key):
        if self.load_factor <= 0.16 and self.n // 4 >= 8 :
            self._resize(self.n // 4)  ## integer division
        self.size -= 1
        return self.table[self._hash(key, self.n)].pop(key)
    def __iter__(self):
        for ll in self.table:
            for item in ll:
                yield item.get_key()
    def _resize(self, new_n):
        old_table = self.table
        self.size = 0
        self.n = next(search_for_primes(new_n))
        self.table = [LinkedList() for _ in range(self.n)]
        # re-index data
        for ll in old_table:
            for item in ll:
                self.__setitem__(item.get_key(), item.get_value())
    def _hash(self, x, m):  # m should be set to an appropriately sized prime number in order to encourage uniqueness
        if isinstance(x, int):
            return x % m
        elif isinstance(x, str):
            if not x:
                return 0 # empty
            res = ord(x[0]) << 7
            for char in x:
                res = (1000003 * res) ^ ord(char)
            res = res ^ len(x)
            return res % m
        elif isinstance(x, tuple):
            res = 0x345678
            for item in x:
                res = (1000003 * res) ^ self._hash(item, m)
            res = res ^ len(x)
            return res % m
        else:
            raise ValueError('Invalid key type')
    @property
    def load_factor(self):
        '''
        Calculate the hash table's current load factor.
        '''
        try:
            return self.size/self.n
        except ZeroDivisionError:
            return 0
    def __str__(self):
        return '{' + ''.join(['{0}: {1}, '.format(k,v) for k, v in self.items()])[0:-2] + '}'
