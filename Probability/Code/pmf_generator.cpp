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


/*  BERNOULLI PMF  */

double bernoulli_pmf (double p, int k) {
  double p_x;

  if (k == 1)
    { p_x = p; }
  else if (k == 0)
    { p_x = 1-p; }
  else
    { p_x = 0; }

  return p_x;
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


/*  GEOMETRIC PMF  */

double geometric_pmf (double p, int k) {
  double p_x;

  p_x = pow((1 - p),k) * p;
  return p_x;
}


/*  UNIFORM  */

double uniform_pmf (int n, int k) {
  double p_x;

  if (k >= 1 && k <= n)
    { p_x = 1.0 / n ; }
  else
    { p_x = 0; }

  return p_x;
}


/*  MAIN  */

int main () {
  FILE * pmf_out;
  int m;
  int n = 8;
  double pmf;

  pmf_out = fopen ("data1.csv","w");
  for (m=0; m<=4; m++)
  {
    pmf = bernoulli_pmf (0.25, m);
    fprintf (pmf_out, "%d %.6f\n", m, pmf);
  };
  fclose (pmf_out);

  pmf_out = fopen ("data2.csv","w");
  for (m=0; m<=9; m++)
  {
    pmf = binomial_pmf (0.25, n, m);
    fprintf (pmf_out, "%d %.6f\n", m, pmf);
  };
  fclose (pmf_out);

  pmf_out = fopen ("data3.csv","w");
  for (m=0; m<=14; m++)
  {
    pmf = poisson_pmf (2, m);
    fprintf (pmf_out, "%d %.6f\n", m, pmf);
  };
  fclose (pmf_out);

  pmf_out = fopen ("data4.csv","w");
  for (m=0; m<=14; m++)
  {
    pmf = geometric_pmf (0.25, m);
    fprintf (pmf_out, "%d %.6f\n", m, pmf);
  };
  fclose (pmf_out);

  pmf_out = fopen ("data5.csv","w");
  for (m=0; m<=9; m++)
  {
    pmf = uniform_pmf (n, m);
    fprintf (pmf_out, "%d %.6f\n", m, pmf);
  };
  fclose (pmf_out);

  return 0;
}

