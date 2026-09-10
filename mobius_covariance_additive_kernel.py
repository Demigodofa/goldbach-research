"""Exact additive kernel for the d=1 Mobius-tail covariance.

Owner: Kevin's Goldbach research.  Purpose: expand the actual shared
Mobius--log coefficient before absolute values and locate any surviving
full-energy diagonal.  The expansion is exact for every hard interval.  It
does not estimate the off-diagonal shifted correlations or the d>1 block.

Let

 r_V(n)=sum_(a|n,a>V) mu(a)log(n/a),
 F_m(x)=sum_(n in J_m,n=x mod m) r_V(n),  1<=x<m.         (1)

The coprimality masks in the d=1 tail are exactly x!=0.  With

 phi_h(x)=e_m(-h*x)+1/(m-1),
 S_m(h)=sum_(x=1)^(m-1) F_m(x)phi_h(x),                  (2)

the hard hyperbola has been retained inside r_V and F_m; no separated-box
factorization is being assumed.

Let I_m be the strict symmetric active band, R=|I_m|, and

 W_m(t)=sum_(h in I_m)e_m(h*t).                           (3)

For nonzero residues x,y, the active-band Gram kernel is

 B_m(x,y)=W_m(y-x)+[W_m(-x)+W_m(y)]/(m-1)+R/(m-1)^2.    (4)

The full nonzero-frequency kernel is exactly

 FUL_m(x,y)=m*1_(x=y)-m/(m-1).                           (5)

Consequently the signed nonprincipal character covariance equals

 OFF_m=sum_(x,y nonzero)F_m(x)conj(F_m(y))D_m(x,y),      (6)
 D_m(x,y)=B_m(x,y)-R/(m-1)*FUL_m(x,y).                  (7)

Equations (4)--(7) are just the character covariance transformed back to
additive residues.  They produce no Kloosterman phase by themselves.

THE LITERAL RESIDUE DIAGONAL CANCELS.
Because I_m is symmetric, W_m(x) is real, and (7) gives

 D_m(x,x)=2*W_m(x)/(m-1)+2*R/(m-1)^2.                   (8)

Moreover

 sum_(x=1)^(m-1)D_m(x,x)=0,                              (9)

since sum_(x nonzero)W_m(x)=-R.  Thus there is no positive
full-energy trace or literal residue diagonal hidden in OFF.  Pointwise,

 |D_m(x,x)|<=2R/(m-1)+2R/(m-1)^2=O(1/H).                (10)

THE MEAN-ZERO FORM REMOVES THE RANK TERMS EXACTLY.
Put

 Fbar_m=(m-1)^(-1)sum_(x=1)^(m-1)F_m(x),
 delta_m(x)=F_m(x)-Fbar_m.                                (11)

Then sum_x delta_m(x)=0, while for every nonzero h

 sum_(x=1)^(m-1)F_m(x)[e_m(-h*x)+1/(m-1)]
       =sum_(x=1)^(m-1)delta_m(x)e_m(-h*x).               (12)

Thus Parseval turns (6) into the especially simple exact identity

 OFF_m=sum_(h in I_m)|delta_hat_m(h)|^2
       -R*m/(m-1)sum_(x=1)^(m-1)|delta_m(x)|^2,           (13)
 delta_hat_m(h)=sum_x delta_m(x)e_m(-h*x).                (14)

Equivalently, OFF is the excess of the actual discrepancy's active-band
energy above the uniform fraction R/(m-1) of its full nonzero-frequency
energy.  The raw W/rank cancellation in the finite diagnostic is therefore
an algebraic mean-removal effect, not new arithmetic cancellation.  In the
mean-zero coordinates the diagonal coefficient in (13) is only
`-R/(m-1)`, and the off-diagonal kernel is W_m(y-x).

The resonant counterexample is therefore necessarily built from x!=y terms.
For x!=y, the leading pair term is W_m(y-x).  It can have size comparable
with R when the cyclic distance |y-x|_m is O(H).  The other terms in (7) are
rank corrections forced by the low projector.  They can be comparable with
the leading pair term and cannot be discarded before signed recombination.

FINITE LAG DIAGNOSTIC.
For the actual U=1 tail at N=200000, H=3, V=6, J=(N/8,7N/8], and all 171
prime m in the finite block, with weight (log m)^2/m, the aggregate OFF was
-3.85508e7.  Its literal residue-diagonal contribution was only -6.44318e2.
But the W_m(y-x) off-diagonal was -1.90631e10 and the centering rank correction
was +1.90245e10.  Within the W term alone, cyclic distances 1..H contributed
+5.59840e10 and distances H+1..2H contributed -7.34683e10.  These floating
figures reproduce the earlier aggregate OFF/character-diagonal ratio
-0.041560, but the tiny cutoff and severe cancellation make them diagnostics,
not asymptotic evidence.

At this tested scale they reject two numerical approximations: dropping the
later lobes, or triangle-bounding the raw W term and low-projector rank
correction.  Equation (13) extracts their exact algebraic cancellation.  It
does not rule out an asymptotic treatment of the remaining mean-zero shifted
correlations.  Taking absolute values before mean removal can restore a much
larger loss than H, and does so in this diagnostic.

DISPOSITION.
The proposed full-energy positive diagonal falsifier is absent.  This is
progress, not the desired estimate: equations (8)--(10) do not control the
full signed off-diagonal, the prime-m average, d>1 CRT, or endpoint transfer.
A valid next theorem must show that the actual shared Mobius--log residue
discrepancy has no positive active-band energy excess beyond the target after
the prime-modulus average.  Formula (13), not the raw rank-term split, is the
narrowest exact d=1 target.
"""

import cmath
from math import pi

from mobius_band_character_covariance import active_nonzero_modes


def additive_band_transform(prime, shift_length, residue):
    """W_m(t) from (3), evaluated directly for finite identity tests."""
    modes = active_nonzero_modes(prime, shift_length)
    return sum(cmath.exp(2j * pi * h * (residue % prime) / prime)
               for h in modes)


def full_centered_kernel(prime, x, y):
    """The exact closed form (5) on nonzero residues."""
    x, y = x % prime, y % prime
    if x == 0 or y == 0:
        raise ValueError("x and y must be nonzero residues")
    return prime * (x == y) - prime / (prime - 1)


def active_centered_kernel(prime, shift_length, x, y):
    """The exact active Gram kernel (4)."""
    x, y = x % prime, y % prime
    if x == 0 or y == 0:
        raise ValueError("x and y must be nonzero residues")
    r = len(active_nonzero_modes(prime, shift_length))
    return (additive_band_transform(prime, shift_length, y - x)
            + additive_band_transform(prime, shift_length, -x) / (prime - 1)
            + additive_band_transform(prime, shift_length, y) / (prime - 1)
            + r / (prime - 1) ** 2)


def off_covariance_kernel(prime, shift_length, x, y):
    """D_m(x,y) in (7)."""
    r = len(active_nonzero_modes(prime, shift_length))
    return (active_centered_kernel(prime, shift_length, x, y)
            - r / (prime - 1) * full_centered_kernel(prime, x, y))


def direct_off_covariance(prime, shift_length, residue_coefficients):
    """Compute OFF from band/full energies for arbitrary nonzero-residue F."""
    coefficients = {x % prime: value for x, value in residue_coefficients.items()}
    if 0 in coefficients:
        raise ValueError("coefficients must be supported on nonzero residues")
    modes = active_nonzero_modes(prime, shift_length)

    def centered_sum(h):
        return sum(value * (cmath.exp(-2j * pi * h * x / prime)
                            + 1 / (prime - 1))
                   for x, value in coefficients.items())

    band = sum(abs(centered_sum(h)) ** 2 for h in modes)
    full = sum(abs(centered_sum(h)) ** 2 for h in range(1, prime))
    return band - len(modes) / (prime - 1) * full


def kernel_off_covariance(prime, shift_length, residue_coefficients):
    """Compute the quadratic form (6) directly."""
    coefficients = {x % prime: value for x, value in residue_coefficients.items()}
    if 0 in coefficients:
        raise ValueError("coefficients must be supported on nonzero residues")
    return sum(value_x * value_y.conjugate()
               * off_covariance_kernel(prime, shift_length, x, y)
               for x, value_x in coefficients.items()
               for y, value_y in coefficients.items())


def off_covariance_decomposition(prime, shift_length, residue_coefficients):
    """Split (6) into literal diagonal, leading W off-diagonal, and rank terms."""
    coefficients = {x % prime: value for x, value in residue_coefficients.items()}
    if 0 in coefficients:
        raise ValueError("coefficients must be supported on nonzero residues")
    total = kernel_off_covariance(prime, shift_length, coefficients)
    diagonal = sum(abs(value) ** 2
                   * off_covariance_kernel(prime, shift_length, x, x)
                   for x, value in coefficients.items())
    leading_off_diagonal = sum(
        value_x * value_y.conjugate()
        * additive_band_transform(prime, shift_length, y - x)
        for x, value_x in coefficients.items()
        for y, value_y in coefficients.items() if x != y
    )
    centering_off_diagonal = total - diagonal - leading_off_diagonal
    return {
        "total": total,
        "literal_diagonal": diagonal,
        "leading_W_off_diagonal": leading_off_diagonal,
        "centering_off_diagonal": centering_off_diagonal,
    }


def mean_zero_off_covariance(prime, shift_length, residue_coefficients):
    """Evaluate the rank-free discrepancy identity (13)."""
    coefficients = {x % prime: value for x, value in residue_coefficients.items()}
    if 0 in coefficients:
        raise ValueError("coefficients must be supported on nonzero residues")
    values = [coefficients.get(x, 0j) for x in range(1, prime)]
    average = sum(values) / (prime - 1)
    discrepancies = [value - average for value in values]
    modes = active_nonzero_modes(prime, shift_length)

    def transform(h):
        return sum(discrepancy * cmath.exp(-2j * pi * h * x / prime)
                   for x, discrepancy in enumerate(discrepancies, start=1))

    band = sum(abs(transform(h)) ** 2 for h in modes)
    parseval_full = prime * sum(abs(value) ** 2 for value in discrepancies)
    return {
        "average": average,
        "discrepancies": tuple(discrepancies),
        "band_energy": band,
        "full_energy": parseval_full,
        "off_diagonal": band - len(modes) / (prime - 1) * parseval_full,
    }
