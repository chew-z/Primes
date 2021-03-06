#!/usr/bin/env python3

# ULLONG_MAX +18 446 744 073 709 551 615

# import libprimes
import timeit
import sys
import datetime
import prettyplotlib as ppl
import numpy as np
import matplotlib.pyplot as plt
from prettyplotlib import brewer2mpl
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)


if __name__ == '__main__':

    # Parse command line options
    if len(sys.argv) <= 1:
        print("Please set loop numbers")
        sys.exit()
    N = int(sys.argv[1])
    n = 10**N
    nbs = np.array([10**i for i in range(3, N + 1)])

    nb_benchloop = 3
    datetimeformat = '%Y-%m-%d %H:%M:%S.%f'
    config = 'from __main__ import n; import pyximport; pyximport.install(); \
        import libprimes; import cprimes; import TestFortran'
    primenumbers_gen = {
        # 'libprimes.sundaram3': {'color': 'b'},
        # 'cprimes.sundaram3_4': {'color': 'b'},
        # 'cprimes.sundaram3_1': {'color': 'b'},
        # 'cprimes.sundaram3_2': {'color': 'b'},
        # 'cprimes.sundaram3_2_1': {'color': 'b'},
        # 'cprimes.sundaram3_3_1': {'color': 'b'},
        # 'cprimes.sundaram3_3_2': {'color': 'b'},
        # 'cprimes.sundaram3_3_3': {'color': 'b'},
        #
        # 'cprimes.cprimes_ajs': {'color': 'b'},
        #
        # 'cprimes.ambi_sieve_1': {'color': 'b'},
        # 'cprimes.ambi_sieve_2': {'color': 'b'},
        # 'libprimes.ambi_sieve': {'color': 'b'},
        # Our Benchmark
        'libprimes.primesfrom3to': {'color': 'b'},
        # 'cprimes.primesfrom3to_1': {'color': 'b'},
        # 'cprimes.primesfrom3to_2': {'color': 'b'},
        # 'cprimes.primesfrom3to_3': {'color': 'b'},
        # 'cprimes.primesfrom3to_4': {'color': 'b'},
        # 'cprimes.primesfrom3to_5': {'color': 'b'},
        # 'cprimes.cprimes_primesfrom3to': {'color': 'b'},
        # Breaks with error
        # malloc: *** error for object 0x7feb99a2ac00: incorrect checksum for
        # freed object - object was probably modified after being freed
        # https://stackoverflow.com/questions/35944478
        # https://stackoverflow.com/questions/12309161/malloc-error-in-f2py
        # 'TestFortran.primes': {'color': 'b'},
        'TestFortran.primes2': {'color': 'b'},
        # 'TestFortran.primes3': {'color': 'b'},
    }

    print("Compute prime number to {0:G}".format(n))
    print(datetime.datetime.now().strftime(datetimeformat))
    results = dict()
    for pgen in primenumbers_gen:
        results[pgen] = dict()
        benchtimes = list()
        for n in nbs:
            t = timeit.Timer("%(pgen)s(n)" % locals(), setup=config)
            execute = timeit.Timer("%(pgen)s(n)" % locals(), setup=config)
            execute_times = t.repeat(repeat=nb_benchloop, number=1)
            benchtime = np.mean(execute_times)
            benchtimes.append(benchtime)
        print('.', end='', flush=True)
        results[pgen] = {'benchtimes': np.array(benchtimes)}
    print('')
    print(datetime.datetime.now().strftime(datetimeformat))

    fig, ax = plt.subplots(1)
    plt.ylabel('Computation time (in milisec) - log scale.')
    plt.xlabel('N - log scale')
    plt.xscale('log')
    plt.yscale('log')
    set2 = brewer2mpl.get_map('Paired', 'qualitative', 12).mpl_colors
    i = 0
    np.set_printoptions(suppress=True)
    np.set_printoptions(precision=2)
    print("Results in miliseconds")
    for pgen in primenumbers_gen:
        bench = results[pgen]['benchtimes'] * 1000
        print("%(pgen)s avg" % locals(), bench)
        i += 1
        label = "%(pgen)s avg" % locals()
        ppl.plot(nbs, bench, label=label, lw=2, color=set2[i % 12])

    ppl.legend(ax, loc='upper left', ncol=4)
    fig.canvas.draw()
    ax = plt.gca()
    plt.grid()
    plt.show()

    print("Don't waist your time improving ineffective algorithm!\n \
        Use better algo!")
