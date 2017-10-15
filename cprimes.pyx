''' This is for experiments with different version of pure Python3, Numpy and 
Cython improvements - especially latest Cython 0.27+.
Comparing different takes on 2-3 selected sieves.

It seems that instead of improving slow algorithm with numpy and especially
cythonization it is more way more effective to simply choose faster algo.

'''

import math
import cython
import Cython.Compiler.Options; Cython.Compiler.Options.annotate = True
cimport numpy as np
# Add CFLAG in virtualenv to link to brew numpy
# export CFLAGS=-I/usr/local/Cellar/numpy/1.13.3/lib/python3.6/site-packages/numpy/core/include
import numpy as np
from libc.math cimport sqrt
from cpython cimport array
import array
from libc.stdlib cimport malloc, free
from libc.string cimport memset

cdef extern from "stdbool.h":
    ctypedef bint bool

cdef unsigned long long div(unsigned long long x, unsigned long long y):
    return x/y


cdef bool * getPrimes1(unsigned long long n):
    # like primesfrom3to
    cdef unsigned long long i, j, half, sq
    half = div(n, 2)
    sq = int(n**0.5) + 1
    cdef bool *primes = <bool*>malloc(half * sizeof(bool))
    memset(primes, 1, half * sizeof(bool))
    # There is big gain from changing for loops to while
    i = 3
    while i < sq:
        if primes[div(i, 2)]:
            j = div(i * i, 2)
            while j < half:
                primes[j] = False
                j += i
        i += 2
    return primes;


def cprimes1(unsigned long long n):
    res = <bool[:n // 2]> (getPrimes1(n))
    return 2 * np.nonzero(res)[0][1::] + 1


cdef bool * getPrimes2(unsigned long long n):
    # like ajs_primes3a
    cdef bool *primes = <bool*>malloc(n * sizeof(bool))
    memset(primes, 1, n * sizeof(bool))
    cdef unsigned long long i, j, half, sq
    half = div(n, 2)
    sq = int(sqrt(n)) + 1

    primes[0] = False
    primes[1] = False
    primes[2] = False
    i = 4
    # There is big gain from changing for loops to while
    while i < n:
        primes[i] = False
        i += 2
    i = 3
    while i < sq:
        j = i * 2
        while j < n:
            primes[j] = False
            j += i
        i += 2
    return primes;


def cprimes2(unsigned long long n):
    res = np.asarray(<bool[:n]> (getPrimes2(n)))
    return np.where(res)[0]


def sundaram3_1(n):
    # pure python3 implementation - basic case
    numbers = list(range(3, n + 1, 2))
    half = (n) // 2
    initial = 4
    for step in range(3, n + 1, 2):
        for i in range(initial, half, step):
            numbers[i - 1] = 0
        initial += 2 * (step + 1)

        if initial > half:
            return [2] + list(filter(None, numbers))


def sundaram3_2(n):
    # Using numpy arrays
    numbers = np.arange(3, n + 1, 2)
    half = (n) // 2
    initial = 4
    for step in range(3, n + 1, 2):
        for i in range(initial, half, step):
            numbers[i - 1] = 0
        initial += 2 * (step + 1)

        if initial > half:
            res = np.asarray(numbers)
            return res[res>0]


def sundaram3_2_1(n):
    # Using numpy arrays
    # Declaring numbers as np.uint64 improved slightly
    # (uint64 0 to 18446744073709551615)
    numbers = np.arange(3, n + 1, 2, dtype=np.uint64)
    half = (n) // 2
    initial = 4
    for step in range(3, n + 1, 2):
        for i in range(initial, half, step):
            numbers[i - 1] = 0
        initial += 2 * (step + 1)

        if initial > half:
            res = np.asarray(numbers)
            return res[res>0]


def sundaram3_3_1(n):
    # Cython arrays from pure python3 using modern Cython arrays and views
    # http://cython.readthedocs.io/en/latest/src/tutorial/array.html
    cdef array.array numbers = array.array('i', range(3, n + 1, 2))
    cdef int[:] numbers_view = numbers
    half = (n) // 2
    initial = 4
    for step in range(3, n + 1, 2):
        for i in range(initial, half, step):
            numbers_view[i - 1] = 0     # warning - index should be typed for
                                        # more effective access
        initial += 2 * (step + 1)

        if initial > half:
            # return [2] + list(filter(None, numbers_view)) - is slower
            return [2] + list(filter(None, numbers))


def sundaram3_3_2(unsigned long long n):
    # Cython arrays from pure python3 like 3_3_1 but with declared index types
    # Not declaring index types we get Cython warning
    # http://cython.readthedocs.io/en/latest/src/tutorial/array.html
    # It is best solution so far
    cdef unsigned long long step, i
    cdef array.array numbers = array.array('L', range(3, n + 1, 2))
    cdef unsigned long long[:] numbers_view = numbers
    half = (n) // 2
    initial = 4
    for step in range(3, n + 1, 2):
        for i in range(initial, half, step):
            numbers_view[i - 1] = 0
        initial += 2 * (step + 1)

        if initial > half:
            return [2] + list(filter(None, numbers))


@cython.cdivision(True)     # turn division by zero checking off - C division
@cython.boundscheck(False)  # turn array bounds check off
@cython.wraparound(False)  # turn negative indexing off
def sundaram3_3_3(unsigned long long n):
    # Cython arrays from pure python3 like 3_3_2 but with checks off
    # http://cython.readthedocs.io/en/latest/src/tutorial/array.html
    # No performance gain compared to 3_3_2...
    cdef unsigned long long step, half, initial, i
    cdef array.array numbers = array.array('L', range(3, n + 1, 2))
    cdef unsigned long long[:] numbers_view = numbers
    half = (n) / 2  # here we could use / in place of // (switching cdivision)
    initial = 4
    for step in range(3, n + 1, 2):
        for i in range(initial, half, step):
            numbers_view[i - 1] = 0
        initial += 2 * (step + 1)

        if initial > half:
            return [2] + list(filter(None, numbers))


def sundaram3_4(unsigned long long n):
    # Mixing numpy arrays and cython array views
    # Seems like consistently the worst solution
    #
    cdef unsigned long long s, i
    # cdef np.ndarray[np.longlong_t, ndim=1] numbers = np.arange(3, n + 1, 2, np.longlong)
    cdef unsigned long long [:] numbers_view = np.arange(3, n + 1, 2, np.ulonglong)
    cdef unsigned long long half = (n) // 2
    cdef unsigned long long initial = 4
    cdef unsigned long long [:] s_view = np.arange(3, n + 1, 2, np.ulonglong)
    cdef unsigned long long [:] i_view
    s = 3
    while s in s_view:
    # for s in s_view:
        i_view =  np.arange(initial, half, s, np.ulonglong)
        i = initial
        while i in i_view:
        #for i in i_view:
            numbers_view[i - 1] = 0
            i += s
        initial += 2 * (s + 1)
        if initial > half:
            numbers = np.asarray(numbers_view)
            return numbers[numbers>0]
        i += 2


def ambi_sieve_1(unsigned long long n):
    # Cythonized from pure python - very bad! Big performance penalty!
    cdef unsigned long long m
    cdef array.array s = array.array('L', range(3, n, 2))
    cdef unsigned long long[:] s_view = s
    cdef array.array em = array.array('L', range(3, int(sqrt(n)) + 1, 2))
    cdef unsigned long long[:] m_view = em
    for m in m_view:
        if s_view[(m - 3) // 2]:
            s_view[(m * m - 3) // 2::m] = 0

    return list(filter(None, s))


# @cython.cdivision(True)    # turn division by zero checking off
# @cython.boundscheck(False)  # turn array bounds check off
# @cython.wraparound(False)  # turn negative indexing off
def ambi_sieve_2(unsigned long long n):
    # Mixing numpy and Cython. No practical improvement.
    # C division gives zero gain here
    cdef unsigned long long m
    cdef np.ndarray[np.longlong_t, ndim=1] s = np.arange(3, n, 2, np.longlong)
    cdef np.ndarray[np.longlong_t, ndim=1] em = np.arange(3, int(sqrt(n)) + 1, 2, np.longlong)
    for m in em:
        if s[(m - 3) // 2]:
            s[(m * m - 3) // 2::m] = 0

    return s[s>0]


# @cython.cdivision(True)    # turn division by zero checking off
# @cython.boundscheck(False)  # turn array bounds check off
# @cython.wraparound(False)  # turn negative indexing off
def primesfrom3to_1(unsigned long long n):
    # Python array.array to cython view but leaving numpy zeros array sieve
    # No effect
    cdef unsigned long long i
    cdef sieve = np.ones(n // 2, dtype=np.bool)
    cdef array.array iv = array.array('L', range(3, int(sqrt(n)) + 1, 2))
    cdef unsigned long long[:] i_view = iv
    for i in i_view:
        if sieve[i // 2]:
            sieve[i * i // 2::i] = False
    return 2 * np.nonzero(sieve)[0][1::] + 1


# @cython.cdivision(True)    # turn division by zero checking off
# @cython.boundscheck(False)  # turn array bounds check off
# @cython.wraparound(False)  # turn negative indexing off
def primesfrom3to_2(unsigned long long n):
    # Cythonizing single array but leaving main sieve in numpy
    # No effect
    cdef unsigned long long i
    cdef sieve = np.ones(n // 2, dtype=np.bool)
    cdef unsigned long long [:] i_view = np.arange(3, int(sqrt(n)) + 1, 2, np.ulonglong)
    for i in i_view:
        if sieve[i // 2]:
            sieve[i * i // 2::i] = False
    return 2 * np.nonzero(sieve)[0][1::] + 1


def primesfrom3to_3(unsigned long long n):
    # Cythonizing numpy zeros array
    cdef unsigned long long i
    cdef np.ndarray[np.uint8_t, ndim=1] sieve = np.ones(n // 2, dtype=np.uint8)
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i // 2]:
            sieve[i * i // 2::i] = False
    return 2 * np.nonzero(sieve)[0][1::] + 1


def primesfrom3to_4(unsigned long long n):
    # Cythonizing both numpy arrays.
    cdef unsigned long long i, half, i2, k
    half = n // 2
    cdef sieve = np.ones(half, dtype=np.uint8)
    cdef unsigned char [:] sieve_view = sieve
    cdef unsigned long long [:] i_view = np.arange(3, int(sqrt(n)) + 1, 2, np.ulonglong)
    for i in i_view:
        i2 = i // 2
        if sieve_view[i2]:
            k =  i * i // 2
            sieve_view[k::i] = False
    return 2 * np.nonzero(sieve_view)[0][1::] + 1


def primesfrom3to_5(unsigned long long n):
    # Terrible idea
    cdef unsigned long long i, j, half
    half = div(n, 2)
    cdef array.array sieve = array.array('B', [1] * (half))
    cdef unsigned char [:] sieve_view = sieve
    for i in range(3, int(sqrt(n)) + 1, 2):
        if sieve[div(i, 2)]:
            for j in range(div(i*i, 2), half, i):
                sieve[j] = False
    return 2 * np.nonzero(sieve_view)[0][1::] + 1
    # return np.asarray(sieve_view)


def prime6(unsigned long long n):
    cdef unsigned long long factor
    cdef np.ndarray[np.longlong_t, ndim=1] primes = np.arange(3, n + 1, 2)
    cdef isprime = np.ones((n - 1) // 2, dtype=np.bool)
    for factor in primes[:int(sqrt(n))]:
        if isprime[(factor - 2) // 2]:
            isprime[(factor * 3 - 2) // 2:(n - 1) // 2:factor] = False
    return np.insert(primes[isprime], 0, 2)


def ajs_primes3a(unsigned long long n):
    cdef unsigned long long idx
    cdef sieve = np.ones((n), dtype=np.bool)
    sieve[0] = False
    sieve[1] = False
    sieve[4::2] = False
    for idx in np.arange(3, int(sqrt(n)) + 1, 2):
        sieve[idx * 2::idx] = False
    return np.where(sieve)[0]


