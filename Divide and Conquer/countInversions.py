# Michael D. Salerno

def countInversions(arr):
    '''
    My implementation of an O(nlog(n) algorithm for counting inversions in an 
    array.  
    
    Input:  A list of comparable elements
    Output: The number of inversions in the list
    
    An inversion is defined as a pair of elements in an array A with indices
    (i, j) where i < j and A[i] > A[j].
    
    A divide an conquer algorithm is used to count the number of inversion in an 
    array A.  Partitioning A into its two halves, the inversions, (A[i], A[j]), 
    can be though of as falling into one of three categories:
    
    Left Inversion:  i, j <= n/2
    Right Inversion: i, j > n/2
    Split Inversion: i <= n/2 < j
    
    The number of left inversions and right inversions is acquired recursively. 
    In addition to counting inversions, the recursion also sorts A via merge
    sort; this is done so that the number of split inversions can be counted
    in O(n) time during the merge step.  The algorithm takes advantage of the 
    fact that, during the merge procedure, each time an element from the right 
    subarray is added to the merged array the number of inversions with elements
    of the left subarray that it is involved in  is equal to the number of 
    elements remaining to be merged from the left subarray.  There are log(n) 
    levels of recursion, each with a total problem size of n; this, this 
    algorithm's asymptotic time complexity is O(nlog(n)).  This can be verified 
    by applying the Master Theorem to the recurrence T(n) = 2*T(n/2) + O(n).
    
    The left, right, and split inversions are summed and the total is returned
    along with the merged(sorted) array.  
    '''
      
    def sortAndCount(arr):
        '''
        Internal routine containing the implementation.  It is called by the
        wrapper in order to ultimately extract and return only the inversion
        count.
        
        Input:  A list of comparable elements
        Output: A tuple containing the list after sorting and the number of
        inversions it originally contained.  (sortedList, count)
        '''
        
        if len(arr) == 1:
            return (arr, 0)
            
        (lhs, countLeft) = sortAndCount(arr[:len(arr)/2])
        (rhs, countRight) = sortAndCount(arr[len(arr)/2:])
        
        mergedArr = []
        countSplits = 0
        
        while len(lhs) != 0 and len(rhs) != 0:
            if lhs[0] <= rhs[0]:
                mergedArr.append(lhs.pop(0))
            else:
                mergedArr.append(rhs.pop(0))
                countSplits += len(lhs)
                
        total = countLeft + countRight + countSplits
                
        if len(lhs) == 0:
            mergedArr += rhs
        else:
            mergedArr += lhs
            
        return (mergedArr, total)
        
    return sortAndCount(arr)[1]