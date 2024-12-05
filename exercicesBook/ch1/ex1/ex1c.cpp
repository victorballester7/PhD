#include "../../libs/polylib.h"
#include <cmath>
#include <iostream>

using namespace std;

#define f(x) sin(x)

// map from [-1, 1] to [a, b]
double localToGlobal(double xi, double a, double b);

double integrate(int Q, double a, double b);


int main() {
  double a = 0.0;
  double b = M_PI_2;

  double sum = 0.0;

  for (int i = 0; i < 8; i++) {
    sum = integrate(i, a, b);

    cout << "Sum (" << i << ") = " << sum << endl;
  }
}

double localToGlobal(double xi, double a, double b) {
  return 0.5 * (b + a + (b - a) * xi);
}

double integrate(int Q, double a, double b) {
  double sum = 0.0;
  double *w, *z;
  w = new double[Q];
  z = new double[Q];
  polylib::zwgll(z, w, Q);
  for (int j = 0; j < Q; j++){
    cout << "z[" << j << "] = " << z[j] << " w[" << j << "] = " << w[j] << endl;
    sum += w[j] * sin(localToGlobal(z[j], a, b));}
  sum *= (b - a) / 2.0;
  delete[] w;
  delete[] z;
  return sum;
}
