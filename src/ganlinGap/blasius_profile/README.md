# Blasius profile (Crossflow velocity)

This solves the boundary value problem to get a blasius profile for an inflow with a sweep angle in the plane $x-z$.

The equations that define the problem are:

$$
\begin{align}
f''' + ff'' + \beta (1-f'^2) &= 0 \\
g'' + f g' &= 0\\
f(0) &= 0\\
f'(0) &= 0\\
f'(\infty) &= 1\\
g(0) &= 0\\
g(\infty) &= 1\\
\end{align}
$$

where $\beta = \frac{2m}{m+1}$ and $m$ is the parameter such that at the top of the boundary layer the velocity is given by $u \sim U_\infty x^m$.


## Usage

The code is written in Python and uses the `scipy` library to solve the boundary value problem. Check the parameter of $m$ at the top of the script and then run it with:

```python
python solve_bvp.py
```

It will output the coefficients of a polynomial approximation of order 8 (default), that then you can use in nektar session files.

