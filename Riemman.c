#include <stdio.h>
#include<math.h>
#include <gsl/gsl_sf_zeta.h>

int main(void)
{

  printf("ζ(%g) = %.12e\n", -1.0, gsl_sf_zeta(-1.0));
  printf("ζ(%g) = %.12e\n", 0.0, gsl_sf_zeta(0.0));
  printf("ζ(%g) = %.12e\n", 0.5, gsl_sf_zeta(0.5));
  printf("ζ(%g) = %.12e\n", 1.0, gsl_sf_zeta(0.99999));
  printf("ζ(%g) = %.12e\n", 2.0, gsl_sf_zeta(2.0));
  printf("ζ(%g) = %.12e\n", M_PI*M_PI/6, gsl_sf_zeta(M_PI*M_PI/6));
  return 0;
}

