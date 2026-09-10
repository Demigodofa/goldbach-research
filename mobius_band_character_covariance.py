"""Exact character covariance behind the d=1 Mobius-tail band energy.

Owner: Kevin's Goldbach research.  Purpose: identify the mechanism that could
make the linked product and active-frequency conditions cancel or reinforce.
This is an exact finite-field reduction on a separated product box.  It is not
an estimate for the hard hyperbolic interval, the d>1 CRT component, or the
Goldbach correlation.

1. THE CLEAN REMAINDER AND THE MODEL BOX.
The U=1, V=N^(3/20) split in ``prime_band_vaughan_type_i.py`` leaves

 T_mu(h)=sum_(a>V)mu(a) sum_b log(b) 1_(ab in J_m)
          [e_m(-hab)+(m-1)^(-1)]                            (1)

in the d=1 block; all variables are nonzero modulo the prime m.  First retain
a separated rectangle Aset x Bset on which the product mask is identically
one.  Give it arbitrary coefficients alpha_a,beta_b and put

 A(chi)=sum_a alpha_a chi(a), B(chi)=sum_b beta_b chi(b).   (2)

The actual box has alpha=mu and beta=log.  Hard product endpoints prevent an
automatic factorization (2); a later transfer must keep them.

2. EXACT GAUSS EXPANSION.
For every h not divisible by m, character orthogonality gives

 e_m(-h*x)+(m-1)^(-1)
   =(m-1)^(-1) sum_(chi nonprincipal)
                   G_m(conj(chi),-h) chi(x),                (3)

where G_m(conj(chi),c)=sum_(r=1)^(m-1)conj(chi(r))e_m(c*r).
The omitted principal term is exactly the low-projector correction, not an
estimated main term.  Write

 u_chi=m^(-1/2)G_m(conj(chi),-1), |u_chi|=1,
 z_chi=A(chi)B(chi).

Since G_m(conj(chi),-h)=chi(h)G_m(conj(chi),-1), (3) yields

 S(h)=sqrt(m)/(m-1) sum_(chi nonprincipal)u_chi z_chi chi(h). (4)

This reintroduces characters only after the exact full-minus-low collapse and
the Mobius factorization.  It does not reverse the earlier conclusion that
character orthogonality alone supplied no saving.

3. THE BAND DIAGONAL AND THE SINGLE OPEN COVARIANCE.
Let I_m be exactly the symmetric active set

 I_m={1<=h<m: m/(2*pi*H)<min(h,m-h)<m/(pi*H)}, R_m=|I_m|. (5)

For a multiplicative character eta put W_m(eta)=sum_(h in I_m)eta(h).
Extend c_chi=u_chi*z_chi by c_principal=0, and define its character-group
autocorrelation

 C_m(eta)=sum_chi c_(eta*chi) conjugate(c_chi).             (6)

Expanding (4) gives the exact identity

 sum_(h in I_m)|S(h)|^2
  =m/(m-1)^2 sum_eta W_m(eta) C_m(eta).                    (7)

For eta principal, W_m(1)=R_m and C_m(1)=sum|z_chi|^2.  Hence

 DIAG_m=m*R_m/(m-1)^2 sum_(chi nonprincipal)|A(chi)B(chi)|^2. (8)

As R_m=m/(pi*H)+O(1), this is exactly an H^-1 fraction of the corresponding
full-character energy.  It is the desired scale, not an obstruction.

All reinforcement or extra cancellation is in

 OFF_m=m/(m-1)^2 sum_(eta nonprincipal)W_m(eta)C_m(eta).   (9)

Thus one concrete sufficient model-box question is

 |sum_(M<m<=2M prime) (log m)^2/m * OFF_m|
  <= L^C/H * sum_(M<m<=2M prime)(log m)^2/m
       *[m/(m-1) sum_(chi nonprincipal)|A_m(chi)B_m(chi)|^2]. (10)

The modulus sum in (10) is signed before its absolute value.  Taking absolute
values separately would discard the proposed mechanism.  The actual theorem
also needs a uniform hard-product endpoint transfer and the d<=B CRT factor.

4. WHY STANDARD NORM BOUNDS STOP SHORT.
Character orthogonality gives, exactly,

 sum_eta |W_m(eta)|^2=(m-1)R_m,
 sum_(eta nonprincipal)|W_m(eta)|^2=(m-1)R_m-R_m^2.        (11)

Cauchy therefore treats the W and C phases as adversarial.  It cannot produce
the R_m/m=H^-1 factor in (9) without an additional decorrelation statement.
Arbitrary character coefficients can make (4) concentrate entirely on I_m,
just as the earlier additive chirp did.  What could save (10) is specific:
the actual c_chi is a product of the Mobius interval transform A(chi), the
logarithmic interval transform B(chi), and a Gauss phase, while W_m is the
transform of one short additive interval.  The needed input is cancellation
between these two linked transforms, possibly after averaging prime m.  Their
individual L2 norms or a pointwise character bound do not assert it.

5. FINITE FALSIFICATION ATTEMPT.
A direct double-precision probe used the exact U=1 Mobius tail on
J=(N/8,7N/8].  At N=200000, H=3, V=6, all 171 primes M<m<=2M and d=1,2,
the weighted band/all nonprincipal energy ratio was 0.104735, compared with
1/(pi*H)=0.106103.  For d=1 alone it was 0.101751; individual modulus ratios
ranged from 0.071323 to 0.133157.  A second d=1 sample at N=1200000, H=4,
U=V=2 for the preceding balanced tail gave 0.078225 versus 0.079577.

These are measured shape checks, not asymptotic evidence: the feasible
cutoffs are tiny, floating FFTs were used, and the second run sampled only
120 of 444 prime moduli.  They falsified the quick prediction of a visible
near-total resonance, but cannot establish (10) or a power saving.  The exact
identity (7)--(10), rather than the numerical ratios, is the retained result.
"""

import cmath
from math import gcd, pi, sqrt


def _prime(value):
    return (type(value) is int and value >= 2
            and all(value % p for p in range(2, int(sqrt(value)) + 1)))


def primitive_root(prime):
    """Smallest primitive root of an odd prime, for finite exact-shape tests."""
    if not _prime(prime) or prime == 2:
        raise ValueError("odd prime required")
    factors, n, p = set(), prime - 1, 2
    remainder = n
    while p * p <= remainder:
        if remainder % p == 0:
            factors.add(p)
            while remainder % p == 0:
                remainder //= p
        p += 1
    if remainder > 1:
        factors.add(remainder)
    for root in range(2, prime):
        if all(pow(root, n // factor, prime) != 1 for factor in factors):
            return root
    raise AssertionError("primitive root not found")


def character_table(prime):
    """Rows chi_k(x), k=0..m-2 and x=0..m-1, using one primitive root."""
    root = primitive_root(prime)
    logs = [None] * prime
    value = 1
    for exponent in range(prime - 1):
        logs[value] = exponent
        value = value * root % prime
    table = []
    for k in range(prime - 1):
        row = [0j]
        row.extend(cmath.exp(2j * pi * k * logs[x] / (prime - 1))
                   for x in range(1, prime))
        table.append(tuple(row))
    return tuple(table)


def active_nonzero_modes(prime, shift_length):
    if not _prime(prime) or type(shift_length) is not int or shift_length < 2:
        raise ValueError("prime modulus and integer H>=2 required")
    return tuple(h for h in range(1, prime)
                 if prime / (2 * pi * shift_length) < min(h, prime - h)
                 < prime / (pi * shift_length))


def direct_box_sum(prime, frequency, alpha, beta):
    """Direct left side of (3) summed over a separated residue box."""
    if not _prime(prime) or not 0 < frequency < prime:
        raise ValueError("prime modulus and nonzero reduced frequency required")
    total = 0j
    for a, avalue in alpha.items():
        for b, bvalue in beta.items():
            if gcd(a * b, prime) != 1:
                raise ValueError("box coordinates must be units modulo the prime")
            total += avalue * bvalue * (
                cmath.exp(-2j * pi * frequency * a * b / prime)
                + 1 / (prime - 1)
            )
    return total


def character_box_sum(prime, frequency, alpha, beta):
    """Right side of (4), with all Gauss phases computed directly."""
    table = character_table(prime)
    total = 0j
    for k in range(1, prime - 1):
        chi = table[k]
        atransform = sum(value * chi[a % prime] for a, value in alpha.items())
        btransform = sum(value * chi[b % prime] for b, value in beta.items())
        gauss = sum(chi[r].conjugate()
                    * cmath.exp(-2j * pi * frequency * r / prime)
                    for r in range(1, prime))
        total += gauss * atransform * btransform
    return total / (prime - 1)


def character_covariance_receipt(prime, shift_length, alpha, beta):
    """Numerically evaluate (7), splitting its exact diagonal and off-diagonal."""
    table = character_table(prime)
    modes = active_nonzero_modes(prime, shift_length)
    z, unit = [], []
    for k in range(prime - 1):
        chi = table[k]
        atransform = sum(value * chi[a % prime] for a, value in alpha.items())
        btransform = sum(value * chi[b % prime] for b, value in beta.items())
        gauss_minus_one = sum(chi[r].conjugate()
                              * cmath.exp(-2j * pi * r / prime)
                              for r in range(1, prime))
        z.append(atransform * btransform)
        unit.append(gauss_minus_one / sqrt(prime) if k else 0j)
    c = [unit[k] * z[k] if k else 0j for k in range(prime - 1)]
    diagonal = prime * len(modes) / (prime - 1) ** 2 * sum(abs(z[k]) ** 2
                                                           for k in range(1, prime - 1))
    direct_energy = sum(abs(direct_box_sum(prime, h, alpha, beta)) ** 2 for h in modes)
    # Multiplication of character indices corresponds to addition modulo m-1.
    weighted_covariance = 0j
    for eta in range(prime - 1):
        w = sum(table[eta][h] for h in modes)
        covariance = sum(c[(eta + k) % (prime - 1)] * c[k].conjugate()
                         for k in range(prime - 1))
        weighted_covariance += w * covariance
    covariance_energy = prime / (prime - 1) ** 2 * weighted_covariance
    return {
        "band_size": len(modes),
        "direct_energy": direct_energy,
        "covariance_energy": covariance_energy,
        "diagonal": diagonal,
        "off_diagonal": covariance_energy - diagonal,
    }
