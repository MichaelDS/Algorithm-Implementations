# Michael D. Salerno

def karatsubaMul(x, y):
    '''
    My implementation of Karatsuba Multiplication; a subquadratic algorithm for
    multiplying two n-digit numbers.  Its recurrences can be expressed as
    T(n) = 3*T(n/2) + O(n); thus, by the Master Theorem, it's asymptotic time 
    complexity is O(n^log2(3)) = (n^1.585).
    
    Takes advantage of the fact that 
    x*y = (a * 10^(n/2) + b) * (c * 10^(n/2) + d), where a and b partition
    x into it's left half digits and right half digits, respectively, and c and 
    d do the same for y.  Thus, x*y = a*c*10^n + (a*d + b*c)*10^(n/2) + b*d.
    
    a*d + b*c is acquired in a single multiplication using a trick attributed to 
    Carl Gauss;
    
    (a+b)*(c+d) = a*c + a*d + b*c + b*d
    Thus, a*d + b*c = (a+b)*(c+d) - a*c - b*d
    '''
    
    if min(x,y) < 10:
        return x * y
    
    deg = len(str(max(x, y)))
    halfDeg = deg//2 + (deg & 1)
    
    a = int(x * 10**-halfDeg) 
    b = int(x % 10**halfDeg)
    c = int(y * 10**-halfDeg)
    d = int(y % 10**halfDeg)

    ac = karatsubaMul(a, c)
    bd = karatsubaMul(b, d)
    gaussTrick = karatsubaMul(a+b, c+d) - ac - bd
    return ac * 10**(2*halfDeg) + gaussTrick * 10**halfDeg + bd