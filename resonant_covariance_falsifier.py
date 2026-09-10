"""Exact resonant falsifier for coefficient-uniform band covariance.

Owner: Kevin's Goldbach research.  Purpose: distinguish the actual fixed
Mobius--log inequality from a tempting but false theorem for arbitrary
coefficients.

THE ACTUAL PROPOSED INEQUALITY.
For an integer N, put

 H=floor(N^(1/10)), B=floor(2*N^(9/1000)),
 M=floor(N^(59/100)), V=floor(N^(3/20)).                  (1)

For every prime M<m<=2M choose an integer interval J_m=(L_m,R_m] satisfying

 N/8<=L_m<R_m<=7*N/8,       R_m-L_m>=N/16.               (2)

For 1<=d<=B with mu(d)^2=1 and (d,m)=1, set q=dm.  Represent h modulo q by
the unique integer h_tilde in (-q/2,q/2], and put

 B_q={h mod q: q/(2*pi*H)<|h_tilde|<q/(pi*H)}.            (3)

Let mbar be the inverse of m modulo d, interpret e_1=1, and define

 K_(d,m,h)(n)=exp(-2*pi*i*h*n/q)
       +(m-1)^(-1) exp(-2*pi*i*h*mbar*n/d),               (4)

 T_mu(d,m,h;J_m)=sum_(a>V,(a,q)=1) mu(a)
     sum_(b>=1, L_m<a*b<=R_m, (b,q)=1) log(b) K_(d,m,h)(a*b). (5)

The exact remaining target is: for every epsilon>0 there are constants
C_epsilon,N_epsilon such that, for all integers N>=N_epsilon and every
interval family (2),

 sum_(1<=d<=B) mu(d)^2
  sum_(M<m<=2M, m prime, (d,m)=1) (log m)^2/(d*m)
   sum_(h in B_(dm)) |T_mu(d,m,h;J_m)|^2
       <= C_epsilon*N^(1499/1000+epsilon).                (6)

This is a conjectural arithmetic inequality.  Equations (1)--(6) specify all
ranges, weights and coefficients.  No formal identity in this repository
proves (6).

AN EXACT RESONANT TEST OF A UNIFORM STRENGTHENING.
Fix an odd prime m and any active h0 in

 I={1<=h<m: m/(2*pi*H)<min(h,m-h)<m/(pi*H)}.

On the separated nonzero-residue box choose

 alpha_a=exp(2*pi*i*h0*a/m),  1<=a<=m-1;   beta_1=1.      (7)

For

 S(h)=sum_(a=1)^(m-1) alpha_a
          [exp(-2*pi*i*h*a/m)+1/(m-1)],                  (8)

geometric summation gives

 S(h0)=m*(m-2)/(m-1),       S(h)=-m/(m-1) for h!=h0.     (9)

Writing R=|I| and E_all=sum_(h=1)^(m-1)|S(h)|^2, exactly

 E_all=m^2*(m-2)/(m-1),
 E_band/E_all=((m-2)^2+R-1)/((m-2)*(m-1)),               (10)
 OFF/E_all=(m-3)*(m-1-R)/((m-2)*(m-1)),                  (11)

where OFF=E_band-R*E_all/(m-1) is precisely the nonprincipal covariance.
If H tends to infinity and H=o(m), (11) tends to one, while
C*(log N)^A/H tends to zero for every fixed C,A.  Thus the coefficient-uniform
version of the proposed H^(-1) covariance estimate is false: resonant
coefficients make the linked conditions reinforce almost maximally.

This does NOT falsify (6).  Its coefficients are the fixed arithmetic values
mu(a)log(b), shared across moduli and constrained by the hard hyperbola.  The
resonant alpha in (7) depends on m and h0 and is not Mobius.  The test proves
that any successful argument for (6) must use that arithmetic structure.
"""

from fractions import Fraction as F

from mobius_band_character_covariance import active_nonzero_modes


def resonant_covariance_receipt(prime, shift_length):
    """Return the exact energy ratios (10)--(11) for the resonance (7)."""
    modes = active_nonzero_modes(prime, shift_length)
    if not modes:
        raise ValueError("the active set must be nonempty")
    r = len(modes)
    full = F(prime * prime * (prime - 2), prime - 1)
    band = F(prime * prime * ((prime - 2) ** 2 + r - 1),
             (prime - 1) ** 2)
    diagonal = F(r, prime - 1) * full
    off = band - diagonal
    return {
        "prime": prime,
        "shift_length": shift_length,
        "active_size": r,
        "resonant_frequency": modes[0],
        "full_energy": full,
        "band_energy": band,
        "diagonal_energy": diagonal,
        "off_diagonal_energy": off,
        "band_over_full": band / full,
        "off_over_full": off / full,
        "closed_band_ratio": F((prime - 2) ** 2 + r - 1,
                               (prime - 2) * (prime - 1)),
        "closed_off_ratio": F((prime - 3) * (prime - 1 - r),
                              (prime - 2) * (prime - 1)),
    }
