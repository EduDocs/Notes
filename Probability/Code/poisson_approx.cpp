#include <cmath>
#include <cstdio>
using namespace std;


/*    FACTORIAL    */

float factorial (int k) {

  return tgamma(k + 1);
}


/*    BINOMIAL COEFFICIENT    */

int binomial_coef (int n, int k) {
  int Bnk = 1;

  if (n > k && k > 0)
    { Bnk = binomial_coef(n-1,k) + binomial_coef(n-1,k-1); }
  else
    { Bnk = 1; }

  return Bnk;
}


/*  BINORMIAL PMF  */

double binomial_pmf (double p, int n, int k) {
  double p_x;

  if (k < 0 || k > n)
    { p_x = 0; }
  else
    { p_x = binomial_coef(n, k) * pow(p,k) * pow(1-p,n-k); }

  return p_x;
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
  double lambda = 4;
  int m;
  int n;
  double p;
  double pmf;

  pmf_out = fopen ("approx1.csv","w");
  for (m=0; m<=25; m++)
  {
    fprintf (pmf_out, "%d", m);
    for (n=10; n<=25; n = n+5)
    {
      {
        p = lambda / n;
        pmf = binomial_pmf (p, n, m);
        fprintf (pmf_out, ",%.6f", pmf);
      };
    };
    fprintf (pmf_out, "\n");
  };
  fclose (pmf_out);

  pmf_out = fopen ("poisson1.csv","w");
  for (m=0; m<=25; m++)
  {
    pmf = poisson_pmf (lambda, m);
    fprintf (pmf_out, "%d, %.6f\n", m, pmf);
  };
  fclose (pmf_out);

  return 0;
}

