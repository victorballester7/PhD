# Notes on linear stability course

### Squire's theorem. 

Consider a 3D parallel viscous flow of the form $(U(y),0,0)$. Given $Re_L$ as the critical Reynolds number for the onset of linear instability for a given wavenumbers $\alpha$ (in $x$ direction) and $\beta$ (in $z$ direction), the Reynolds number $\Re_c$ below which no exponential instabilities exist for any wave number satisfies

$$
\Re_c = \min_{\alpha,\beta} \Re_L(\alpha,\beta) = \min_{\alpha} \Re_L(\alpha,0)
$$

_Remark_: The most unstable linear instability is always 2D.

_Remark_: Viscosity can destabilize the flow (TS waves). For example, in parallel inviscid flows, Rayleigh inflection theorem tells as that if there exists a perturbation that generates linear instability then, $d^2U/dy^2$ must change sign (i.e. must have a zero). However, in the presence of viscosity, the flow can be linearly unstable even if $d^2U/dy^2$ does not change sign (example in Poiseuille flow, with $U(y) = 1-y^2$).

_Remark_: Usually the modes $\alpha$ and $\beta$ that generate the instability are low, because as they tend to infinity, the effect in the viscous term becomes more and more important, so instabilities are wiped out (think in Fourier transform).
