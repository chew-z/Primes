#!/usr/bin/env python3
# coding: utf-8
# various algos generating prime numbers < N, factors and couting primes < N
# 

import itertools
import numpy as np
from operator import mul
from functools import reduce

GAMMA = 0.57721566490153286061
li2 = 1.045163780117492784844588889194  # Li(x) = li(x) - li(2)


# FACTORS AND DIVISORS

def factors(n):
    # with list
    return [p for p in ambi_sieve(n + 1) if n % p == 0]


def factors2(n):
    # with generator
    return (p for p in ambi_sieve(n + 1) if n % p == 0)  # generator


def factors3(n):
    # with yield
    for p in primesfrom2to(n + 1):
        if n % p == 0:
            yield p  # yield


def all_factors(prime_dict):
    series = [[p**e for e in range(maxe + 1)]
              for p, maxe in prime_dict.items()]
    for multipliers in itertools.product(*series):
        yield reduce(mul, multipliers)


def divisors(factors):
    # Generates all divisors, unordered, from the prime factorization.
    ps = sorted(set(factors))
    omega = len(ps)

    def rec_gen(n=0):
        if n == omega:
            yield 1
        else:
            pows = [1]
            for j in range(factors.count(ps[n])):
                pows += [pows[-1] * ps[n]]
            for q in rec_gen(n + 1):
                for p in pows:
                    yield p * q

    for p in rec_gen():
        yield p

# Mu functions


def m1(n, p):
    return -1 if (n / p) % p else 0


def m2(n, f):
    # zero if duplicated factor, -1 otherwise
    return 0 if (n / f) % f == 0 else - 1


def m(n, f):
    # lambda in explicit way
    if (n / f) % f == 0:
        return 0
    else:
        return -1


def mu(n):
    # Works. But difficult to understand code for n == 1
    return reduce(mul, [m1(n, p) for p in factors3(n)], 1)


# PRIME SIEVES


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
            isprime[(factor * 3 - 2) // 2:(n - 1) // 2:factor] = False
    return np.insert(primes[isprime], 0, 2)


def primes_simpy(n):
    from sympy import sieve
    return list(sieve.primerange(1, n))


def pyprimesieve(n):
    import pyprimesieve
    return list(pyprimesieve.primes(n))


def ajs_primes3a(n):
    sieve = np.ones((n), dtype=bool)
    sieve[0] = False
    sieve[1] = False
    sieve[4::2] = False
    for idx in range(3, int(n ** 0.5) + 1, 2):
        sieve[idx * 2::idx] = False
    # return np.where(mat == True)[0]
    return np.where(sieve)[0]


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


def primes_bitarray(n):
    from bitarray import bitarray
    size = n // 2
    sieve = bitarray(size)
    sieve.setall(1)
    for i in range(1, int(n**0.5)):
        if sieve[i]:
            val = 2 * i + 1
            sieve[(i + i * val)::val] = False
    # return [2] + [2 * i + 1 for i, v in enumerate(sieve) if v and i > 0]
    # return np.r_[2, (2 * np.nonzero(sieve)[0][1:] + 1)]
    # return 2 * np.nonzero(sieve)[0][1::] + 1
    return np.r_[2, ((2 * np.nonzero(sieve)[0][1:] + 1) | 1)]


# Moebius, Li and Riemann


def mobius(n):
    # My definition of Mobius.
    if n == 1:
        return 1
    else:
        # zero if duplicated factor, -1 otherwise
        # multiply all. if either is duplicated = 0
        return reduce(mul, [m2(n, k) for k in factors(n)], 1)


# tuple of Mobius(k) computed outside R(x) calls
moby = tuple(mobius(k) for k in range(1, 101))


def li(x):
    # programmingpraxis.com/2011/07/29/approximating-pi
    # mathworld.wolfram.com/LogarithmicIntegral.html
    return GAMMA + np.log(np.log(x)) + sum(pow(np.log(x), k) /
                                           (reduce(mul, range(1, k + 1)) * k) for k in range(1, 101))


def Li(x):
    return li(x) - li2


def R(x):
    # mathworld.wolfram.com/RiemannPrimeCountingFunction.html
    # suboptimal. don't bother with k where mobius(k)==0
    return sum(mobius(k) / k * li(pow(x, 1.0 / k)) for k in range(1, 101))


def Ri(x):
    # mathworld.wolfram.com/RiemannPrimeCountingFunction.html
    # with generator computing Mobius(k) twice but ignoring k where Mobius == 0
    return sum(mobius(k) / k * li(pow(x, 1.0 / k)) for k in range(1, 101) if mobius(k) != 0)


def Ri2(x):
    # mathworld.wolfram.com/RiemannPrimeCountingFunction.html
    # with tuple ignoring k where Mobius == 0
    mob = tuple(mobius(k) for k in range(1, 101))
    return sum(mob[k - 1] / k * li(pow(x, 1.0 / k)) for k in range(1, 101) if mob[k - 1] != 0)


def Ri3(x):
    # mathworld.wolfram.com/RiemannPrimeCountingFunction.html
    # with generator ignoring k where Mobius == 0
    mob = ((k, mobius(k)) for k in range(1, 101))
    return sum(mu / k * li(pow(x, 1.0 / k)) for (k, mu) in mob if mu != 0)


def Ri4(x):
    # mathworld.wolfram.com/RiemannPrimeCountingFunction.html
    # with tuple ignoring k where Mobius == 0
    return sum(moby[k - 1] / k * li(pow(x, 1.0 / k)) for k in range(1, 101) if moby[k - 1] != 0)