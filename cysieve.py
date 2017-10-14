
import pyximport; pyximport.install()
import cprimes
import numpy as np
import sys

# for i in range(1, 10):
#     print('primes below 10**%d: %d' % (i, sieve.eratosthenes(10**i)))


def primes(n):
    for i in range(2, n):
        yield cprimes.nth_prime(i)


if __name__ == '__main__':

    # Parse command line options
    if len(sys.argv) <= 1:
        print("Please set loop numbers")
        sys.exit()

    N = int(sys.argv[1])
    # print(cprimes.sundaram3(N))
    print(cprimes.ambi_sieve(N))
    # print(cprimes.prime6(N))
    # print(cprimes.primes_bitarray(N))
    # print(cprimes.primesfrom2to(N))
    print(cprimes.primesfrom3to(N))
    # P = np.fromiter(primes(N), dtype=int)
    # print(P)

