"""Filter actual detector lengths by their integer-power mean squares.

Owner: Kevin's Goldbach research. Purpose: use the actual detector
coefficients in the surviving T=N^(9/10) band. All source corrections,
prime-support bounds and unproved signed margins remain in force.

1. THE ACTUAL FILTER AND FOUR REMAINING LENGTH INTERVALS.
Keep N,T=N^(9/10),L=logN, a=16/25,b=19/25 and the exact D_M
from zero_detector_band_reduction.py. Allowed M are dyadic in
[T^(1/100),sqrtT*(logT)^2]. A length M is GOOD if for some integer
1<=k<=100,
 N^(41/50)<=M^k<=N^(49/50).                                    (1)
Let G contain the actual zero copies with a<beta<b which are detected
at ANY good length: |D_M(rho)|>=1/(3logT). Then for some fixed C,
 |sum_(rho in G OR sigma in G)chi(gamma/T)chi(eta/T)J_N(rho,sigma)|
 <<N^(623/625)*L^C+N^(9/10)*L^12+N^(-7/10)*L^13.               (2)
The other coordinate in this sum is the FULL unmasked smooth band.
This is a COMPLEX signed estimate for the actual finite-period kernel.

Combined with the earlier exterior-real-part and nondetector reductions,
the whole smooth band therefore reduces with O_A(N/L^A) error to zero
copies which have a<beta<b, are detected at least once, and are NOT
detected at ANY good length. Every detecting length of a surviving zero
has m=logM/logN in one of the FOUR OPEN intervals
 (49/300,41/250), (49/250,41/200),
 (49/200,41/150), (49/150,41/100).                             (3)
The end points are good and are removed. This statement holds for all
sufficiently large N; the allowed upper length is N^(9/20)*log^2T,
not literally N^(9/20). No contribution bound is proved for the
remaining detected-pair sum beyond its retained O(N) bound.

2. POWERED COEFFICIENTS AND THEIR COMPLETE SECOND-MOMENT COST.
Fix an allowed M and k satisfying(1), and put P=M^k. Then
 F(s)=D_M(s)^k=sum_(P<n<=2^k*P)c(n)*n^(-s),
 |c(n)|<=tau_(2k)(n),                                         (4)
because |a_T(n)exp(-n/sqrtT)|<=tau_2(n) and the unrestricted
k-fold Dirichlet convolution of tau_2 is tau_(2k). Restricting the
factors to(M,2M] only decreases the positive coefficient majorant.
Factors2^k are constants since k<=100, not uncharged N powers.

For every positive integer r, tau_r(n)^2<=tau_(r^2)(n). At a
prime power p^e, the left side counts pairs of r-component weak
compositions of e. Every such pair can be the row and column sums of
a nonnegative integer r-by-r matrix of total e, by the greedy filling
algorithm. Different pairs have disjoint sets of matrices. Counting
all such matrices proves the inequality, and multiplicativity proves
it for n. Moreover, for fixed q,
 sum_(n<=X)tau_q(n)<=X*(1+logX)^(q-1),                          (5)
by fixing q-1 factors, bounding the number of choices for the last
factor by X divided by their product, and enlarging the harmonic sums.
Thus uniformly for a<=sigma<=b,
 sum_n |c(n)|^2*n^(-2sigma)<<_k P^(1-2sigma)*L^(4k^2-1).       (6)
Every coefficient cost remains a fixed log power; no n^epsilon is used.

3. MEAN VALUE, ACTUAL COPY SAMPLING AND VARIABLE REAL PARTS.
Primary source checked2026-09-10: Tao,254A Notes6,13Feb2015,
Exercise2(ii), equation(3), states the sharper mean-value estimate
int_(t0)^(t0+H)|sum_(n<=Q)d_n*n^(-it)|^2dt
                  =(H+O(Q))*sum|d_n|^2.
 https://terrytao.wordpress.com/2015/02/13/254a-notes-6-large-values-of-dirichlet-polynomials-zero-density-estimates-and-primes-in-short-intervals/
Only that mean-value fact is relevant here, not the page's later
zero detector or unrelated statements. We provide an elementary
weaker bound, sufficient with its EXTRA LOGARITHM PAID:
 int_(t0)^(t0+H)|sum_(n<=Q)d_n*n^(-it)|^2dt
             <<(H+Q*log(2Q))*sum|d_n|^2.                       (7)
Expand the square. The diagonal is H*sum|d_n|^2. For m!=n the
integral is bounded by2/|log(m/n)|<=2Q/|m-n|. Use
2|d_m*d_n|<=|d_m|^2+|d_n|^2 and sum the harmonic row bound.
This proves(7) for every t0 and complex coefficient list without
spacing assumptions or a Hilbert-inequality citation.

For a C1 function H(t), the elementary unit-interval Sobolev bound is
 |H(v)|^2<<int_(v-1)^(v+1)(|H(t)|^2+|H'(t)|^2)dt.             (8)
To see this, compare H(v) with H(t) by the fundamental theorem of
calculus, apply Cauchy on the interval, and average t. Actual zero
ordinates in[T,2T], with copies, have O(L) occupancy in every unit
interval. Summing(8) over ANY subset therefore costs at most O(L)
overlap and an integral over[T-1,2T+1]. Apply(7) with Q<=2^k P
and H comparable to T. Derivatives in t add factors logn=O_k(L).

It remains essential that beta varies between zeros. Fix sigma in[a,b]
and consider only zero copies with sigma<=beta<=b. Write
 F(beta+i*gamma)=F(sigma+i*gamma)
     -int_sigma^beta F_1(alpha+i*gamma)dalpha,
 F_1(s)=sum_n c(n)*logn*n^(-s).                                (9)
Cauchy bounds the squared integral by(b-a)*int_sigma^b|F_1|^2.
Sum over the zeros BEFORE integrating in alpha. The fixed-real-part
Sobolev/mean-value bound applies for each alpha; its derivative in t
uses at most two factors logn. Since alpha>=sigma and n>=1, its
coefficient square sum is no larger than the one at sigma, apart from
these explicit logarithms. Equations(6)-(9) give
 sum_(copies: sigma<=beta<=b, gamma in[T,2T])|F(beta+i*gamma)|^2
                 <<_k (T+P)*P^(1-2sigma)*L^(4k^2+5).          (10)
For example the largest log cost is4k^2-1 from(6), four from the
two logn factors after squaring, one from(7), and one from occupancy.
The exponent in(10) is their sum. No uniform-spacing, RH, or fixed-beta
assumption has entered, and no detector predicate was needed yet.

If |D_M(rho)|>=1/(3logT), then
 |F(rho)|^2>= (3logT)^(-2k),                                  (11)
not merely the original detector threshold. Therefore the number
R_(M,k)(sigma) of detected zero copies with sigma<=beta<=b obeys
 R_(M,k)(sigma)<<_k(T+P)*P^(1-2sigma)*L^(4k^2+2k+5).           (12)
This is uniform in sigma in[a,b]. Constants such as3^(2k) remain
bounded over the finite set1<=k<=100, and are included explicitly
in the implied constant. Huge fixed log powers give no numerical onset.

4. THE NORMALIZED ENERGY HAS A STRICT SAVING IN BOTH MEAN-VALUE TERMS.
Let E_(M,k) be sum |chi(gamma/T)|^2*N^(2beta-2) over the detected
middle-strip zero copies at this M. By positive layer cake,
 E_(M,k)<<N^(2a-2)*R_(M,k)(a)
         +2L*int_a^b N^(2sigma-2)*R_(M,k)(sigma)dsigma.        (13)
Put p=logP/logN in[41/50,49/50]. The T and P terms in(12)
respectively have normalized exponents
 e_T(beta,p)=9/10+p*(1-2beta)+2beta-2,
 e_P(beta,p)=2*(1-beta)*(p-1).                                 (14)
Both are increasing in beta because p<1. At beta=b=19/25,
 e_T=21/50-(13/25)*p<=-4/625,
 e_P=(12/25)*(p-1)<=-6/625.                                   (15)
The first worst case is p=41/50, the second p=49/50. The lower
boundary term in(13) obeys the same bounds. Thus each energy is
O(N^-4/625 times a fixed log power).

There are O(L) allowed dyadic M and at most100 powers. Summing
their NONNEGATIVE energy bounds, even when a zero is detected more
than once, bounds the UNION G. For example the deliberately ample
fixed exponent40220 pays all thresholds, powers, layer cakes and
length summation, giving
 E_G<<N^(-4/625)*L^40220.                                     (16)
This exponent is bookkeeping, not an optimized rate or finite certificate.

5. ACTUAL FINITE-PERIOD DELETION AND THE REMAINDER'S QUANTIFIERS.
Use the retained Gram synthesis estimate for a restricted actual field,
||theta*Z_G||_2^2<<L*E_G, and the O(1) arithmetic energy ONLY for
the full Z=S_T(aN)/sqrtN. Column and row cost sqrt(L E_G), and
their intersection costs L E_G. The exact beta identity and absolute
endpoint/J-minus-beta errors therefore give
 |sum_(rho in G OR sigma in G)chi*chi*J_N|
 <<N*[sqrt(L E_G)+L E_G]+N^.9 L^12+N^(-.7)L^13.                (17)
Equation(16) proves(2); the Gram square root gives623/625 and the
intersection621/625 is smaller. The large log power is fixed, hence
every displayed error is all-log small on the N scale asymptotically.

Combine G with the prior exterior set D and nondetected middle set U
BEFORE applying the same Gram argument: D,U,G are disjoint and their
energies add. This licenses the final reduction without assuming that
arithmetic energy stays O(1) under arbitrary masking. A zero is removed
if ANY detecting length is good, even if its least detecting length is bad.
Every survivor has at least one detector, and ALL its detecting lengths
lie in the complement of(1). Choosing its least remaining detector then
gives the prior disjoint Cartesian partition. No arbitrary pair mask is used.

6. EXACT INTEGER-POWER COVERAGE LEAVES FOUR GAPS.
Writing m=logM/logN, condition(1) is
 m in union_(k=1)^100 [41/(50k),49/(50k)].                      (18)
The intervals for k>=6 overlap their neighbors because
41/(50k)<=49/(50(k+1)) iff k>=41/8; their union is
[41/5000,49/300]. The other five intervals, for k=5,4,3,2,1,
are [41/250,49/250], [41/200,49/200], [41/150,49/150],
[41/100,49/100], [41/50,49/50], respectively. They are separated.
The actual allowed range begins at m=9/1000>41/5000 and ends at
9/20+2loglogT/logN<49/100 for sufficiently large N. Intersecting
with that range leaves exactly the possible open gaps in(3); eventually
the allowed upper range exceeds41/100, so no additional upper gap occurs.
This is not a continuous choice of k. For example m=7/20 lies in
the fourth gap and has no eligible integer power; m=9/20 does.

This is an application of classical power moments to the actual detector
and current paired-band normalization, new-to-this-task only. The remaining
four ranges and their signed paired interaction are not bounded here. All
earlier polynomial/phase components and the corrected Maynard--Pratt
Gamma argument persist. The overall Goldbach research goal remains open.
"""
from fractions import Fraction as F


def power_window_exponents(beta, power_length):
    if (type(beta) is not F or type(power_length) is not F
            or not F(16,25) <= beta <= F(19,25)
            or not F(41,50) <= power_length <= F(49,50)):
        raise ValueError('exact retained beta and licensed power-length interval required')
    return {'time':F(9,10)+power_length*(1-2*beta)+2*beta-2,
            'length':2*(1-beta)*(power_length-1)}


def eligible_powers(length_exponent):
    if type(length_exponent) is not F or length_exponent <= 0:
        raise ValueError('positive exact length exponent required')
    return tuple(k for k in range(1,101)
                 if F(41,50) <= k*length_exponent <= F(49,50))


def merged_power_intervals():
    intervals=sorted((F(41,50*k),F(49,50*k)) for k in range(1,101))
    merged=[]
    for left,right in intervals:
        if not merged or left > merged[-1][1]:
            merged.append([left,right])
        else:
            merged[-1][1]=max(merged[-1][1],right)
    return tuple(tuple(pair) for pair in merged)


def source_threshold_log_loss(power):
    if type(power) is not int or not 1 <= power <= 100:
        raise ValueError('integer power in[1,100] required')
    return 2*power
