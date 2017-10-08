#!/usr/bin/env python3
# coding: utf-8
# plots prime counting functions

import sys
import libprimes
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':

    # Parse command line options
    if len(sys.argv) <= 1:
        print("Please set loop numbers")
        sys.exit()

    N = int(sys.argv[1])
    n = np.logspace(1, N)

    plt.grid(False)
    plt.title('n/log(n) ~ Li(n) ~ Ri(n)')
    plt.yscale('log')
    plt.ylim(10, 2 * 10**(N - 1))
    p1 = plt.plot(n, n / np.log(n), lw=2, c='b')
    p2 = plt.plot(n, libprimes.Li(n), lw=2, c='g')
    p3 = plt.plot(n, libprimes.Ri4(n), lw=2, c='r')
    plt.legend([p1[0], p2[0], p3[0]], ['n/log(n)', 'Li(n)', 'Ri(n)'], loc=4)
    plt.show()
