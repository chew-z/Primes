#!/usr/bin/env python3

import sys
from fprimes import fprimes
# Don't be lazy compile f2py using check=all option for fortran
# It can save you hours and maybe days of looking for weird errors
# f2py3.6 -c Primes.f90 -m fprimes <-- STUPID
# f2py3.6 --f90flags=-fcheck=all -c Primes.f90 -m fprimes <-- SMART


def primes(n):
    sieve_array = fprimes.sieve(n)
    return fprimes.logical_to_integer(sieve_array, sum(sieve_array), n)


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print(dir(fprimes))
        print(fprimes.__doc__)
        print(fprimes.sieve.__doc__)
        print(fprimes.logical_to_integer.__doc__)

        print("Please set loop numbers")
        sys.exit()

    N = int(sys.argv[1])

    print(primes(N))
