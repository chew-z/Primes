#include <stdio.h>
#include <stdlib.h>
#include<stdbool.h>
#include<string.h>
#include<math.h>

/* 
 * This is less readable code then Primes1.c without any benefit.
 * */

/*
 * ULLONG_MAX +18 446 744 073 709 551 615 - but it clearly goes wild before
 * largest prime generated being 1215752191 on my machine. It all turtles down
 * from there forward - tricks, bits or special libraries.. 
*/
#define MAX_N 4000000000


static void getPrimes(uint64_t *n, uint64_t *half, bool _tp[]) {
    uint64_t i, j, sq, index;
    memset(_tp, 1, *half * sizeof(bool));
    sq = (uint64_t)(sqrt(*n) +1);
    for(i = 3; i < sq; i += 2) {
        index = (uint64_t)(i/2);
        if(_tp[index] == true) {
            for(j = (uint64_t) (i * i / 2); j < *half; j += i) {
                _tp[j] = false;
             }
        }
    }
}

/* Effective sieve algorithm - generating primes */
int main(int argc, char* argv[]) {
    uint64_t i, N, Half;

    N = atoi(argv[1]);
    if (N > MAX_N) {
        N = MAX_N;
        printf("Maximum allowed N is %ld\n", MAX_N);
    }
    Half = (uint64_t)(N / 2);

    bool *primes = (bool*)malloc(N * sizeof(bool));
    bool *tp = (bool*)malloc(Half * sizeof(bool));

    getPrimes(&N, &Half, tp);
    memset(primes, 0, N * sizeof(bool));
    for(i=1; i < Half; i++) {
        if ( tp[i] == true) {
            primes[2*i+1] = true;
        }
    }
    free(tp);
    if ( N < 1000) {
        for(i=1; i < N; i++) {
            if( primes[i] == true)
                printf("%llu ", i);
        }
    } else {
        for(i=1; i < 100; i++) {
            if(primes[i] == true)
                printf("%llu ", i);
        }
        printf("... ");
        for(i=N-1; i > N-100; i--) {
            if(primes[i] == true)
                printf("%llu ", i);
        }
    }
    return 0;
}
