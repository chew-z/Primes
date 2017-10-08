#!/usr/bin/env python3

# import libprimes
import timeit
import sys
import datetime
import prettyplotlib as ppl
import numpy as np
import matplotlib.pyplot as plt
from prettyplotlib import brewer2mpl


primenumbers_gen = [
    'ambi_sieve',
    'sundaram3',
    'primesfrom3to',
    'primesfrom2to',
    'rwh_primes2_python3',
    'prime6',
    'pyprimesieve',
    'primes_simpy',
    'primes_bitarray',
    'ajs_primes3a'
]


if __name__ == '__main__':

    # Parse command line options
    if len(sys.argv) <= 1:
        print("Please set loop numbers")
        sys.exit()
    N = int(sys.argv[1])
    n = 10**N
    step = 1
    nbs = np.array([10**i for i in range(1, N + 1)])

    nb_benchloop = 3
    datetimeformat = '%Y-%m-%d %H:%M:%S.%f'
    config = 'from __main__ import n; import libprimes'
    primenumbers_gen = {
        'ambi_sieve': {'color': 'b'},
        'rwh_primes2_python3': {'color': 'b'},
        'sundaram3': {'color': 'b'},
        'primesfrom2to': {'color': 'b'},
        'primesfrom3to': {'color': 'b'},
        'primes_simpy': {'color': 'b'},
        'prime6': {'color': 'b'},
        'pyprimesieve': {'color': 'b'},
        'primes_bitarray': {'color': 'b'},
        'ajs_primes3a': {'color': 'b'},
    }

    print("Compute prime number to %(n)s" % locals())
    print(datetime.datetime.now().strftime(datetimeformat))
    results = dict()
    for pgen in primenumbers_gen:
        results[pgen] = dict()
        benchtimes = list()
        for n in nbs:
            t = timeit.Timer("libprimes.%(pgen)s(n)" % locals(), setup=config)
            execute_times = t.repeat(repeat=nb_benchloop, number=1)
            benchtime = np.mean(execute_times)
            benchtimes.append(benchtime)
        print('.', end='', flush=True)
        results[pgen] = {'benchtimes': np.array(benchtimes)}
    print('')
    print(datetime.datetime.now().strftime(datetimeformat))

    fig, ax = plt.subplots(1)
    plt.ylabel('Computation time (in miliseconds)')
    plt.xlabel('N')
    plt.xscale('log')
    plt.yscale('log')
    set2 = brewer2mpl.get_map('Paired', 'qualitative', 12).mpl_colors
    i = 0
    for pgen in primenumbers_gen:
        bench = results[pgen]['benchtimes'] * 1000
        i += 1
        label = "%(pgen)s avg" % locals()
        ppl.plot(nbs, bench, label=label, lw=2, color=set2[i % 12])

    ppl.legend(ax, loc='upper left', ncol=4)
    fig.canvas.draw()
    ax = plt.gca()
    plt.grid()
    plt.show()
