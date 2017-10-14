#!/usr/bin/env python3

# import libprimes
import timeit
import sys
import datetime
from tabulate import tabulate
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
    config = 'from __main__ import n; import pyximport; pyximport.install(); import libprimes; import cprimes'
    primenumbers_gen = {
        'cprimes.sundaram3_1': {'color': 'b'},
        'cprimes.sundaram3_2': {'color': 'b'},
        'cprimes.sundaram3_2_1': {'color': 'b'},
        'cprimes.sundaram3_3_1': {'color': 'b'},
        'cprimes.sundaram3_3_2': {'color': 'b'},
        'cprimes.sundaram3_3_3': {'color': 'b'},
        'cprimes.sundaram3_4': {'color': 'b'},
        # Benchmark
        # 'cprimes.primesfrom3to': {'color': 'b'},
    }

    print("Compute prime number to %(n)s" % locals())
    print(datetime.datetime.now().strftime(datetimeformat))
    results = dict()
    for pgen in primenumbers_gen:
        results[pgen] = dict()
        benchtimes = list()
        for n in nbs:
            # t = timeit.Timer("libprimes.%(pgen)s(n)" % locals(), setup=config)
            t = timeit.Timer("%(pgen)s(n)" % locals(), setup=config)
            # execute = timeit.Timer("libprimes.%(pgen)s(n)" % locals(), setup=config)
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
        # ppl.plot(nbs, bench, label=label, lw=2, color=set2[i % 12])
        ppl.plot(nbs, bench, label=label, lw=2)

    ppl.legend(ax, loc='upper left', ncol=4)
    fig.canvas.draw()
    ax = plt.gca()
    plt.grid()
    plt.show()
