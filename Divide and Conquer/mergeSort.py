# Michael D. Salerno

def mergeSort(arr):
    '''
    My implementation of Merge Sort.
    
    Input:  A list of comparable elements
    Output: The list of the elements in sorted order
    
    Merge Sort splits the input array in half and sends each subarray into a 
    recursive call.  The results of these two recursive calls, by virtue of 
    being sorted, can then merged into a complete sorted array by simultaneously 
    iterating through each of them and, at each iteration, removing the smaller 
    of their first elements and appending that element to the result.
    
    At each recursion level, j, there are 2^j subproblems each of size n/(2^j); 
    this counterbalancing produces a size n problem at each level of recursion.  
    There are log2(n) levels of recursion; thus, the Merge Sort algorithm has an 
    asymptotic time complexity of O(n*logn).  This can be verified by applying
    the Master Theorem to the recurrence T(n) = 2*T(n/2) + O(n).
    '''
      
    if len(arr) <= 1:
        return arr
    
    lhs = mergeSort(arr[:len(arr)/2])        #recursively sort the two halves of the input 
    rhs = mergeSort(arr[len(arr)/2:])
    
    result = []
    
    while len(lhs) != 0 and len(rhs) != 0:  #Merge step
        if lhs[0] <= rhs[0]:
            result.append(lhs.pop(0))
        else:
            result.append(rhs.pop(0))
            
    if len(lhs) == 0:     #once one of the lists is exhausted, simply append the remaining list to the result
        result += rhs
    else:
        result += lhs
        
    return result
        