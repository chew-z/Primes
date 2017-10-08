#!/usr/bin/env python

import libprimes
import sys
import prettyplotlib as ppl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


if __name__ == '__main__':

    # Parse command line options
    if len(sys.argv) <= 1:
        print("Please set loop numbers")
        sys.exit()

    # Vars
    n = int(sys.argv[1])
    div = 100
    step = n / div

    # With range
    x = np.arange(0, n + step, step)
    drawx = x[1:]
    primes = libprimes.primesfrom3to(n)

    # Compute histogram
    hist = np.histogram(primes, bins=x)
    y = hist[0]

    # # Fit
    coefficients = np.polyfit(np.log(drawx), y, 1)
    fit = np.poly1d(coefficients)

    # Graph
    fig, ax = ppl.subplots(1)
    plt.ylabel('Number primes')
    # plt.xlabel('In (%s) range (Less than)' % libprimes.human_format(int(step)))

    ppl.plot(x[1:], y, 'o', label='number primes')
    # ppl.plot(x, fit(np.log(x)), "--", label="fit")

    # Change x axis label
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    fig.canvas.draw()
    # ax.xaxis.set_major_formatter(ticker.FuncFormatter(libprimes.custom_ticks))
    ax = plt.gca()

    ppl.legend()
    plt.grid()
    plt.show()
