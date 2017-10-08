#!/usr/bin/env python3
# coding: utf-8
# various algos counting prime numbers < N
# each better or more pythonic then previous

import sys
import datetime
import libprimes


if __name__ == '__main__':

    # Parse command line options
    if len(sys.argv) <= 1:
        print("Please set loop numbers")
        sys.exit()

    n = int(sys.argv[1])
    N = n

    # print divisors([2, 3, 5])

    # print sorted(all_factors({2:3, 3:2, 5:1}))

    # print [m(N, k) for k in factors(N)], mobius3(N)

    # print [mobius3(n) for n in range(100)]

    # print [mu(n) for n in range(N)]

    # mob = [mobius3(k) for k in range(1, N)]
    # print mob, len(mob)

    tc = datetime.datetime.now()
    print("Ri4", libprimes.Ri4(N), datetime.datetime.now() - tc)
    tc = datetime.datetime.now()
    print("Ri2", libprimes.Ri2(N), datetime.datetime.now() - tc)
    tc = datetime.datetime.now()
    print("Ri", libprimes.Ri(N), datetime.datetime.now() - tc)
    tc = datetime.datetime.now()
    print("R", libprimes.R(N), datetime.datetime.now() - tc)

    # print reduce(mul, [m(n, k) for k in factors(n)], 1)

    # print [mobius2(i) for i in range(1000)]

    # print [factors(i) for i in range(1000)]

    # for N in range(10, 10000, 1000):
    #   print R(N), li(N), Li(N), N/np.log(N)

    # print factors(N), factors2(N), factors3(N)