# Michael D. Salerno

def dSelect(A, k):
    '''
    My implementation of an O(n) deterministic selection algorithm.
    
    Input:  A list of comparable elements, A, and the order of the element to
    be selected, k.
    Output:  The kth order statistic (the kth smallest element in A).
    
    The deterministic selection algorithm is very similar to the randomized
    selection algorithm (see my documentation for rSelect.py).  The key 
    differences are the manner in which the pivot is chosen (using the median of
    medians method) and the fact that the algorithm is no longer performed 
    in-place, since it requires creating copies of portions of the input array.  
    For the sake of demonstration, the parameters to the recursion in this 
    implementation do not make use of pointers to the boundaries of the portion 
    of the array being recursively searched; instead, the parameters consist of  
    an array, its size, and the order of the element being searched for.
    
    Procedure Overview:
        0.  If the length of the array is 1, return its element
        1.  Logically break A into n/5 groups of size 5 each (plus remainders)
        2.  Sort each group (e.g., using Merge Sort)
        3.  Copy n/5 medians (i.e., middle element of each sorted group) into
            new array C
        4.  Recursively compute the median of C and return this as the pivot
        5.  Partition A around the pivot.  (Let i = final index of the pivot)
        6.  If i > k, return a recursion on the left side of the array
        7.  If i < k, return a recursion on the right side of the array
        
    Another key difference between rSelect and dSelect is that the dSelect
    algorithm uses 2 recursive calls instead of 1.
    
    dSelect Theorem:
    For every input array of length n, dSelect runs in O(n) time.
    
    Warning:
    Although dSelect deterministically guarantees an O(n) running time, it is
    not as good as rSelect in practice. This is because it has larger hidden
    constants and it does not perform the selection in place.
    
    Analysis:
        
    Breakdown of the running times of each step of the algorithm as enumerated
    in the Procedure Overview above:
        0. O(1)
        1. O(n)
        2. O(n) - Sorting an array with 5 elements has an O(1) time complexity.
        This step sorts approximately n/5 such arrays.
        3. O(n)
        4. T(n/5)
        5. O(n)
        6./7. T(7n/10) - See proof of following lemma
        
    Key Lemma:  The second recursive call (in step 6 or 7) is guaranteed to be
    on an array of rough size <= 7*n/10
    
    Rough Proof:
        - Let k = n/5 = # of groups
        - Let xi = ith smallest of the k "middle elements" (so pivot = xi, 
        where i = k/2)
        
        Because x(k/2) is the median of medians, it is larger than about 50%
        of the other middle elements.  Transitively, the subgroups that these 
        lesser middle elements belong to also contain 2 additional elements that
        are guaranteed to be less than x(k/2).  So x(k/2) is greater than 3 out
        of 5 (60%) of the elements in roughly 50% of the subgroups; thus, x(k/2)
        is guaranteed to be greater than at least 30% of all of the elements
        across the subgroups.  
        
        Similarly, x(k/2) is smaller than about 50% of the other middle 
        elements and a symmetric argument shows that x(k/2) is guaranteed to be
        less than at least 30% of the elements across all of the subgrous.
        
        Therefore, the upper bound on the size of the array being passed to the
        second recursive call is 7/10ths of the original array size, or 7*n/10.
        
    So, T(1) = 1 and
    T(n) <= c*n + T(n/5) + T(7*n/10), where c is a constant >= 1
    
    Strategy:  Guess and check
    
    Guess:  There is some constant a (independent of n) such that T(n) <= a*n
    for all n >= 1.  (If this is true, the T(n) = O(n) and the algorithm is 
    linear-time.
    
    Claim:  Let a = 10*c, then T(n) <= a*n for all n >= 1 
    (the 10 is reverse-engineered)
    
    Proof (by induction on n):
        
        Base case:  T(1) = 1 <= a*1  (since a >= 1)
        
        Inductive step: (n > 1)  Inductive Hypothesis: T(k) <= a*k for all k < n
        We have T(n) <= c*n + T(n/5) + T(7*n/10)  (given)
        <= c*n + a*(n/5) + a*(7*n/10)             (inductive hypothesis)
        = n*(c + 9*a/10) = a*n = O(n)             (choice of a)
        
        QED!
    '''
    
    assert 1 <= k <= len(A)  #Ensure that k makes sense for an array of length len(A)
    
    def deterministicSelection(A, n, k):
        
        if n == 1:
            return A[0]
        
        groups = groupsOfFive(A)                #break A into groups of 5
        
        for i in range(len(groups)):
            groups[i] = mergeSort(groups[i])    #sort each of the groups (O(n))
        
        C = medians(groups)                     #find the medians of each group
        
        pivot = deterministicSelection(C, len(C), n/10)  #select the median of medians as the pivot; len(C) is either n/5 or n/5 + 1
        p = A.index(pivot)                      #save the pivot's index

        A[0], A[p] = A[p], A[0]                 #swap the pivot into the first position
        
        switchFlag = False                      ##flag to be used to handle duplicate pivot values
        i = 0                                   #initialize pointer to shadow the division between the <p and >p partitions
        for j in range(1, len(A)):             #j is a pointer to the next unexamined element; it separates the <p and >p partitions from the unexamined partition
            if A[j] == A[0]:                   ##check if the next unexamined value is equal to the pivot; of this happens more than once, there are some number of duplicate pivot values
                if not switchFlag:
                    switchFlag = True          ##alternating switchFlag ensures that duplicate pivot values are split evenly
                else:
                    i += 1
                    if i != j:
                        A[i], A[j] = A[j], A[i]
                    switchFlag = False
                    
            elif A[j] < A[0]:
                i += 1                          #increment i so that it points at the left-most element of the >p partition
                if i != j:                      #this check avoids redundant swaps which would occur if an element greater than the pivot hasn't been found yet
                    A[i], A[j] = A[j], A[i]     #after this swap, i points at the right-most element of the <p partition that was just swapped in

        A[0], A[i] = A[i], A[0]                 #swap the pivot with the right-most element of the <p partition; this will also be its correct position in the final sorted list
        
        if i == k:                            #check if the pivot is the kth order statistic
            return A[i]
        
        elif i > k:                           #if the pivot is greater than the kth order element, recurse on a copy of the left side of the array and adjust the size parameter
            return deterministicSelection(A[:i], i, k)
        else:                                 #if the pivot is smaller than the kth order element, recurse on a copy the right side of the array and adjust the size and order parameters
            return deterministicSelection(A[i+1:], n-(i+1), k-(i+1))
        
    return deterministicSelection(A[:], len(A), k-1)  #k-1 is passed here in order to offset to 1-based indexing from Python's native 0-based indexing
                                                      #a copy of A is passed in order to prevent the original list from being modified 
    
    
    
def groupsOfFive(A):
    '''
    Breaks a list of length n into into groups of 5 elements (n/5 subgroups) and 
    returns them in a list of lists.  The origninal elements are copied into 
    their respective subgroups.
    
    Input:  A list, A.
    Output: A list of lists containing the n/5 subgroups
    '''
    
    groups = []
    x = []
    for e in A:
        x.append(e)
        if len(x) == 5:
            groups.append(x)
            x = []
            
    if len(x) != 0:
        groups.append(x)
        
    return groups
    
def mergeSort(arr):
    '''
    My implementation of Merge Sort.  For analysis see my documentation of
    mergeSort.py.
    '''
      
    if len(arr) <= 1:
        return arr
    
    lhs = mergeSort(arr[:len(arr)/2])
    rhs = mergeSort(arr[len(arr)/2:])
    
    result = []
    
    while len(lhs) != 0 and len(rhs) != 0:
        if lhs[0] <= rhs[0]:
            result.append(lhs.pop(0))
        else:
            result.append(rhs.pop(0))
            
    if len(lhs) == 0:
        result += rhs
    else:
        result += lhs
        
    return result
    
def medians(groups):
    '''
    Computes the medians of the given subgroups and returns them in a list.
    
    Input:  A list of lists containing subgroups
    Output: A list of the subgroups' medians
    '''
    
    result = []
    for g in groups:
        if len(g) %2 == 0:
            result.append(g[len(g)/2 - 1])  #if the given array is even in length, identify the first of the two middle indices as the middle index
        else:
            result.append(g[len(g)/2])
            
    return result