#!/usr/bin/env python3

import sys
import numpy as np
import fprimes      # f2py3.6 -c Primes.f90 -m fprimes


def primes(n):
    sieve_array = fprimes.sieve(n)
    prime_numbers = fprimes.logical_to_integer(sieve_array, sum(sieve_array))
    return prime_numbers


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print(fprimes.__doc__)
        print(fprimes.sieve.__doc__)
        print(fprimes.logical_to_integer.__doc__)

        print("Please set loop numbers")
        sys.exit()

    N = int(sys.argv[1])

    print(primes(N))

