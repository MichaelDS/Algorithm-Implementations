# Michael D. Salerno

def example_quickSort(A):
    '''
    Another Quick Sort implementation of mine.  This one is mostly for 
    demonstrative purposes.  It uses the in-place partitioning algorithm 
    without handling the distribution of duplicate pivot values, so it's easier 
    to see the procedure, however, it does not use pointers to keep track of 
    which part of the array is being processed; thus, copies of the slices of 
    the array to the left and right of the pivot after partitioning are passed 
    to the recursive calls to Quick Sort.  If copies are going to be used, then 
    the cop out method in cop_out_quickSort.py may as well be used, as it is 
    even easier to implement.
    
    See my documentation for quickSort.py for more details and analysis on
    the Quick Sort algorithm.
    '''
    
    import random
    
    if len(A) == 0:
        return A
    
    p = random.choice(list(range(len(A))))     #randomized selection of pivot index

    A[0], A[p] = A[p], A[0]              #swap the pivot into the first position

    i = 0                                #initialize pointer to shadow the division between the <p and >p partitions
    for j in range(1, len(A)):           #j is a pointer to the next unexamined element; it separates the <p and >p partitions from the unexamined partition
        if A[j] < A[0]:
            i += 1                       #increment i so that it points at the left-most element of the >p partition
            if i != j:                   #this check avoids redundant swaps which would occur if an element greater than the pivot hasn't been found yet
                A[i], A[j] = A[j], A[i]  #after this swap, i points at the right-most element of the <p partition that was just swapped in
                
    A[0], A[i] = A[i], A[0]              #swap the pivot with the right-most element of the <p partition; this will also be its correct position in the final sorted list
    
    lhs = example_quickSort(A[:i])               #recurse on copies of the <p and >p partitions; sort and return them recursively
    rhs = example_quickSort(A[i+1:])             #avoid including the pivot in the recursion

    return lhs + [A[i]] + rhs           #prepend and append the sorted <p and >p partitions, respectively, to the pivot