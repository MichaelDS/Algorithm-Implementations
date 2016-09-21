from random import randint

def square(x):
    return x*x

## Computes the exponential of a number modulo another number
def expmod(base, exp, m):
    if exp == 0:
        return 1
    if exp % 2 == 0:
        return square(expmod(base, exp/2, m)) % m
    else:
        return (base * expmod(base, exp-1, m)) % m

## Performs a single Fermat test; a probabilistic method used to increase our
## confidence that a given number is prime.  The Fermat test is based on
## Fermat's Little Theorem, which states that if "n" is a prime number and "a" is
## any positive integer less than "n", then "a" raised to the  "n"th power is
## congruent to "a" modulo "n".
def fermat_test(n):
    def try_it(a):
        return expmod(a, n, n) == a
    return try_it(randint(1, n-1))

## Determines whether or not a number is prime to arbitrarily high confidence
## by performing a specified number of Fermat tests.
def fast_prime_test(n, times):
    if times == 0:
        return True
    elif fermat_test(n):
        return fast_prime_test(n, times-1)
    else:
        return False

## checks the primality of consecutive odd numbers
def search_for_primes(start, times = 100):
    if start < 2:
        yield from search_for_primes(2, times)
    elif start % 2 == 0:
        if start == 2:
            yield start
        yield from search_for_primes(start+1, times)
    elif fast_prime_test(start, times):
        yield start
    yield from search_for_primes(start+2, times)
