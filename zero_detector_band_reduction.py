"""Remove nondetected actual zeros from the localized comparable band.

Owner: Kevin's Goldbach research. Purpose: retain an arithmetic condition
on every zero in the unresolved paired sum, beyond density and smooth-phase
tests. This imports only unconditional classical zero detection, not the
source paper's hypothesis about finitely many vertical lines.

1. THE ACTUAL DETECTOR AND THE REDUCED BAND.
Keep N as the target, T=N^(9/10), L=logN, fixed real smooth chi
supported in(1,2), and the actual finite-period kernel J_N. Every sum
is over ACTUAL positive-height zeta-zero copies rho=beta+i*gamma.
For B=2*T^(1/100) and Y=sqrtT define
 a_T(n)=sum_(d|n,d<=B)mu(d),
 D_M(s)=sum_(M<n<=2M) a_T(n)*exp(-n/Y)*n^(-s),                 (1)
where M ranges over the DYADIC numbers in
 T^(1/100)<=M<=T^(1/2)*(logT)^2.                               (2)
Say a zero is detected if at least one of these polynomials satisfies
 |D_M(rho)|>=1/(3logT).                                       (3)
The coefficients and allowed lengths depend on T but not on the zero.
The chosen length can differ between zeros. These are the source's
zero-detection Type I objects, not Vaughan Type I prime sums.

Let a=16/25, b=19/25, and let V be the list of zero copies with
 a<beta<b AND condition(3).
Then, for every fixed A>0,
 sum_(rho,sigma) chi(gamma/T)*chi(eta/T)*J_N(rho,sigma)
 =sum_(rho,sigma in V) chi(gamma/T)*chi(eta/T)*J_N(rho,sigma)
                                            +O_A(N/L^A).     (4)
The remaining sum stays O(N) by the earlier full-band theorem and(4).
No o(N) estimate, sufficient signed lower margin, or prime-pair coverage
is proved for it. This is one fixed smooth comparable height band.

2. PRIMARY SOURCE AND A PRINTED GAMMA SIGN CORRECTION.
Checked2026-09-09: Maynard--Pratt, Half-isolated zeros and zero-density
estimates, arXiv2206.11729v2,29May2023,39pages:
 https://arxiv.org/pdf/2206.11729v2
PDF SHA256 e6407c953c4ddcbf9daa2fa941d1a84bf9db90f19a96e50ee8796bf9aea5947a.
Notation p6 says n~M means M<n<=2M. Definition17/equations(15)-(16)
p14 give(1); Definition22 and Lemmas23-24 p16 give the two detector
types and their count; Appendix C pp36-38 supplies unconditional proofs.
The later Hypothesis F, clusters on fixed vertical lines, and conditional
main theorems are NOT used. Guth--Maynard2405.20552v2 Section13.1
pp48-49 independently uses this same classical detector setup.

Write the source mollifier as
 M_T(s)=sum_(d<=B)mu(d)*d^(-s).
Its Type II condition is that the absolute value of
 (1/(2pi*i))*int_(Re z=1/2-beta)
     Y^z*Gamma(z)*M_T(rho+z)*zeta(rho+z) dz                     (5)
is at least1/3. Lemma23 says every relevant zero is Type I or Type II,
possibly BOTH. It suffices here that beta lies in[a,b], which is inside
the Appendix C proof's beta>=1/2+1/logT range for sufficiently large T.

The printed pp37-38 substitute Gamma(beta-1/2+i*u) in the proof of
Lemma24, although the contour in(5) gives Gamma(1/2-beta+i*u).
This discrepancy was confirmed in the rendered original PDF, not just
text extraction. We retain the correct negative real part. Set
 delta=beta-1/2 in[7/50,13/50]. The recurrence gives
 Gamma(-delta+i*u)=Gamma(1-delta+i*u)/(-delta+i*u),
 |Gamma(-delta+i*u)|<=Gamma(1-delta)/delta=O(1).                (6)
The numerator inequality follows from the absolutely convergent Euler
integral with positive real part1-delta. Stirling also gives uniform
exponential decay at large |u|. Thus the source proof's needed Gamma
majorant remains valid on this fixed real-part interval. We do not use
its erroneous signed argument or assert that the two Gamma values agree.

3. THE UNCONDITIONAL RESTRICTED TYPE II COUNT, WITH COPIES.
Let R_II(s,T) count Type II zero copies with s<=beta<=b and
gamma in[T,2T], for a<=s<=b. Repeating the source proof with(6) gives
 R_II(s,T)<<T^(2*(1-s))*(logT)^C0                              (7)
uniformly in this interval, for some fixed absolute C0. Here are the
inputs and uniformity details; no fixed power T^epsilon is substituted.

In(5) set z=1/2-beta+i*u. Truncate |u|<=(logT)^2 using exponential
Gamma decay and polynomial bounds for the zeta and mollifier factors.
The omitted tail is negligible uniformly in beta in[a,b]. Even keeping
the source's weaker O(logT) Gamma majorant, a Type II zero satisfies
 T^(s/2-1/4)/logT
  <<int_(|u|<=(logT)^2) |M_T(1/2+i*(gamma+u))*zeta(1/2+i*(gamma+u))|du.
The fourth power and Holder give a lower bound
 T^(2s-1)/(logT)^10
  <<int_(|u|<=(logT)^2) |M_T*zeta|^4(1/2+i*(gamma+u))du.       (8)
All constants are uniform on[a,b]. Choose a (logT)^3-separated
sublist of ordinates. The actual local O(logT) copy count bounds
each removed neighborhood by O((logT)^4) copies, so this extraction
loses at most that logarithmic factor, even with coincident zeros.
The retained integration intervals are disjoint for sufficiently large T.

Appendix C p38 explicitly invokes the classical mollified fourth-moment
bound, for THIS mollifier of length2*T^(1/100),
 int_(T/2)^(3T) |M_T(1/2+i*t)*zeta(1/2+i*t)|^4 dt
                                      <<T*(logT)^C1.          (9)
This is the source's log-power bound from the twisted fourth moment,
not its separate Watt bound with an epsilon loss. It is independent of
Hypothesis F. Combining(8)-(9) and the copy extraction proves(7),
after increasing the fixed log exponent. If the source's original
notation were read as counting distinct locations, this argument still
counts copies explicitly. No simplicity or spacing assumption remains.

For completeness, the dichotomy itself comes from the smoothed series
 sum_(n>=1) a_T(n)*n^(-rho)*exp(-n/Y).
Here a_T(1)=1, a_T(n)=0 for2<=n<=B, and |a_T(n)|<=tau(n).
Mellin inversion and shifting from Re z=2 to1/2-beta cross the zeta
pole at1-rho, exponentially small, and the Gamma pole at0 is canceled
by the ACTUAL zero zeta(rho)=0. The dyadic expansion therefore equals
1+sum_M D_M(rho)+O(T^-1/2)=(5).
There are fewer than logT allowed dyadic blocks eventually. If every
|D_M|<1/(3logT), the magnitude of the right side exceeds1/3 for
sufficiently large T. This proves the implication needed here. The
argument cannot be assigned to an arbitrary artificial frequency list.

4. NONDETECTED COLUMNS HAVE A POWER-SMALL COEFFICIENT ENERGY.
Let U be the disjoint complement of the detected zeros within a<beta<b.
The dichotomy gives U subset Type II; we do not subtract the potentially
overlapping source classes. With the SAME actual coefficient normalization
as zero_packet_realpart_localization.py, put
 E_U=sum_(rho in U)|chi(gamma/T)|^2*N^(2beta-2).
Positive layer cake, including its lower boundary term, gives
 E_U << N^(2a-2)*R_II(a,T)
       +2L*int_a^b N^(2s-2)*R_II(s,T) ds.                    (10)
The count on the right can include additional Type II zeros; this is
only an upper bound. With u=1-s in[6/25,9/25], the N exponent is
 (9/10)*2u-2u=-u/5<=-6/125.
Consequently
 E_U<<N^(-6/125)*L^(C0+1).                                    (11)
The boundary at a has the stronger exponent -9/125. All real parts
and multiplicities are retained. No RH or numerical zero input is used.

Let Z=S_T(aN)/sqrtN be the FULL actual field, whose arithmetic L2
energy on the central interval is O(1). The previously proved masked
Gram estimate gives ||theta*Z_U||_2^2<<L*E_U. Use the arithmetic
energy only for the full other factor. Column, row and intersection
are bounded respectively by sqrt(L E_U), sqrt(L E_U), and L E_U.
The exact beta transfer and the absolutely paid finite-period errors
therefore give, for some fixed C2,
 |sum_(rho in U OR sigma in U) chi*chi*J_N|
 <<N^(122/125)*L^C2+N^(9/10)*L^12+N^(-7/10)*L^13.             (12)
The exponent122/125=1-(6/125)/2 pays the Gram square root. The
intersection exponent119/125 is smaller. This is an ACTUAL complex
signed bound; it is not a termwise absolute bound on J_N itself.

5. COMBINE MASKS BEFORE BOUNDING; RETAIN A PRECISE DETECTED REMAINDER.
Let D be the prior exterior-real-part set {beta<=a or beta>=b}.
The earlier result proves its energy E_D all-log small, and D and U
are disjoint. Apply the SAME Gram argument directly to W=D union U,
with E_W=E_D+E_U, then use inclusion-exclusion for the two coordinates.
This gives an all-log bound for the full-band union
 {rho in W OR sigma in W}, proving(4). We do not assume an O(1)
arithmetic norm for a masked field or subtract arbitrary coupled masks.
The old beta endpoint and J-minus-beta errors were absolute over this
entire band, so every subset used here inherits them.

For each zero in V, choose the LEAST allowed dyadic M satisfying(3).
This partitions V into O(logT) disjoint copy-counted lists V_M and
the remaining paired sum exactly into O((logT)^2) Cartesian products
V_M times V_H. Every zero in each coordinate list satisfies the
stated detector inequality at that list's common length. Lists may be
empty and no common length for the entire spectrum is claimed.
This partition provides an explicit arithmetic condition for the next
signed estimate. The detector inequalities alone do not prove such an
estimate, and their absolute-value lower bounds cannot be inverted into
bounded-phase cancellation without paying the actual coefficients.

All earlier polynomial, phase, prime-support and density results persist.
The source Gamma correction is part of this continuation record. The
smooth T=N9/10 band, much less the full signed Goldbach margin, remains
unresolved after this reduction. The result is new-to-this-task only.
"""
from fractions import Fraction as F


def type_ii_energy_exponent(beta):
    if type(beta) is not F or not F(16,25) <= beta <= F(19,25):
        raise ValueError('exact real part in[16/25,19/25] required')
    return F(9,10)*2*(1-beta)+2*beta-2


def type_ii_band_budget():
    energy=type_ii_energy_exponent(F(19,25))
    return {'energy':energy, 'column':1+energy/2,
            'intersection':1+energy, 'finite_period':F(9,10),
            'beta_endpoint':-F(7,10)}


def gamma_contour_realpart(beta):
    if type(beta) is not F or not F(16,25) <= beta <= F(19,25):
        raise ValueError('exact retained real part required')
    return F(1,2)-beta


def first_detecting_length(squared_values, squared_threshold):
    """Exact finite assignment guard; supplied values are not zeta data.

    The caller owns the allowed-length range and the actual evaluations.
    This helper checks dyadic keys and assigns each record only once.
    """
    if type(squared_threshold) is not F or squared_threshold <= 0:
        raise ValueError('positive exact squared threshold required')
    for length,value in squared_values.items():
        if (type(length) is not int or length < 1 or length & (length-1)
                or type(value) is not F or value < 0):
            raise ValueError('positive dyadic lengths and nonnegative exact squares required')
    return next((m for m in sorted(squared_values)
                 if squared_values[m] >= squared_threshold),None)
