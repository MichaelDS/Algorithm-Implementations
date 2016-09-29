from hashTable import HashTable
from multiprocessing import Pool
# from multiprocessing.dummy import Pool as ThreadPool

f = open('2sum.txt')
data = f.read().split('\n')
data.pop()                   # last line was an empty string; discard
data = list(map(int, data))

#TODO: Figure out Pool nonsense
def two_sum(data = data):
    hashset = HashTable()
    hits = HashTable()
    for k in data:
        hashset[k] = None
    def ts(t):
        print(t)
        for x in data:
            y = t - x
            if y in hashset and x != y:
                return 1
        return 0
    p = Pool()
    return sum(p.map(ts, range(-10000, 10001)))


def two_sum_range(data = data, target = range(-10000, 10001)):
    hashset = HashTable()
    hits = HashTable()
    for k in data:
        hashset[k] = None
    for t in target:
        print(t)
        for x in data:
            y = t - x
            if y in hashset and x != y:
                hits[t] = None
                break
    return hits

def two_sum_range2(data = data, lower = -10000, upper = 10000):
    data.sort()
    target = range(lower, upper+1)
    hits = HashTable()
    left = 0
    right = len(data) - 1
    while left != right:
        x, y = data[left], data[right]
        if x + y > upper:
            right -= 1
        elif x + y < lower:
            left += 1
        else:
            if x != y:
                hits[x+y] = None
            for k in data[(left+1):right]:
                if x + k in target and x != k:
                    hits[x+k] = None
                if y + k in target and y != k:
                    hits[y+k] = None
            left += 1
            right -= 1
    return hits

hits = two_sum_range(data)
