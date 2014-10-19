# Michael D. Salerno

def quickSort(A):
    '''
    My implementation of the Quick Sort algorithm with randomized pivot
    selection and in-place sorting.
    
    Input:  A list of comparable elements
    Output: The list in sorted order
    Note:  It is not necessary to return the sorted list in this implementation
    because the list is sorted in place.  It is returned here for ease of 
    testing.
    
    The Quick Sort algorithm sorts an array of elements, A, by partitioning them
    around a selected pivot such that all elements to the left of the pivot are
    less than the pivot (<p partition) and all elements to the right of the
    pivot are greater than the pivot (>p partition).  The two partitions are
    then sorted recursively.
    
    The choice of pivot is made uniformly at random.  Correct partitioning 
    around the pivot can be achieved in O(n) time by using the following 
    approach:
    
        The pivot is moved into the first position of A by swapping it with the 
        element at the first position.  During partitioning, A can be thought of 
        as having four parts, from left to right; the pivot, elements that are 
        less than the pivot (<p), the elements that are greater than the pivot 
        (>p), and yet unexamined elements.  A pointer, j, iterates through A 
        in order to compare each element to the pivot; it points at the next 
        unexamined element.  A pointer, i, maintains the division between the 
        <p and >p partitions.  At each iteration, if A[j] is less than the pivot 
        (A[0]), it is swapped with the element at the left most position of the 
        >p partition, A[i].  Once j is done iterating, the pivot is swapped with 
        the right-most element of the <p partition (A[i] at the end of 
        partitioning).  This is the pivot's correct sorted position in A.
        
    Once the array is properly partitioned, the <p and >p partitions are 
    sent into recursive calls to Quick Sort.  This implementation uses minimal
    memory by sorting in-place; thus, the recursive calls do not need to return
    anything, however, they must be passed the original array as a parameter
    along with pointers to the boundaries of the portion of the array that they
    are recursively sorting.
    
    Quicksort Theorem:
    For every input array of length n, the average running time of Quck Sort
    (with uniformly random pivots) is O(nlog(n)). 
    -Holds for every input (no assumptions on the data)
    -"Average" is over random pivot choices made by the algorithm
    
    Intution:
    Always getting pivots which produce a 25-75 split or better is good enough
    to produce an O(nlog(n)) running time.  This can be proven via recursion
    tree.
    
    Analysis:
        
    Proof of the Quick Sort Theorem:
        
        Fix an input of array A of length n.  
        
        Let O = the sample space of all possible outcomes of random pivot 
        sequences in Quick Sort.
         
        For s in O, let C(s) = the number of comparisons between two input
        elements made by Quick Sort, given s.
        
        Lemma:  The running time of Quick Sort is dominated by comparisons.
        
        Therefore, proving that E[C] = O(nlog(n)) will also prove the Quick 
        Sort Theorem.  The Master Method can't be applied because of random 
        and unbalanced subproblems.  A decomposition approach will be used
        instead.
        
        Let zi = ith smallest element of A.  
        
        For s in O, indices i < j, let Xij(s) = the number of times zi, zj get
        compared in Quick Sort with pivot sequence s.
        
        Two elements of the input array can be compare at most 1 time because 
        two elements are compared only when one is the pivot, which is excluded 
        recursive calls.  If an element with a value in between the values of
        the two elements is chosen as the pivot, then those two values will 
        never be compared because they are sent into separate recursions of
        Quick Sort.  Thus, Xij is an indicator random variable 
        (takes on value 0 or 1).
        
        Then, for all s, C(s) = SIGMA(i to n-1)SIGMA(j=i+1 to n) Xij(s) 
        
        Thus, by linearity of expectation, 
        E[C] = SIGMA(i to n-1)SIGMA(j=i+1 to n) E[Xij]  <-Much simpler than E[C]
        
        E[Xij] = 0*P[Xij = 0] + 1*P[Xij = 1] = P[Xij = 1]
        
        Thus, E[C] = SIGMA(i to n-1)SIGMA(j=i+1 to n) P[zi, zj get compared]
        
        Fix zi, zj with i < j.  Consider the set zi, zi+1, ..., zj-1, zj.
        
        Inductively:  As long as none of these are chosen as the pivot, all are 
        passed to the same recursive call.  Consider the first among zi,..., zj
        that gets chosen as a pivot.  If zi or zj gets chosen first, then zi and
        zj get compared.  If one of the zi+1,..., zj-1 gets chosen first, then 
        zi and zj are never compared as they are split into difference recursive
        calls. 
        
        Thus, P[zi, zj get compared] = 2/(j - i + 1); in words, 2 divided by
        the number of (equally likely) pivot choices in the sequence.
        
        So, E[C] = SIGMA(i to n-1)SIGMA(j=i+1 to n) 2/(j - i + 1)
        
        E[C] = 2*SIGMA(i to n-1)SIGMA(j=i+1 to n) 1/(j - i + 1)
        
        For each fixed i, the inner sum is -
        SIGMA(j=i+1 to n) 1/(j - i + 1) = 1/2 + 1/3 + 1/4 + ...
        and there are O(n) choices for i.
        
        So, E[C] <= 2 * n * SIGMA(k=2 to n) 1/k
        
        SIGMA(k=2 to n) 1/k is upper bounded by the function 1/x  *see notes
        
        thus, SIGMA(k=2 to n) 1/k <= integral(1 to n) 1/x * dx = lnx | 1 to n
        = ln(n) - ln(1) = ln(n)
        
        thus, E[C] <= 2*n*ln(n)  (base of log does not matter; logs of different
        bases differ only by a constant factor)
        
        QED!
        
    '''
    
    def qSort(A, left, right):
        '''
        Internal routine containing the implementation of Quick Sort.  
        
        Input:  A list, A, and indices, left and right,  indicating the 
        boundaries of the partition to be processed.
        Output: The list in sorted order.
        
        The wrapper function, quickSort, calls this function with the 
        appropriate initialization parameters.
        '''
        
        import random
        
        if left == right:
            return A
        
        p = random.choice(range(left, right))    #randomized selection of pivot index

        A[left], A[p] = A[p], A[left]           #swap the pivot into the first position

        switchFlag = False                      ##flag to be used to handle duplicate pivot values
        i = left                                #initialize pointer to shadow the division between the <p and >p partitions
        for j in range(left+1, right):         #j is a pointer to the next unexamined element; it separates the <p and >p partitions from the unexamined partition
            if A[j] == A[left]:                ##check if the next unexamined value is equal to the pivot; of this happens more than once, there are some number of duplicate pivot values
                if not switchFlag:
                    switchFlag = True          ##alternating switchFlag ensures that duplicate pivot values are split evenly
                else:
                    i += 1
                    if i != j:
                        A[i], A[j] = A[j], A[i]
                    switchFlag = False
                    
            elif A[j] < A[left]:
                i += 1                          #increment i so that it points at the left-most element of the >p partition
                if i != j:                      #this check avoids redundant swaps which would occur if an element greater than the pivot hasn't been found yet
                    A[i], A[j] = A[j], A[i]     #after this swap, i points at the right-most element of the <p partition that was just swapped in
   
        A[left], A[i] = A[i], A[left]           #swap the pivot with the right-most element of the <p partition; this will also be its correct position in the final sorted list

        qSort(A, left, i)                      #recurse on the array itself; uses pointers to the <p and >p partitions to sort in place so no return is necessary
        qSort(A, i+1, right)                   #avoid including the pivot in the recursion

        return A                              #return the sorted array
        
    return qSort(A, 0, len(A))