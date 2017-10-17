#!/usr/bin/env python3
# https://gist.github.com/sangheestyle/1f08a6e5294cb8442130e117fd50e5ca

from datetime import datetime

from numba import jit
from numpy import arange

# jit decorator tells Numba to compile this function.
# The argument types will be inferred by Numba when function is called.
@jit
def sum2d(arr):
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i,j]
    return result

begin = datetime.now()
size = 10000
a = arange(size * size).reshape(size,size)
print(sum2d(a))
end = datetime.now()
print("duration: {} ms".format(end - begin))

