#!/usr/bin/python

import sys, time
from random import randint
from math import sqrt, ceil, floor, log

MAX = 20000000

def sieveOfErat(upperBound):
    """ http://krenzel.info/static/atkin.py """

    if upperBound < 2:
        return []

    # Don't include even numbers
    lng = ((upperBound/2) - 1 + upperBound % 2)
    sieve = [ True ] * (lng + 1)

    # Only go up to square root of the upperBound
    for i in range(int(sqrt(upperBound)) >> 1):
            
        if not sieve[i]:
            continue

        # increment by twice the multiple: no even numbers
        for j in range( (i*(i + 3) << 1) + 3, lng, (i << 1) + 3 ):
            sieve[j] = False
            
    # Don't forget 2!
    primes = [ 2 ]
    # Gather all the primes into a list
    primes.extend([(i << 1) + 3 for i in range(lng) if sieve[i]])

    return primes


def output(primes):
    for p in primes:
        print p

# ---------------------------------------------------------------------------- #

timer = time.time

start = timer()
primes = sieveOfErat(MAX)
end = timer()

# Don't include I/O for printing 20 million numbers in test
output(primes)

runtime = end - start
print >> sys.stderr, "Running time: %.2f s" % (runtime)
