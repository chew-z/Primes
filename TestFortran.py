#!/usr/bin/env python3

import sys
import numpy as np
import libprimes
from fprimes import fprimes
# Don't be lazy compile f2py using check=all option for fortran
# It can save you hours and maybe days of looking for weird errors
# f2py3.6 -c Primes.f90 -m fprimes <-- STUPID
# f2py3.6 --f90flags=-fcheck=all -c Primes.f90 -m fprimes <-- SMART


def primes(n):
    sieve_array = fprimes.sieve(n)
    return fprimes.logical_to_integer(sieve_array, sum(sieve_array), n)


def primes2(n):
    # pi = int(libprimes.Ri4(n))
    # pi = int(1.2 * n / np.log(n))
    pi = int(0.123 * n)
    # primes = np.zeros(pi, dtype=np.int32, order='F')
    primes = fprimes.all_in_one(n, pi)
    return primes


def primes3(n):
    sieve_array = fprimes.sieve(n)
    return 1 + np.nonzero(sieve_array)[0]


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print(dir(fprimes))

        print(fprimes.__doc__)
        print(fprimes.sieve.__doc__)
        print(fprimes.logical_to_integer.__doc__)
        print(fprimes.all_in_one.__doc__)

        print("Please set loop numbers")
        sys.exit()

    N = int(sys.argv[1])

    print(primes(N))
    print(primes2(N))
    print(primes3(N))
