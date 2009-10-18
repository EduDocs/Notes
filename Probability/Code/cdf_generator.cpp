#include <cmath>
#include <cstdio>
using namespace std;


/*    FACTORIAL
  The factoral function is needed in the computation of various PMFs.
  It is implemented here using the Gamma function (tgamma), which is
  included in the standard <cmath> library.
*/

float factorial (int k) {

  return tgamma(k + 1);
}


/*    BINOMIAL COEFFICIENT
  The binomial coefficient is also needed in computing various PMFs.
  We chose to implement it through a simple recursion.
*/


int binomial_coef (int n, int k) {
  int Bnk = 1;

  if (n > k && k > 0)
    { Bnk = binomial_coef(n-1,k) + binomial_coef(n-1,k-1); }
  else
    { Bnk = 1; }

  return Bnk;
}


/*  POISSON PMF */

double poisson_pmf (double lambda, int k) {
  double p_n;

  p_n = pow(lambda,k) * exp(-lambda) / factorial(k);

  return p_n;
}


/*  MAIN  */

int main () {
  FILE * pmf_out;
  int m;
  int n = 8;
  double pmf, cdf;

  pmf_out = fopen ("data_cdf.csv","w");
  cdf = 0;
  for (m=0; m<=12; m++)
  {
    pmf = poisson_pmf (2, m);
    cdf = cdf + pmf;
    fprintf (pmf_out, "%d %.6f %.6f\n", m, pmf, cdf);
  };
  fclose (pmf_out);

  return 0;
}

