# derivation of the formula in gmsh

## Formula for quad elements

Consider a 1D line from $a_0$ to $a_f$ of length $L$, that is $a_f = a_0 + L$. We want to split the segment in $n$ elements using a geometric progression of ratio $p$. We are given this $p$ and let $dx$ be the distance between the last two elements. We want to compute an approximate number of the number of elements $N$ that we need.

Let $a_1$ be the first element in the domain. Thus:

$$
a_0 + (a_1 - a_0) * (1 + p + p^2 + \ldots + p^n) = a_f
$$

Which implies:

$$
(a_1 - a_0) * (1 + p + p^2 + \ldots + p^n) = (a_1 - a_0) (1 - p^{n+1}) / (1 - p) = L
$$

Moreover, we know that $(a_1 - a_0)p^n = dx$. Thus:

$$
dx / p^n = L * (1 - p) / (1 - p^{n+1})
$$

Let $a = p^n$ and $d = dx/L$. Then:

$$
d * (1 - p * a) = (1 - p) * a \implies
a = d / (1 - p + d * p)
$$

Finally:

$$
n = \log (a) / \log (p) = \log (d / (1 - p + d * p)) / \log (p)
$$

## Formula for triangular elements

To determine the first $dx$ based on the one from the quads, we just need $a_1-a_0= L*(1-p)/(1-p^{n+1})$. And then we need to compute $n$ based on the greatest distance, as opposed to the last one (where we were based on the smallest distance between elements). So in this case we have $dx = a_1-a_0$, thus:

$$
dx = L * (1 - p) / (1 - p^{n+1}) \implies
n = \log (1 - (1 - p) / d) / \log (p) - 1
$$
