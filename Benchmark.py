#!/usr/bin/env python3

# import libprimes
import timeit
import sys
import math
import datetime
import prettyplotlib as ppl
import numpy as np
import matplotlib.pyplot as plt
from prettyplotlib import brewer2mpl
import matplotlib.ticker as ticker


primenumbers_gen = [
    'ambi_sieve',
    # 'sundaram3',
    'primesfrom3to',
    'primesfrom2to',
    # 'rwh_primes2_python3',
    'prime6',
    'pyprimesieve',
    # 'primes_simpy',
    # 'primes_bitarray',
    # 'ajs_primes3a'

]


def custom_ticks(x, pos):
    ''' https://stackoverflow.com/questions/36480077/ '''
    if x == 0:
        return "$0$"
    exponent = int(np.log10(x))
    coeff = x / 10**exponent
    return r"${:2.0f} \times 10^{{ {:2d} }}$".format(coeff, exponent)


if __name__ == '__main__':

    # Vars
    n = 10000000  # number itereration generator
    nbcol = 4  # For decompose prime number generator
    # Eliminate false positive value during the test (bench average time)
    nb_benchloop = 3
    datetimeformat = '%Y-%m-%d %H:%M:%S.%f'
    config = 'from __main__ import n; import libprimes'
    primenumbers_gen = {
        'ambi_sieve': {'color': 'b'},
        # 'rwh_primes2_python3': {'color': 'b'},
        # 'sundaram3': {'color': 'b'},
        'primesfrom2to': {'color': 'b'},
        'primesfrom3to': {'color': 'b'},
        # 'primes_simpy': {'color': 'b'},
        'prime6': {'color': 'b'},
        'pyprimesieve': {'color': 'b'},
        # 'primes_bitarray': {'color': 'b'},
        # 'ajs_primes3a': {'color': 'b'},
    }

    # Parse command line options
    if len(sys.argv) <= 1:
        print("Please set loop numbers")
        sys.exit()

    n = int(sys.argv[1])
    step = int(math.ceil(n / float(nbcol)))
    nbs = np.array([i * step for i in range(1, int(nbcol) + 1)])
    set2 = brewer2mpl.get_map('Paired', 'qualitative', 12).mpl_colors

    print(datetime.datetime.now().strftime(datetimeformat))
    print("Compute prime number to %(n)s" % locals())
    print("")

    results = dict()
    for pgen in primenumbers_gen:
        results[pgen] = dict()
        benchtimes = list()
        for n in nbs:
            t = timeit.Timer("libprimes.%(pgen)s(n)" % locals(), setup=config)
            execute_times = t.repeat(repeat=nb_benchloop, number=1)
            benchtime = np.mean(execute_times)
            benchtimes.append(benchtime)
        results[pgen] = {'benchtimes': np.array(benchtimes)}

fig, ax = plt.subplots(1)
plt.ylabel('Computation time (in second)')
plt.xlabel('N')
i = 0
for pgen in primenumbers_gen:

    bench = results[pgen]['benchtimes']
    avgs = np.divide(bench, nbs)
    avg = np.average(bench, weights=nbs)

    # Compute linear regression
    A = np.vstack([nbs, np.ones(len(nbs))]).T
    a, b = np.linalg.lstsq(A, nbs * avgs)[0]

    # Plot
    i += 1
    # label="%(pgen)s" % locals()
    # ppl.plot(nbs, nbs*avgs, label=label, lw=1, linestyle='--', color=set2[i % 12])
    label = "%(pgen)s avg" % locals()
    ppl.plot(nbs, a * nbs + b, label=label, lw=2, color=set2[i % 12])
print(datetime.datetime.now().strftime(datetimeformat))

ppl.legend(ax, loc='upper left', ncol=4)

# Change x axis label
ax.get_xaxis().get_major_formatter().set_scientific(False)
fig.canvas.draw()
ax.xaxis.set_major_formatter(ticker.FuncFormatter(custom_ticks))
ax = plt.gca()

plt.grid()
plt.show()
