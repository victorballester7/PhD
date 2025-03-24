#include <cmath>
#include <complex>
#include <eigen3/Eigen/Dense>
#include <eigen3/Eigen/Eigenvalues>
#include <iostream>
#include <vector>

// Define complex type for easier use
using namespace std;
using Complex = std::complex<double>;
using ComplexMatrix = Eigen::MatrixXcd;
using ComplexVector = Eigen::VectorXcd;

class Ufield {
public:
  virtual void getU(vector<double> y, vector<double> U) = 0;
  virtual void getd2U(vector<double> y, vector<double> d2U) = 0;
};

class Poiseuille : public Ufield {
private:
  double L; // Half-width of channel
public:
  Poiseuille(double L) : L(L) {}

  void getU(vector<double> y, vector<double> U) override {
    for (double yi : y) {
      U.push_back(1.0 - yi * yi / (L * L));
    }
  }

  void getd2U(vector<double> y, vector<double> d2U) override {
    for (double yi : y) {
      d2U.push_back(-2.0 / (L * L));
    }
  }
};

class OrrSommerfeldSolver {
private:
  // Parameters
  double Re;    // Reynolds number
  double alpha; // Wavenumber
  int N;        // Number of elements
  int p;        // max polynomial order of the finite element basis
  double a;     // Left boundary of domain
  double b;     // Right boundary of domain

  // Computational variables
  std::vector<double> nodes;             // Discretization nodes
  std::vector<double> weights;           // Gauss-Hermite quadrature weights
  std::vector<double> quadrature_points; // Gauss-Hermite quadrature points
  ComplexMatrix A;            // Matrix A for generalized eigenvalue problem
  ComplexMatrix B;            // Matrix B for generalized eigenvalue problem
  ComplexVector eigenvalues;  // Calculated eigenvalues
  ComplexMatrix eigenvectors; // Calculated eigenvectors

public:
  OrrSommerfeldSolver(double reynolds_number, double wavenumber,
                      int num_elements, int poly_order, double left_boundary,
                      double right_boundary)
      : Re(reynolds_number), alpha(wavenumber), N(num_elements), p(poly_order),
        a(left_boundary), b(right_boundary) {
    // Initialize matrices with appropriate size
    // Each element has 4 DOFs (value and derivative at each end)
    int matrix_size = 2 * (N + 1);
    A = ComplexMatrix::Zero(matrix_size, matrix_size);
    B = ComplexMatrix::Zero(matrix_size, matrix_size);

    // Create discretization nodes (element boundaries)
    generateNodes();

    // Initialize quadrature rule for numerical integration
    initializeQuadrature();
  }

  // Generate equally spaced nodes for now (could be improved with mesh
  // refinement)
  void generateNodes() {
    nodes.resize(N + 1);
    double h = 2.0 * L / N; // Element size

    for (int i = 0; i <= N; ++i) {
      nodes[i] = -L + i * h;
    }
  }

  // Initialize Gauss-Hermite quadrature for numerical integration
  // void initializeQuadrature() {
  //     // Use 10-point Gauss-Hermite quadrature
  //     int n_quad = 10;
  //     quadrature_points.resize(n_quad);
  //     weights.resize(n_quad);
  //
  //     // Hardcoded values for 10-point Gauss-Hermite quadrature
  //     // These values are for the standard Hermite weight function e^(-x^2)
  //     quadrature_points = {-3.436159118837738, -2.532731674232790,
  //     -1.756683649299882,
  //                          -1.036610829789514, -0.342901327223705,
  //                          0.342901327223705,
  //                          1.036610829789514, 1.756683649299882, 2.532731674232790,
  //                          3.436159118837738};
  //
  //     weights = {7.64043285523262e-06, 0.00134364574678124,
  //     0.0338743944554810,
  //                0.240138611082314, 0.610862633735326, 0.610862633735326,
  //                0.240138611082314, 0.0338743944554810,
  //                0.00134364574678124, 7.64043285523262e-06};
  //
  //     // Scale weights for the interval transformation
  //     for (int i = 0; i < n_quad; ++i) {
  //         weights[i] *= std::exp(quadrature_points[i] *
  //         quadrature_points[i]);
  //     }
  // }

  // // Hermite basis functions (cubic Hermite interpolation polynomials)
  // double h1(double xi) { return (1 + 2*xi) * (1 - xi) * (1 - xi); }
  // double h2(double xi) { return xi * (1 - xi) * (1 - xi); }
  // double h3(double xi) { return xi * xi * (3 - 2*xi); }
  // double h4(double xi) { return xi * xi * (xi - 1); }
  //
  // // Derivatives of Hermite basis functions
  // double dh1(double xi) { return 6 * xi * xi - 6 * xi; }
  // double dh2(double xi) { return (1 - xi) * (1 - xi) - 2 * xi * (1 - xi); }
  // double dh3(double xi) { return 6 * xi - 6 * xi * xi; }
  // double dh4(double xi) { return 3 * xi * xi - 2 * xi; }
  //
  // // Second derivatives of Hermite basis functions
  // double d2h1(double xi) { return 12 * xi - 6; }
  // double d2h2(double xi) { return -4 + 6 * xi; }
  // double d2h3(double xi) { return 6 - 12 * xi; }
  // double d2h4(double xi) { return 6 * xi - 2; }
  //
  // // Fourth derivatives of Hermite basis functions (constant for cubic
  // Hermite) double d4h1(double xi) { return 0; } double d4h2(double xi) {
  // return 0; } double d4h3(double xi) { return 0; } double d4h4(double xi) {
  // return 0; }
  //
  // // Base flow (plane Poiseuille flow: U(y) = 1-y^2)
  // double baseFlow(double y) {
  //     return 1.0 - y * y / (L * L);
  // }
  //
  // // First derivative of base flow
  // double baseFlowDerivative(double y) {
  //     return -2.0 * y / (L * L);
  // }

  // // Second derivative of base flow
  // double baseFlowSecondDerivative(double y) {
  //     return -2.0 / (L * L);
  // }
  //
  // // Assemble the finite element matrices
  // void assembleMatrices() {
  //     A = ComplexMatrix::Zero(2*(N+1), 2*(N+1));
  //     B = ComplexMatrix::Zero(2*(N+1), 2*(N+1));
  //
  //     // For each element
  //     for (int e = 0; e < N; ++e) {
  //         double y1 = nodes[e];    // Left node
  //         double y2 = nodes[e+1];  // Right node
  //         double he = y2 - y1;     // Element size
  //
  //         // Element matrices
  //         ComplexMatrix Ae = ComplexMatrix::Zero(4, 4);
  //         ComplexMatrix Be = ComplexMatrix::Zero(4, 4);
  //
  //         // Perform numerical integration using Gauss-Hermite quadrature
  //         for (int q = 0; q < quadrature_points.size(); ++q) {
  //             // Transform quadrature point to element
  //             double xi = (quadrature_points[q] + 1.0) / 2.0;  // Map from
  //             [-1,1] to [0,1] double y = y1 + xi * he;  // Map to physical
  //             coordinate double w = weights[q] * he / 2.0;  // Scale weight
  //             by Jacobian
  //
  //             // Base flow and derivatives at quadrature point
  //             double U = baseFlow(y);
  //             double dU = baseFlowDerivative(y);
  //             double d2U = baseFlowSecondDerivative(y);
  //
  //             // Basis functions and derivatives at quadrature point
  //             std::vector<double> phi = {h1(xi), h2(xi), h3(xi), h4(xi)};
  //             std::vector<double> dphi = {dh1(xi) / he, dh2(xi) / he, dh3(xi)
  //             / he, dh4(xi) / he}; std::vector<double> d2phi = {d2h1(xi) /
  //             (he*he), d2h2(xi) / (he*he),
  //                                        d2h3(xi) / (he*he), d2h4(xi) /
  //                                        (he*he)};
  //             std::vector<double> d4phi = {d4h1(xi) / std::pow(he, 4),
  //             d4h2(xi) / std::pow(he, 4),
  //                                        d4h3(xi) / std::pow(he, 4), d4h4(xi)
  //                                        / std::pow(he, 4)};
  //
  //             // Assemble element matrices
  //             for (int i = 0; i < 4; ++i) {
  //                 for (int j = 0; j < 4; ++j) {
  //                     // Orr-Sommerfeld operators
  //                     // A matrix: (1/Re)*(D^2-alpha^2)^2 -
  //                     i*alpha*U*(D^2-alpha^2) - i*alpha*d2U Complex term1 =
  //                     (1.0/Re) * ((d2phi[i] - alpha*alpha*phi[i]) * (d2phi[j]
  //                     - alpha*alpha*phi[j])); Complex term2 = Complex(0,
  //                     -alpha) * U * ((d2phi[i] - alpha*alpha*phi[i]) *
  //                     phi[j]); Complex term3 = Complex(0, -alpha) * d2U *
  //                     (phi[i] * phi[j]);
  //
  //                     Ae(i, j) += w * (term1 + term2 + term3);
  //
  //                     // B matrix: (D^2-alpha^2)
  //                     Be(i, j) += w * (phi[i] * phi[j]);
  //                 }
  //             }
  //         }
  //
  //         // Assemble element matrices into global matrices
  //         int idx1 = 2 * e;      // Global index for left node
  //         int idx2 = 2 * (e+1);  // Global index for right node
  //
  //         // Map element DOFs to global DOFs
  //         std::vector<int> global_dofs = {idx1, idx1+1, idx2, idx2+1};
  //
  //         // Add element contributions to global matrices
  //         for (int i = 0; i < 4; ++i) {
  //             for (int j = 0; j < 4; ++j) {
  //                 A(global_dofs[i], global_dofs[j]) += Ae(i, j);
  //                 B(global_dofs[i], global_dofs[j]) += Be(i, j);
  //             }
  //         }
  //     }
  //
  //     // Apply boundary conditions (homogeneous Dirichlet and Neumann at y =
  //     ±L)
  //     // We need to enforce phi(-L) = phi'(-L) = phi(L) = phi'(L) = 0
  //
  //     // Enforce boundary conditions by modifying first and last rows/columns
  //     int last_idx = 2 * (N + 1) - 1;
  //
  //     // Zero out rows and columns for boundary DOFs
  //     for (int i = 0; i < 2*(N+1); ++i) {
  //         A(0, i) = A(1, i) = A(last_idx-1, i) = A(last_idx, i) = 0;
  //         A(i, 0) = A(i, 1) = A(i, last_idx-1) = A(i, last_idx) = 0;
  //
  //         B(0, i) = B(1, i) = B(last_idx-1, i) = B(last_idx, i) = 0;
  //         B(i, 0) = B(i, 1) = B(i, last_idx-1) = B(i, last_idx) = 0;
  //     }
  //
  //     // Set diagonal entries to 1 for boundary DOFs
  //     A(0, 0) = A(1, 1) = A(last_idx-1, last_idx-1) = A(last_idx, last_idx)
  //     = 1.0; B(0, 0) = B(1, 1) = B(last_idx-1, last_idx-1) = B(last_idx,
  //     last_idx) = 1.0;
  // }

  // Solve the eigenvalue problem
  void solve() {
    // Assemble matrices
    assembleMatrices();

    // Solve generalized eigenvalue problem: A*v = lambda*B*v
    Eigen::GeneralizedEigenSolver<ComplexMatrix> ges;
    ges.compute(A, B);

    // Extract eigenvalues and eigenvectors
    eigenvalues = ges.eigenvalues();
    eigenvectors = ges.eigenvectors();

    // Sort eigenvalues by imaginary part (growth rate)
    std::vector<std::pair<int, double>> idx_imag;
    for (int i = 0; i < eigenvalues.size(); ++i) {
      idx_imag.push_back({i, eigenvalues(i).imag()});
    }

    std::sort(
        idx_imag.begin(), idx_imag.end(),
        [](const std::pair<int, double> &a, const std::pair<int, double> &b) {
          return a.second > b.second;
        });
  }

  // Print the most unstable eigenvalues (largest imaginary part)
  void printResults(int num_values = 5) {
    std::cout << "Most unstable eigenvalues:" << std::endl;
    std::cout << "Re = " << Re << ", alpha = " << alpha << std::endl;
    std::cout << "----------------------------------------" << std::endl;
    std::cout << "   Real part      |   Imaginary part   " << std::endl;
    std::cout << "----------------------------------------" << std::endl;

    // Sort eigenvalues by imaginary part
    std::vector<std::pair<int, double>> idx_imag;
    for (int i = 0; i < eigenvalues.size(); ++i) {
      // Skip eigenvalues with very large magnitude (numerical artifacts)
      if (std::abs(eigenvalues(i)) < 1e6) {
        idx_imag.push_back({i, eigenvalues(i).imag()});
      }
    }

    std::sort(
        idx_imag.begin(), idx_imag.end(),
        [](const std::pair<int, double> &a, const std::pair<int, double> &b) {
          return a.second > b.second;
        });

    int count = std::min(num_values, static_cast<int>(idx_imag.size()));
    for (int i = 0; i < count; ++i) {
      int idx = idx_imag[i].first;
      std::cout << std::setw(15) << eigenvalues(idx).real() << " | "
                << std::setw(15) << eigenvalues(idx).imag() << std::endl;
    }
    std::cout << "----------------------------------------" << std::endl;
  }

  // Evaluate eigenfunction for a specific eigenvalue
  // ComplexVector getEigenfunction(int eigen_idx, int num_points = 100) {
  //     ComplexVector result(num_points);
  //     double dy = 2.0 * L / (num_points - 1);
  //
  //     for (int i = 0; i < num_points; ++i) {
  //         double y = -L + i * dy;
  //
  //         // Find which element contains this point
  //         int elem_idx = -1;
  //         for (int e = 0; e < N; ++e) {
  //             if (y >= nodes[e] && y <= nodes[e+1]) {
  //                 elem_idx = e;
  //                 break;
  //             }
  //         }
  //
  //         if (elem_idx == -1) continue;  // Skip if point is outside domain
  //
  //         // Local coordinate within element
  //         double he = nodes[elem_idx+1] - nodes[elem_idx];
  //         double xi = (y - nodes[elem_idx]) / he;
  //
  //         // Evaluate basis functions
  //         double phi1 = h1(xi);
  //         double phi2 = h2(xi);
  //         double phi3 = h3(xi);
  //         double phi4 = h4(xi);
  //
  //         // Get global DOF indices
  //         int idx1 = 2 * elem_idx;
  //         int idx2 = 2 * (elem_idx + 1);
  //
  //         // Interpolate eigenfunction
  //         result(i) = eigenvectors(idx1, eigen_idx) * phi1 +
  //                    eigenvectors(idx1+1, eigen_idx) * phi2 +
  //                    eigenvectors(idx2, eigen_idx) * phi3 +
  //                    eigenvectors(idx2+1, eigen_idx) * phi4;
  //     }
  //
  //     return result;
  // }

  // Save eigenfunction to file
  // void saveEigenfunction(int eigen_idx, const std::string& filename) {
  //     int num_points = 100;
  //     ComplexVector eigenfunction = getEigenfunction(eigen_idx, num_points);
  //
  //     std::ofstream file(filename);
  //     if (!file.is_open()) {
  //         std::cerr << "Error opening file: " << filename << std::endl;
  //         return;
  //     }
  //
  //     file << "# y-coordinate, Re(phi), Im(phi), |phi|" << std::endl;
  //     double dy = 2.0 * L / (num_points - 1);
  //
  //     for (int i = 0; i < num_points; ++i) {
  //         double y = -L + i * dy;
  //         file << y << " "
  //              << eigenfunction(i).real() << " "
  //              << eigenfunction(i).imag() << " "
  //              << std::abs(eigenfunction(i)) << std::endl;
  //     }
  //
  //     file.close();
  //     std::cout << "Eigenfunction saved to " << filename << std::endl;
  // }
};

int main() {
  // Set parameters
  double Re = 10000;  // Reynolds number
  double alpha = 1.0; // Wavenumber
  int N = 20;         // Number of elements
  int p = 3;          // Cubic Hermite polynomials

  std::cout << "Solving Orr-Sommerfeld equation for plane Poiseuille flow"
            << std::endl;
  std::cout << "Parameters: Re = " << Re << ", alpha = " << alpha << std::endl;
  std::cout << "Discretization: " << N
            << " elements with cubic Hermite interpolation" << std::endl;

  // Create solver and solve
  OrrSommerfeldSolver solver(Re, alpha, N, p);
  solver.solve();
  solver.printResults(10);

  // Save most unstable eigenfunction
  solver.saveEigenfunction(0, "eigenfunction.dat");

  // Try different Reynolds numbers
  std::cout << "\nTesting critical Reynolds numbers:" << std::endl;
  for (double test_Re : {5772.0, 7500.0, 10000.0}) {
    OrrSommerfeldSolver test_solver(test_Re, alpha, N, p);
    test_solver.solve();
    std::cout << "\nResults for Re = " << test_Re << ":" << std::endl;
    test_solver.printResults(3);
  }

  return 0;
}
