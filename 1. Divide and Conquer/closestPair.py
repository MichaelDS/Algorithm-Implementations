# Michael D. Salerno

def closestPair(points):
    '''
    My implementation of an O(nlog(n)) algorithm for finding the pair of points
    that are closest to each other among a set of points.  Euclidean distance
    was used in this implementation.
    
    Notation: d(pi, pj) = Euclidean distance between pi and pj.
    
    Input:  A list of tuples that represent the x and y coordinates of a set of 
    n points in R^2.  P = [(x1, y2), (x2, y2), (x3, y3),.....,(xn, yn)]
    Output: A tuple of the two tuples that represent the the pair of distinct 
    points p, q in P that minimize d(p, q) over all p, q in P.
          
    The naive approach takes O(n^2) time.  This is also true of the analogous
    1-D version of the problem of finding the closest pair on a line.  The 1-D 
    version of the problem can be solved in O(nlog(n)) time by first sorting
    the points based on their position on the line (O(nlog(n))), and then 
    scanning the sorted list and returning the closest pair of adjacent points
    O(n).  An O(nlog(n)) solution to the 2-D version involving points on the 
    plane is obtained with the following approach:
    
    1. Make a list of the points sorted by x-coordinate, px, and by 
       y-coordinate, py.  (O(nlog(n)) time.
    2. Use divide + conquer:  findClosestPair(px,py)        
        1. Let q = left half of P, R = right half of P.  Form sorted lists of
           the points in these halves, both, by x-coordinate and y-coordinate;
           qx, qy, rx, ry.  This takes O(n) time by taking advantage of the 
           original sorted lists, px and py.  (qx and rx are already sorted; 
           takes O(n) for qy and ry)
        2. Recursively compute the closest pair in the left half of P;
           (p1, q1) = findClosestPair(qx, qy)
        3. Recursively compute the closest pair in the right half of P;
           (p2, q2) = findClosestPair(rx, ry)
        4. Let d = min{ d(p1, q1), d(p2, q2) }
        5. Compute the closest split pair (whenever the closest pair of P is a
           split pair) in O(n) time;
           (p3, q3) = closestSplitPair(px, py, d)
        6. Return the minimum of (p1, q1), (p2, q2), (p3, q3)
    
    A split pair is defined as a pair of points such that one lies in the left 
    half of P and the other in the right half.  In order to find the closest
    split pair, given that there exists a split pair less than d apart, first 
    partition P into its left and right halfs by defining midx = largest 
    x-coordinate in the left of P (in q).  (O(1) time)
    Next, let sy = points of P with x-coordinate in [midx - d, midx + d],
    sorted by y-coordinate.  (O(n) time by taking advantage of py)
    Lastly, iterate through sy and for each point compute its Euclidean 
    distance to the 7 subsequent points in sy, or to the last point in sy, 
    whichever is less.  If any of these distances is less than the current 
    minimum distance (d at the start), then store it as the new minimum.  
    (O(n) time)
    
    If no eligible split pair was identified, then d(p3, q3) = infinity.
    The closest pair is min{ d(p1, q1), d(p2, q2), d(p3, q3) }.
    
    Correctness Claim:  Let p = (x1, y1) and q = x2, y2) 
    be in the left and right half of P, respectively and let them be a split 
    pair with d(p, q) < d.  Then,
    A.  p and q are members of sy
    B.  p and q are at most 7 positions apart in sy
    
    Corollary 1:  If the closest pair of P is a split pair, then 
    closestSplitPair finds it.
    Corollary 2:  Closest pair is correct and runs in O(nlog(n)) time.
    
    *See notes for proofs of correctness claims.  Essentially, claim A is true
    because their distance is bound by d; thus, as a split pair, the farthest
    that either can be from the center(midx) sy is d.  Claim B can be shown to 
    be true by proving that given 8 d/2 x d/2 boxes centered at midx and with 
    bottom at min{y1, y2}, all points of sy with y-coordinate between those of 
    p and q, inclusive, lie in one of the 8 boxes and there is at most one point 
    in each box because two points in one box would imply a non-split pair with 
    distance less than d, which contradicts the definition of d.
    
    This algorithm's asymptotic time complexity can be verified using the 
    Master Method.  Its recurrences can be expressed as T(n) = 2*T(n/2) + O(n);
    thus, the running time is O(nlog(n))
    '''
    
    from operator import itemgetter
    
    px = sorted(points, key = itemgetter(0))
    py = sorted(points, key = itemgetter(1))
    
    def findClosestPair(px, py):
        
        if len(px) == 2:
            return px
        elif len(px) == 3:
            return min((px[0], px[1]), (px[0], px[2]),(px[1], px[2]), key = euclideanDist)
        
        q = px[:len(px)/2]  #left half of points
        r = px[len(px)/2:]  #right half of points
        
        print q, r
        print px
        
        qx = q
        rx = r
        qy = []
        ry = []
        switchFlag = False   #must be initialized to false in order to ensure a proper split in the case and q and r do not split any x values; see next two comments for context
        
        for p in py:
            if p[0] == q[-1][0]:       #check if p's x value is equal to q's greatest x value; if this happens more than once, it indicates that q and r split some number of points with duplicate x values
                if not switchFlag:   
                    qy.append(p)
                    switchFlag = True  #alternating switchFlag each time such a point is detected ensures that these points are also appropriately split between qy and ry
                else:
                    ry.append(p)
                    switchFlag = False
            elif p[0] < q[-1][0]:  #check if p's x value falls within the range of q
                qy.append(p)
            else:
                ry.append(p)
                
        print qy, ry
        closestLeftPair = findClosestPair(qx, qy)
        closestRightPair = findClosestPair(rx, ry)
        
        d = min(euclideanDist(closestLeftPair), euclideanDist(closestRightPair))  #helper function implemented at end of script
        midx = q[-1][0]
        sy = []
        
        for p in py:
            if midx - d < p[0] < midx + d:  #checks if the point's x-coordinate is within boundary
                sy.append(p)
        
        shortestDist = d
        closerSplitPair = None      #Will only be found if there exist split pairs closer than d; euclideanDist has been implemented to define the distance between non-existant points as infinite
        
        for i in range(len(sy) - 1):                 #No elements follow the last element, so exclude it from the loop
            for j in range(1, min(7, len(sy) - i)):  #Check the subsequent 7 points or the remaining points if less than 7
                     pair = (sy[i], sy[i+j])
                     dist = euclideanDist(pair)
                     if dist < shortestDist:
                            closerSplitPair = pair
                            shortestDist = dist
        
        return min(closestLeftPair, closestRightPair, closerSplitPair, key = euclideanDist)
        
    return findClosestPair(px, py)

def euclideanDist(pair):
    '''
    Input:  A list containing two points
    Output: Their Euclidean distance
    '''
    from math import sqrt
    
    if pair == None:
        return float('inf')
    
    return sqrt((pair[0][0] - pair[1][0])**2 + (pair[0][1] - pair[1][1])**2)