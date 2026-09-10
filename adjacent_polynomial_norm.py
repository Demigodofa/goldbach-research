"""Audit the polynomial-moment route for the remaining N^.41--N^.46 core.

Owner: Kevin's Goldbach research. Purpose: test whether the retained
integer-power detector moments control the original (first-power) arithmetic
cofactor field in the adjacent band. The test finds a real exponent gap;
it does not rule out a new arithmetic estimate.

1. THE QUESTION AND THE EXACT MISMATCH.
Take a_B(n)=sum_(d|n,d<=B)mu(d), and the adjacent coefficient
 b_adj(n)=a_B(n)*1_(N^.41<=n<N^.46). Its convolution b_adj*Lambda
is the actual residual field left after the tail result. A desired estimate
would be ||theta*P_(b_adj*Lambda)/sqrtN||_2=O_A((logN)^-A), or an equivalent
bound for the reflected pairing. The already retained polynomial detector
uses D_M(s)=sum a_B(n)e^(-n/sqrtT)n^-s on one dyadic length M=N^h,
then studies D_M(s)^k. Its mean-value bound applies to the POWERED
coefficient, not to b_adj itself.

2. FIRST-POWER MOMENT FAILS ON AN OPEN PART OF THE STRIP.
For k=1 and p=h in[41/100,46/100], the retained T-term exponent at
beta=19/25 is
 e1(h)=9/10+h*(1-2*(19/25))+2*(19/25)-2
      =21/50-(13/25)*h.
At h=.46 this is 113/625>0; at h=.41 it is 517/2500>0.
The length (P) term is 2*(1-beta)*(h-1)=12/25*(h-1)<0,
but the mean-value interval contributes T and dominates. Thus the
existing first-power moment gives an upper bound growing like N^.18
to N^.21 in normalized energy, even before logs. Zero-density
weights cannot reverse this because the positive layer cake is monotone
and the bad strip reaches beta=19/25.

3. SQUARING CHANGES THE OBJECT.
For k=2, the powered coefficient has P=M²=N^(2h) in[N^.82,N^.92],
inside the licensed good interval. Its T-term exponent becomes
 e2(h)=9/10+2h*(1-2beta)+2beta-2=21/50-(26/25)h,
which is negative throughout h>.41. This proves a saving for D_M²
on the detected-zero moments, as already used by the good-length theory.
It does NOT imply a saving for D_M or for the arithmetic coefficient
a_B*1_(M,2M]. Cauchy gives ||D_M||² as its own second moment; no
inequality changes D_M into D_M² without a lower bound or threshold
on |D_M|. The retained detector threshold applies only to zeros already
classified as detected, not to the entire arithmetic field.

4. TRANSFER AND PROPER-POWER CHECKS DO NOT REPAIR THIS GAP.
The full-field Guinand transfer is algebraically compatible with a larger
cofactor support: its error scales as sqrt(Q) up to fixed logs, so Q=N^.46
would still be power-small after division by sqrtN. But this only relates
the unknown first-power zero field to P_(b_adj*Lambda); it supplies no
bound for that zero field. The proper-power removal bound at Q=N^.46
is N^-49/400 L^(11/2), which is small, but it applies after a first-power
norm or moment has been obtained. No existing polynomial inequality bridges
these two objects.

5. DISPOSITION.
The proposed retained-moment route is falsified for its stated target:
the k=1 exponent is positive, while k=2 controls a different powered
coefficient. This is not an all-method barrier. A future arithmetic input
could supply a first-power cancellation, a pointwise lower/upper detector
relation, or a genuinely bilinear decomposition. Preserve the successful
k=2 good-length component and the N^.46 prime-companion tail. The signed
core, reflected pairing and Goldbach coverage remain open.
"""
from fractions import Fraction as F


def adjacent_moment_exponents(h, beta=F(19, 25), power=1):
    if (type(h) is not F or type(beta) is not F or type(power) is not int
            or not F(41, 100) <= h <= F(46, 100)
            or not F(16, 25) <= beta <= F(19, 25)
            or power < 1):
        raise ValueError('licensed adjacent exponent, beta and positive power required')
    p=power*h
    return {'T':F(9,10)+p*(1-2*beta)+2*beta-2,
            'length':2*(1-beta)*(p-1)}


def powered_length_is_licensed(h, power=2):
    if type(h) is not F or not F(41,100) <= h <= F(46,100):
        raise ValueError('adjacent length exponent required')
    if type(power) is not int or power < 1:
        raise ValueError('positive integer power required')
    p=power*h
    return F(41,50) <= p <= F(49,50)


def transfer_error_exponent(cofactor_support):
    if type(cofactor_support) is not F or cofactor_support <= 0:
        raise ValueError('positive support exponent required')
    return cofactor_support/2-F(1,2)
