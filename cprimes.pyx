''' This is for experiments with different version of pure Python3, Numpy and 
Cypython improvements - especially latest Cython 0.27+.
Comparing different takes on 2-3 selected sieves.'''

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
    # It is actually quite effective itself for larger numbers
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
    # It is actually quite effective for larger numbers
    cdef unsigned long long step, i
    cdef array.array numbers = array.array('i', range(3, n + 1, 2))
    cdef int[:] numbers_view = numbers
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
    # It is actually most effective so far
    cdef unsigned long long step, half, initial, i
    cdef array.array numbers = array.array('i', range(3, n + 1, 2))
    cdef int[:] numbers_view = numbers
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
    for s in s_view:
        i_view =  np.arange(initial, half, s, np.ulonglong)
        for i in i_view:
            numbers_view[i - 1] = 0
        initial += 2 * (s + 1)
        if initial > half:
            numbers = np.asarray(numbers_view)
            return numbers[numbers>0]


@cython.cdivision(True)    # turn division by zero checking off
@cython.boundscheck(False)
def ambi_sieve(unsigned long long n):
    cdef unsigned long long m
    # cdef np.ndarray[np.longlong_t, ndim=1] s = np.arange(3, n, 2, np.longlong)
    cdef unsigned long long [:] s_view = np.arange(3, n, 2, np.ulonglong)
    # cdef np.ndarray[np.longlong_t, ndim=1] m_vect = np.arange(3, int(sqrt(n)) + 1, 2, np.longlong)
    cdef unsigned long long [:] m_view = np.arange(3, int(sqrt(n)) + 1, 2, np.ulonglong)
    for m in m_view:
        # if s_view[(m - 3) // 2]:
        if s_view[(m - 3) / 2]:
            s_view[(m * m - 3) / 2::m] = 0
    s = np.asarray(s_view)
    return s[s > 0]


@cython.cdivision(True)    # turn division by zero checking off '/ vs //'
def primesfrom3to(unsigned long long n):
    """ Returns an array of primes, 3 <= p < n """
    cdef unsigned long long i
    cdef sieve = np.ones(n / 2, dtype=np.bool)
    cdef unsigned long long [:] i_view = np.arange(3, int(sqrt(n)) + 1, 2, np.ulonglong)
    for i in i_view:
        if sieve[i / 2]:
            sieve[i * i / 2::i] = False
    return 2 * np.nonzero(sieve)[0][1::] + 1


def prime6(unsigned long long n):
    cdef unsigned long long factor
    cdef np.ndarray[np.longlong_t, ndim=1] primes = np.arange(3, n + 1, 2)
    cdef isprime = np.ones((n - 1) // 2, dtype=bool)
    for factor in primes[:int(sqrt(n))]:
        if isprime[(factor - 2) // 2]:
            isprime[(factor * 3 - 2) // 2:(n - 1) // 2:factor] = False
    return np.insert(primes[isprime], 0, 2)


def ajs_primes3a(unsigned long long n):
    cdef unsigned long long idx
    cdef sieve = np.ones((n), dtype=bool)
    sieve[0] = False
    sieve[1] = False
    sieve[4::2] = False
    for idx in np.arange(3, int(sqrt(n)) + 1, 2):
        sieve[idx * 2::idx] = False
    return np.where(sieve)[0]


