#!/usr/bin/env python

import libprimes
import sys
import prettyplotlib as ppl
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':

    # Parse command line options
    if len(sys.argv) <= 1:
        print("Please set loop numbers")
        sys.exit()

    n = int(sys.argv[1])
    N = 10**n
    div = 100
    step = N / div
    x = np.arange(2, N, step, dtype=int)
    ri = libprimes.Ri4(x)
    delta = np.r_[step / np.log(step), np.diff(ri)]
    primes = libprimes.primesfrom3to(N)

    # Compute histogram
    hist = np.histogram(primes, bins=div)
    y = hist[0]

    # Graph
    plt.ylabel('Count of primes')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    # plt.xscale('log')
    ppl.plot(x, y, 'o', label='count of primes')
    ppl.plot(x, delta, "--", label="Riemman function")
    ppl.legend()
    plt.grid()
    plt.show()
