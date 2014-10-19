# Michael D. Salerno

def rSelect(A, k):
    '''
    My implementation of an O(n) randomized in-place selection algorithm.
    
    Input:  A list of comparable elements, A, and the order of the element to
    be selected, k.
    Output:  The kth order statistic (the kth smallest element in A).
    
    The randomized selection algorithm uses the same partitioning procedure
    as Quick Sort (see my documentation for quickSort.py) and adapts its usage
    to the selection problem.  
        
    Procedure Overview:
        0.  If the length of the array is 1, return its element
        1.  Choose a pivot from A uniformly at random
        2.  Partition A around the pivot.  Let i = new index of the pivot
        3.  If i == k, return the pivot
        4.  If i > k, return a recursion on the left side of the array
        5.  If i < k, return a recursion on the right side of the array
    
    A key difference between this algorithm and Quick Sort is that there it uses 
    only one recursive call at each level.
    
    This implementation uses minimal memory by performing in-place searching; 
    thus, the recursive calls must be passed the original array as a parameter 
    along with pointers to the boundaries of the portion of the array that they 
    are recursively searching.     
    
    Randomized Selection Theorem:  
    For every input array of length n, the average running time of the 
    Randomized Selection algorithm is O(n).
    -Holds for every input (no assumptions on the data)
    -"Average" is over random pivot choices made by the algorithm
    
    Analysis:
    
    Note: Randomized Selection (rSelect) uses <= c*n operations outside if the 
    recursive call, for some constant c > 0 (in other words, O(n))
    
    Tracking Progress via Phases:
        
    Notation:  rSelect is in phase j if the size of the current array being 
    searched is between ((3/4)^(j+1))*n and ((3/4)^j)*n
    - Higher numbers of j indicate more progress has been made
    - The phase number j quantifies the number of times 75% progress has been 
    made relative to the original input array
    - Xj = number of recursive calls during phase j <--random variable, depends 
    on random pivot choices
    
    Note:  Running time of rSelect <= SIGMA(phases of j) Xj*c*((3/4)^j)*n
    - Xj is the number of phase-j subproblems
    - ((3/4)^j)*n is an upper bound on the array size during phase j
    - c*((3/4)^j)*n is the amount of work per phase-j subproblem
    
    Note:  If rSelect chooses a pivot give a 25-75 split or better, then the
    current phase ends (the subarray sent into the recursion will have a length
    that is at most 75% of the old length.)
    
    The probability of a 25-75 split or better is 50%, thus
    E[Xj] <= expected number of times a trial with probability of success 0.5
    must be repeated before the first success occurs (success = good pivot,
    failure = bad pivot)
    
    Let N = number of such trials until the first success (a geometric random
    variable with parameter p = 0.5).  By definition, E[N] = 1/p = 2.  Below
    is another proof.
    
    Note:  E[N] = 1 + (1/2)*E[N] = (1st trial) + P[failure]*(#further trials 
    needed in this case)
    Thus, E[N] = 2
    
    Recall:  E[Xj <= E[N]
    
    Expected running time of rSelect <= E[c*n*SIGMA(phases of j) ((3/4)^j)*Xj]
    = c*n*SIGMA(phases of j) ((3/4)^j)*E[Xj]  <- linearity of expectation
    <= 2*c*n*SIGMA(phases of j) ((3/4)^j) <- geometric sum, <= 1/(1-(3/4)) = 4
    <= 8*c*n = O(n)
    
    QED!
    
    '''
    
    assert 1 <= k <= len(A)  #Ensure that k makes sense for an array of length len(A)
    
    def randomizedSelection(A, left, right, k):
        '''
        Internal routine containing the implementation of the Randomized 
        Selection algorithm.  
        
        Input: A list, A, indices, left and right,  indicating the 
        boundaries of the partition to be processed, and the order of the 
        element being searched for, k.
        Output:  The kth order statistic.
        
        The wrapper function, quickSort, calls this function with the 
        appropriate initialization parameters.  rSelect(A, k) passes k-1 as the
        fourth parameter to this internal routine in order to offset for 
        Python's 0-based indexing.  If 0-based indexing is desired for the
        results rSelect (so there would be a 0th order statistic and the highest
        order statistic would be the (len(A) - 1)th), simply pass k as the 
        fourth initialization parameter instead of k-1 and change the wrapper
        function's assertion to reflect the change in indexing.
        '''
        
        import random
        
        if left == right:
            return A[0]
            
        p = random.choice(range(left, right))    #randomized selection of pivot index
        
        A[left], A[p] = A[p], A[left]            #swap the pivot into the first position
        
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

        if i == k:                             #check if the pivot is the kth order statistic
            return A[i]
                                              
        elif i > k:                           #if the pivot is greater than the kth order element, recurse on the left side of the array itself 
            return randomizedSelection(A, left, i, k)
        else:                                 #if the pivot is smaller than the kth order element, recurse on the right side of the array itself
            return randomizedSelection(A, i+1, right, k)
            
            
    return randomizedSelection(A[:], 0, len(A), k-1)   #k-1 is passed here in order to offset to 1-based indexing from Python's native 0-based indexing
                                                       #a copy of A is passed in order to prevent the original list from being modified 