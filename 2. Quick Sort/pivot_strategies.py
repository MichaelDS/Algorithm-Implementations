# Michael D. Salerno

def quickSort_first_element(A):

    def qSort(A, left, right):

        import random

        if left == right:
            return 0

        p = left    #always chooses the first element as the pivot

        A[left], A[p] = A[p], A[left]

        switchFlag = False                      ##flag to be used to handle duplicate pivot values
        i = left                                #initialize pointer to shadow the division between the <p and >p partitions
        for j in range(left+1, right):         #j is a pointer to the next unexamined element; it separates the <p and >p partitions from the unexamined partition
            if A[j] == A[left]:                ##check if the next unexamined value is equal to the pivot; if this happens more than once, there are some number of duplicate pivot values
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

        #recurse on the array itself; uses pointers to the <p and >p partitions to sort in place
        #recursively aggregate the number of comparisons being made
        return (right - left - 1) + qSort(A, left, i) + qSort(A, i+1, right)

    return qSort(A, 0, len(A))                        #call to qSort with initial boundary pointers; sorts the list in place

def quickSort_last_element(A):

    def qSort(A, left, right):

        import random

        if left == right:
            return 0

        p = right - 1                           # always chooses the last element as the pivot

        A[left], A[p] = A[p], A[left]           #swap the pivot into the first position

        switchFlag = False                      ##flag to be used to handle duplicate pivot values
        i = left                                #initialize pointer to shadow the division between the <p and >p partitions
        for j in range(left+1, right):         #j is a pointer to the next unexamined element; it separates the <p and >p partitions from the unexamined partition
            if A[j] == A[left]:                ##check if the next unexamined value is equal to the pivot; if this happens more than once, there are some number of duplicate pivot values
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

        #recurse on the array itself; uses pointers to the <p and >p partitions to sort in place
        #recursively aggregate the number of comparisons being made
        return (right - left - 1) + qSort(A, left, i) + qSort(A, i+1, right)

    return qSort(A, 0, len(A))                        #call to qSort with initial boundary pointers; sorts the list in place

def quickSort_median_of_three(A):

    def qSort(A, left, right):

        import random, math

        if left == right:
            return 0

        #compute the middle index for this array
        length = right - left
        if length % 2 == 0:
            mid = left + int(length/2 - 1)               #result is an integer, but python coerces to float.  Need int for indexing.
        else:
            mid = math.floor(left + length/2)

        #point the pivot to the "median of three"
        if A[left] <= A[mid] <= A[right-1] or A[left] >= A[mid] >= A[right-1]:
            p = mid
        elif A[mid] <= A[left] <= A[right-1] or A[mid] >= A[left] >= A[right-1]:
            p = left
        else:
            p = right-1

        A[left], A[p] = A[p], A[left]           #swap the pivot into the first position

        switchFlag = False                      ##flag to be used to handle duplicate pivot values
        i = left                                #initialize pointer to shadow the division between the <p and >p partitions
        for j in range(left+1, right):         #j is a pointer to the next unexamined element; it separates the <p and >p partitions from the unexamined partition
            if A[j] == A[left]:                ##check if the next unexamined value is equal to the pivot; if this happens more than once, there are some number of duplicate pivot values
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

        #recurse on the array itself; uses pointers to the <p and >p partitions to sort in place
        #recursively aggregate the number of comparisons being made
        return (right - left - 1) + qSort(A, left, i) + qSort(A, i+1, right)

    return qSort(A, 0, len(A))                        #call to qSort with initial boundary pointers; sorts the list in place
