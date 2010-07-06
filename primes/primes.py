#!/usr/bin/python
# primes up to 10000

r,e,a = range,enumerate,all
for i,x in e(i for i in r(4,10**4) if a(i%j!=0 for j in r(3,i))):
    print x
