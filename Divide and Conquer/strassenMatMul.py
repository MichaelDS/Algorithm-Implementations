# Michael D. Salerno

def strassenMatMul(x, y):
    '''
    My implementation of Strassen's subcubic algorithm for matrix 
    multiplication.  
    
    For multiplication of n x n matrices, the input size is defined as n.  
    Although strassenMatMul does not require that the matrices be square or
    identical, preprocessing steps pad the matrices with zeros so that all of 
    their dimensions end up being equal to the largest original dimension or to 
    the next largest power of 2 if the dimension was not originally a power of 
    2.  This allows the algorithm to handle multiplicable matrices of arbitrary
    dimensions.
    
    Input:  Two lists, x and y, that each represent a matrix.  Each list 
    contains a set of lists of equal length that correspond to the rows of the 
    matrix. 
    Output: A similarly formatted list representing their matrix product, if 
    defined; otherwise raises an appropriate error.
    
    This divide and conquer algorithm takes advantage of the fact that
    performing quadrant-wise multiplication of two matrices produces the same 
    results as ordinary matrix multiplication.  The matrices x and y are 
    partitioned into their quadrants with submatrices a through h and matrix
    product x*y defined as follows:
    
    x = [[a, b],      y = [[e, f],   so x*y = [[a*e + b*g, a*f + b*h],
         [c, d]]           [g, h]]             [c*e + d*g, c*f + d*h]]
        
    Making 8 recursive calls, each on a subproblem that is half-sized, in order
    to compute the necessary products and performing the necessary corresponding
    additions (quadratic time) results in an overall cubic time complexity, 
    which is no better than ordinary matrix multiplication.
    
    Instead, Strassen's algorithm reduces the number of recursive calls to 7 by
    constructing the product matrix out of the following 7 products:
    
    p1 = a*(f-h), p2 = (a+b)*h, p3 = (c+d)*e, p4 = d(g-e), p5 = (a+d)*(e+h),
    p6 = (b-d)*(g+h), p7 = (a-c)*(e+f)
        
    The product matrix can then be constructed as x*y = [[p5+-p4-p2+p6, p1+p2],
                                                         [p3+p4, p1+p5-p3-p7]]
                                                         
    This algorithm achieves a subcubic asymptotic time complexity.  Its 
    recurrences can be expressed as T(n) = 7*T(n/2) + O(n^2); thus, by the 
    Master Theorem, its asymptotic time complexity is O(n^log2(7)) which is 
    approximately O(n^2.8074).
    '''
    
    import numpy as np
    
    x = np.matrix(x)
    y = np.matrix(y)
    
    if x.shape[1] != y.shape[0]:
        
        raise ValueError('The input matrices are misaligned; matrix \
multiplication x * y is defined only if the number of columns in x is equal to \
the number of rows in y.')
        
    #The following steps, up until the strassen function, enable strassenMatMul 
    #to handle matrices with arbitrary dimensions; in other words, non-square
    #matrices, dimensions that are not powers of two, and matrices of 
    #differing sizes.  If it can be assumed that strassenMatMul will only be
    #passed square matrices with identical dimensions that are powers of two,
    #then these preprocessing steps, as well as the post-processing steps for 
    #removing padded zeroes, are not necessary.
    
    resultNRows = x.shape[0]   #saving the inner dimensions for final processing of result matrix
    resultNCols = y.shape[1]
    
    largestDim = max(max(x.shape), max(y.shape))
        
    if (largestDim & (largestDim - 1)) != 0:        #detects if largestDim is not a power of 2
        largestDim = nextPowerOfTwo(largestDim)     #sets largestDim to the next highest power of 2; helper function implemented at end of script
    
    #Pad matrices with zeros until their dimensions are largestDim x largestDim
    if x.shape[0] != largestDim:
        x = np.vstack((x, np.zeros((largestDim - x.shape[0], x.shape[1]),dtype=np.int)))
    if x.shape[1] != largestDim:
        x = np.hstack((x, np.zeros((x.shape[0], largestDim - x.shape[1]),dtype=np.int)))
    if y.shape[0] != largestDim:
        y = np.vstack((y, np.zeros((largestDim - y.shape[0], y.shape[1]),dtype=np.int)))
    if y.shape[1] != largestDim:
        y = np.hstack((y, np.zeros((y.shape[0], largestDim - y.shape[1]),dtype=np.int)))
    
    def strassen(x, y):
        '''
        Internal routine containing the implementation of Strassen's algorithm.
        
        Input:  Two equidimensional square matrices with dimensions that are 
        powers of two.
        Output: The product of the two matrices as a numpy matrix.
          
        The wrapper function, strassenMatMul, takes care of appropriately 
        preprocessing the input matrices and processing this function's output.
        '''
        
        dimensions = x.shape     #matrices will have same dimensions; only need to check one
        
        if dimensions == (1, 1): 
            return x*y
        
        nrows = dimensions[0]
        ncols = dimensions[1]
        
        a = x[:nrows/2, :ncols/2]
        b = x[:nrows/2, ncols/2:]
        c = x[nrows/2:, :ncols/2]
        d = x[nrows/2:, ncols/2:]
        e = y[:nrows/2, :ncols/2]
        f = y[:nrows/2, ncols/2:]
        g = y[nrows/2:, :ncols/2]
        h = y[nrows/2:, ncols/2:]
        
        p1 = strassen(a, f-h)
        p2 = strassen(a+b, h)
        p3 = strassen(c+d, e)
        p4 = strassen(d, g-e)
        p5 = strassen(a+d, e+h)
        p6 = strassen(b-d, g+h)
        p7 = strassen(a-c, e+f)
        
        left = np.vstack((p5+p4-p2+p6, p3+p4))   #row binding left half of product matrix
        right = np.vstack((p1+p2, p1+p5-p3-p7))  #row binding right half of product matrix
        
        return np.hstack((left, right))         #column binding the two halves into final result and returning it
       
    return strassen(x, y)[:resultNRows, :resultNCols].tolist()  #using the inner dimensions of original input matrices to subset out zero-padding
    
    
def nextPowerOfTwo(n):
    '''
    Finds the next highest power of 2 of an up to 64-bit integer by copying 
    the highest set bit to all of the lower bits and the adding one.  It can be
    modified to support higher-bit numbers by extending the number of 
    right-shifts indefinitely. The initial decrement is to ensure that it works 
    for numbers that are already powers of 2.
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