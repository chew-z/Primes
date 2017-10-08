#!/usr/bin/env python3

import sys
import libprimes

if __name__ == '__main__':

    # Parse command line options
    if len(sys.argv) <= 1:
        print("Please set loop numbers")
        sys.exit()

    n = int(sys.argv[1])

    print(libprimes.pyprimesieve(n))
