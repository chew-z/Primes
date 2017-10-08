#!/usr/bin/env python3
# coding: utf-8
# various algos generating prime numbers < N
# https://stackoverflow.com/questions/2068372

import itertools
import numpy as np
import datetime
# from operator import mul
# from functools import reduce


def ambi_sieve(n):
    # DEAD link http://tommih.blogspot.com/2009/04/fast-prime-number-generator.html
    s = np.arange(3, n, 2)
    for m in range(3, int(n ** 0.5) + 1, 2):
        if s[(m - 3) // 2]:
            s[(m * m - 3) // 2::m] = 0
    return np.r_[2, s[s > 0]]


def rwh_primes(n):
    # https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    """ Returns  a list of primes < n """
    sieve = np.ones((n,))
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i]:
            sieve[i * i::2 * i] = np.asarray(0) * \
                ((n - i * i - 1) // (2 * i) + 1)
    return [2] + [i for i in range(3, n, 2) if sieve[i]]


def sundaram3(n):
    numbers = list(range(3, n + 1, 2))
    half = (n) // 2
    initial = 4
    for step in range(3, n + 1, 2):
        for i in range(initial, half, step):
            numbers[i - 1] = 0
        initial += 2 * (step + 1)

        if initial > half:
            return [2] + list(filter(None, numbers))


def rwh_primes2_python3(n):
    """ Input n>=6, Returns a list of primes, 2 <= p < n """
    zero = bytearray([False])
    izip = itertools.zip_longest
    chain = itertools.chain.from_iterable
    compress = itertools.compress

    size = n // 3 + (n % 6 == 2)
    sieve = bytearray([True]) * size
    sieve[0] = False
    for i in range(int(n**0.5) // 3 + 1):
        if sieve[i]:
            k = 3 * i + 1 | 1
            start = (k * k + 4 * k - 2 * k * (i & 1)) // 3
            sieve[(k * k) // 3::2 * k] = zero * \
                ((size - (k * k) // 3 - 1) // (2 * k) + 1)
            sieve[start::2 * k] = zero * ((size - start - 1) // (2 * k) + 1)
    ans = [2, 3]
    poss = chain(izip(*[range(i, n, 6) for i in (1, 5)]))
    ans.extend(compress(poss, sieve))
    return ans


def prime6(n):
    from math import sqrt
    primes = np.arange(3, n + 1, 2)
    isprime = np.ones((n - 1) // 2, dtype=bool)
    for factor in primes[:int(sqrt(n))]:
        if isprime[(factor - 2) // 2]:
            isprime[(factor * 3 - 2) // 2:(n - 1) // 2:factor] = 0
    return np.insert(primes[isprime], 0, 2)


def primes_simpy(n):
    from sympy import sieve
    return list(sieve.primerange(1, n))


def primesfrom2to(n):
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    sieve = np.ones(n // 3 + (n % 6 == 2), dtype=np.bool)
    for i in range(1, int(n**0.5) // 3 + 1):
        if sieve[i]:
            k = 3 * i + 1 | 1
            sieve[k * k // 3::2 * k] = False
            sieve[k * (k - 2 * (i & 1) + 4) // 3::2 * k] = False
    return np.r_[2, 3, ((3 * np.nonzero(sieve)[0][1:] + 1) | 1)]


def primesfrom3to(n):
    """ Returns a array of primes, 3 <= p < n """
    sieve = np.ones(n // 2, dtype=np.bool)
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i // 2]:
            sieve[i * i // 2::i] = False
    return 2 * np.nonzero(sieve)[0][1::] + 1


def primes_to(n):
    from bitarray import bitarray
    size = n // 2
    sieve = bitarray(size)
    sieve.setall(1)
    limit = int(n**0.5)
    for i in range(1, limit):
        if sieve[i]:
            val = 2 * i + 1
            sieve[(i + i * val)::val] = 0
    return [2] + [2 * i + 1 for i, v in enumerate(sieve) if v and i > 0]


N = 1000
# print( ambi_sieve(N), factors(N), divisors(factors(N)), mobius3(N))
tc = datetime.datetime.now()
print(ambi_sieve(N))
print("ambi sieve", datetime.datetime.now() - tc)
tc = datetime.datetime.now()
print(rwh_primes(N))
print("rwh sieve", datetime.datetime.now() - tc)
tc = datetime.datetime.now()
print(prime6(N))
print("prime6 sieve", datetime.datetime.now() - tc)
tc = datetime.datetime.now()
print(rwh_primes2_python3(N))
print("rwh2 python3 sieve", datetime.datetime.now() - tc)
tc = datetime.datetime.now()
print(primes_simpy(N))
print("simpy primes sieve", datetime.datetime.now() - tc)
tc = datetime.datetime.now()
print(primesfrom3to(N))
print("primesfrom3to", datetime.datetime.now() - tc)
tc = datetime.datetime.now()
print(primesfrom2to(N))
print("primesfrom2to", datetime.datetime.now() - tc)
tc = datetime.datetime.now()
print(primes_to(N))
print("primes_to", datetime.datetime.now() - tc)


# print factors(N), factors2(N), factors3(N)