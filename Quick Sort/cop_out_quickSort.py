# Michael D. Salerno

def cop_out_quickSort(A):
    '''
    Another Quick Sort implementation of mine.  This version is a cop out in the
    sense that it does not take advantage of the in-place sorting that Quick
    Sort is capable of.  While this makes the algorithm much easier to
    implement, it greatly reduces its practical value, as it will use much more
    memory than an in-place Quick Sort does.  I provide it here for 
    demonstrative purposes.
    
    For more details and analysis of the Quick Sort algorithm, see my 
    documentation for quickSort.py.
    '''
    
    import random
    
    if len(A) == 0:
        return A
    
    p = random.choice(range(len(A)))     #randomized selection of pivot index
    
    ALeft = []                           #initialize ALeft which will contain the <p partition
    ARight = []                          #initialize ARight which will contain the >p partition
    switchFlag = False
    for j in range(1, len(A)):           #iterate through the array
        if j == p:                       #skip comparing the pivot to itself
            continue
        if A[j] == A[p]:                 #this if block properly distributes duplicate pivot values between ALeft and ARight
            if not switchFlag:
                ARight.append(A[j])
                switchFlag = True
            else:
                ALeft.append(A[j])
                switchFlag = False
        elif A[j] < A[p]:                  
            ALeft.append(A[j])
        else:
            ARight.append(A[j])
            
    
    lhs = cop_out_quickSort(ALeft)       #recurse on copies of the <p and >p partitions; sort and return them recursively
    rhs = cop_out_quickSort(ARight)             

    return lhs + [A[p]] + rhs            #prepend and append the sorted <p and >p partitions, respectively, to the pivot