#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define N        1000000000

int main(void)
{
    int       arraySize = ((N + 63)/64 + 1) * sizeof(uint32_t);
    uint32_t *primes    = malloc(arraySize);

    // Each bit in primes is an odd number.
    // Bit 0 = 1, bit 1 = 3, bit 2 = 5, etc.
    memset(primes, 0xff, arraySize);

    // 1 is not a prime.
    primes[0] &= ~0x1;

    int sqrt_N = sqrt(N);
    for(int i = 3; i <= sqrt_N; i += 2) {
        int iIndex = i >> 6;
        int iBit   = (1 << ((i >> 1) & 31));
        if ((primes[iIndex] & iBit) != 0) {
            int increment = i+i;
            for (int j = i * i; j < N; j += increment) {
                int jIndex = j >> 6;
                int jBit   = (1 << ((j >> 1) & 31));
                primes[jIndex] &= ~jBit;
            }
        }
    }

    // Count the number of primes in order to verify that the above worked.
    // Start count at 1 to include 2 as the first prime, since we are only
    // going to count odd primes.
    int count = 1;
    for (int i = 3; i < N; i += 2) {
        int iIndex = i >> 6;
        int iBit   = (1 << ((i >> 1) & 31));
        if (primes[iIndex] & iBit)
            count++;
    }
    printf("%d\n", count);

    free(primes);
    return 0;
}
