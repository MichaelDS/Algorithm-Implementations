# Michael D. Salerno

def nextPowerOfTwo(n):
    '''
    Finds the next highest power of 2 of an up to 64-bit integer by copying 
    the highest set bit to all of the lower bits and the adding one.  The 
    initial decrement is to ensure that it works for numbers that are already
    powers of 2.
    '''
    
    n -= 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    n |= n >> 32
    n += 1
    
    return n