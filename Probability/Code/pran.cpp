#include <cmath>
#include <cstdio>
#include "fl-ran.h"

int main() {
  int seed;
  int index;
  int samples = 10000;
  int die[6];
  float hist[6];
  unsigned long long int mypseudo;

  printf("Enter seed: ");
  scanf("%d", &seed);
  printf("\n");
  Ran myran(seed);

  for (index = 1; index <= 6; index++)
  { die[index] = 0; };

  for (index = 1; index <= samples; index++)
  {
    mypseudo = 1 + myran.int64() % 6;
    switch (mypseudo) {
      case 1: die[1]++; break;
      case 2: die[2]++; break;
      case 3: die[3]++; break;
      case 4: die[4]++; break;
      case 5: die[5]++; break;
      case 6: die[6]++;
    };
  };

  for (index = 1; index <= 6; index++)
  {
    hist[index] = (float) die[index] / samples;
    printf ("%.3f ", hist[index]);
  };
  printf ("\n");

  return 0;
}
