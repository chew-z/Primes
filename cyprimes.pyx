import math
import cython
import Cython.Compiler.Options; Cython.Compiler.Options.annotate = True
cimport numpy as np
# Add CFLAG in virtualenv to link to brew numpy
# export CFLAGS=-I/usr/local/Cellar/numpy/1.13.3/lib/python3.6/site-packages/numpy/core/include
import numpy as np
from libc.math cimport sqrt


def sundaram3(unsigned long long n):
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

''' All those tricks below give very little improvement over pure numpy and
introduce tons off possibilities for errors and a code that's tricky in details.
So I am freezing this here.
I will try other experiments in Benchmark2.py and cprimes.pyx '''
def ambi_sieve(unsigned long long n):
    cdef unsigned long long m
    # cdef np.ndarray[np.longlong_t, ndim=1] s = np.arange(3, n, 2, np.longlong)
    cdef unsigned long long [:] s_view = np.arange(3, n, 2, np.ulonglong)
    # cdef np.ndarray[np.longlong_t, ndim=1] m_vect = np.arange(3, int(sqrt(n)) + 1, 2, np.longlong)
    cdef unsigned long long [:] m_view = np.arange(3, int(sqrt(n)) + 1, 2, np.ulonglong)
    for m in m_view:
        if s_view[(m - 3) // 2]:
            s_view[(m * m - 3) // 2::m] = 0
    s = np.asarray(s_view)
    return s[s > 0]


def primesfrom2to(unsigned long long n):
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    cdef unsigned long long i, k
    cdef sieve = np.ones(n // 3 + (n % 6 == 2), dtype=np.bool)
    for i in np.arange(1, int(sqrt(n)) // 3 + 1):
        if sieve[i]:
            k = 3 * i + 1 | 1
            sieve[k * k // 3::2 * k] = False
            sieve[k * (k - 2 * (i & 1) + 4) // 3::2 * k] = False
    return np.r_[2, 3, ((3 * np.nonzero(sieve)[0][1:] + 1) | 1)]


def primesfrom3to(unsigned long long n):
    """ Returns an array of primes, 3 <= p < n """
    cdef unsigned long long i
    cdef sieve = np.ones(n // 2, dtype=np.bool)
    cdef unsigned long long [:] i_view = np.arange(3, int(sqrt(n)) + 1, 2, np.ulonglong)
    for i in i_view:
        if sieve[i // 2]:
            sieve[i * i // 2::i] = False
    return 2 * np.nonzero(sieve)[0][1::] + 1


def primes_bitarray(unsigned long long n):
    from bitarray import bitarray
    cdef unsigned long long i
    cdef size = n // 2
    sieve = bitarray(size)
    sieve.setall(1)
    for i in range(1, int(sqrt(n))):
        if sieve[i]:
            val = 2 * i + 1
            sieve[(i + i * val)::val] = False
    return np.r_[2, ((2 * np.nonzero(sieve)[0][1:] + 1) | 1)]


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


def primes(int nmax):       # declare types of parameters
    cdef int n, k, i        # declare types of variables
    cdef int p[10000]        # including arrays
    result = []             # can still use normal Python types
    kmax = 10000
    if kmax > 10000:         # in this case need to hardcode limit
        kmax = 10000
    k = 0
    n = 2
    while k < kmax and n < nmax:
        i = 0
        while i < k and n % p[i] != 0:
            i += 1
        if i == k:
            p[k] = n
            k += 1
            result.append(n)
        n += 1
    return result  # return Python object


def nth_prime(unsigned long long n):
    cdef unsigned long long prime_count
    cdef unsigned long long num

    def _is_prime(unsigned long long num):
        cdef unsigned long long i
        for i in range(3, int(sqrt(num))+1, 2):
            if num % i == 0:
                return False
        return True

    assert n > 0
    if n == 1:
        return 2
    if n == 2:
        return 3
    prime_count = 2
    num = 3
    while prime_count != n:
        num += 2
        if _is_prime(num):
            prime_count += 1
    return num

