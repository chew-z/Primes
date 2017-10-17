#include <stdio.h>
#include <stdlib.h>
#include<stdbool.h>
#include<string.h>
#include<math.h>

/* C99
 * ULLONG_MAX +18 446 744 073 709 551 615 - but it clearly goes wild before
 * heap size, physical memory size etc. 
 * from there turtles all the way down - tricks, bits or special libraries..
 */
#define MAX_N 4000000000


static bool * getPrimes(uint64_t n, uint64_t half) {
    bool * primes = (bool *)malloc(half * sizeof(bool));
    uint64_t i, j, sq, index;
    memset(primes, 1, half * sizeof(bool));
    sq = (uint64_t)(sqrt(n) +1);

    for(i = 3; i < sq; i += 2) {
        index = (uint64_t)(i/2);
        if(primes[index] == true) {
            for(j = (uint64_t) (i * i / 2); j < half; j += i) {
                primes[j] = false;
            }
        }
    }
    return primes;
}

/* Effective sieve algorithm - generating primes */
int main(int argc, char* argv[]) {
    bool * p, * temp;
    uint64_t i, N, Half;

    N = atoi(argv[1]);
    if (N > MAX_N) {
        N = MAX_N;
        printf("Maximum allowed N is %ld Turtles all the way down.\n", MAX_N);
    }

    Half = (uint64_t)(N / 2);
    p = (bool*)malloc(N * sizeof(bool));
    memset(p, 0, N * sizeof(bool));

    temp = getPrimes(N, Half);
    for(i=1; i < Half; i++) {
        if ( temp[i] == true) {
            p[2*i+1] = true;
        }
    }
    free(temp);
    if ( N < 1000) {
        for(i=1; i < N; i++) {
            if( p[i] == true)
                printf("%llu ", i);
        }
    } else {
        for(i=1; i < 100; i++) {
            if(p[i] == true)
                printf("%llu ", i);
        }
        printf("... ");
        for(i=N-1; i > N-100; i--) {
            if(p[i] == true)
                printf("%llu ", i);
        }
    }
    free(p);
    return 0;
}
