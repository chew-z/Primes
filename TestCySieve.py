''' This is for calling simple check if it is works '''

import sys
import pyximport
pyximport.install()
import cprimes
import libprimes

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
    # print(cprimes.sundaram3_1(N))
    # print(cprimes.sundaram3_2(N))
    # print(cprimes.sundaram3_2_1(N))
    # print(cprimes.sundaram3_3_1(N))
    # print(cprimes.sundaram3_3_2(N))
    # print(cprimes.sundaram3_3_3(N))
    # print(cprimes.sundaram3_4(N))
    #
    # print(cprimes.ambi_sieve_1(N))
    # print(cprimes.ambi_sieve_2(N))
    # print(libprimes.ambi_sieve(N))
    # print(cprimes.prime6(N))
    # print(cprimes.primes_bitarray(N))
    # print(cprimes.primesfrom2to(N))
    #
    print(libprimes.primesfrom3to(N))
    print(cprimes.primesfrom3to_1(N))
    print(cprimes.primesfrom3to_2(N))
    print(cprimes.primesfrom3to_3(N))
    print(cprimes.primesfrom3to_4(N))
