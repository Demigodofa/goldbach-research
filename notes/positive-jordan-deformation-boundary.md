# Positive Jordan deformation and its prime-detecting boundary

Owner: Goldbach research. Parent: `3712c0e46caacd1608580927e2d922f85ddef209`.
Purpose: test a positive multiplicative deformation as a different route
to the unpaid prime correlation, and decide whether its controlled averages
can be transferred to the prime-detecting coefficient at zero.
Novelty: `new-to-this-task`; no historical novelty claim.

## One question, declared before computation

Can positivity and uniform pair asymptotics for a Jordan-type deformation
resolve its quadratic coefficient at s=0? This combines the exact Mobius
prime detector with positive Euler products, rather than adding another
cutoff, support localization or norm inequality to the residual.

Mechanism: J_s(n)=sum_(d|n)mu(d)(n/d)^s is positive for real s>0 and
J_s(n)/s tends to Lambda(n) for n>1. First control its normalized pair
average by truncating prime factors, not divisors. Changed prediction:
the new family has a pointwise positive, controllable main, potentially
even for s tending to zero. The required analytical estimate is

```text
F_N(s)=I_s rho_s(N)+O(y^(-s)/s+M_y/N),   M_y=product_(p<=y)p. (Goal)
```

Falsifier of the proposed TRANSFER: the same asymptotic survives deleting
all prime-power-containing pairs while the quadratic coefficient becomes
identically zero. Budget: one elementary uniform estimate, exact guards,
and a separate review. No scans or inferred boundary derivatives. Sleep
the prime-detection route if that falsifier holds; preserve only the proved
estimate and exact boundary obligation. Creative tools checked: curiosity,
inventive synthesis and hypothesis preservation. No Qwen.

## Definitions and exact detector

For integer n>=1 and real s>0 define

```text
J_s(n)=sum_(d|n)mu(d)(n/d)^s
      =n^s product_(p|n)(1-p^(-s)),
q_s(n)=J_s(n)/n^s,                  0<q_s(n)<=1.
```

These identities follow by expanding the finite Euler product. At s=1
this is the ordinary totient. For n>1 the function J_s(n) is entire in s,
vanishes at zero to order omega(n), and its first derivative there is
Lambda(n). In particular PRIME POWERS, not just primes, have order one.
Indeed, if n=product p^a,

```text
J_s(n)=product_(p^a||n) exp((a-1)s log p)(exp(s log p)-1).
```

Every leading coefficient is positive. The Mobius/Mangoldt identity also
appears in [NIST DLMF 27.5.5](https://dlmf.nist.gov/27.5.E5).

Let N>=6 be even, I_N=(N/3,2N/3) intersect Z, and define

```text
w_s(u)=[u(1-u)]^s,
F_N(s)=N^(-2s-1) sum_(n in I_N)J_s(n)J_s(N-n)
      =(1/N)sum_(n in I_N)w_s(n/N)q_s(n)q_s(N-n),
I_s=integral_(1/3)^(2/3)w_s(u)du,
rho_s(N)=product_p [1-2/p^(1+s)+1_(p|N)/p^(1+2s)].
```

The Euler product converges absolutely and is positive for every s>0.
Writing [s^2] for Taylor coefficient at zero, the exact finite identity is

```text
[s^2]F_N(s)=(1/N)sum_(n in I_N)Lambda(n)Lambda(N-n).       (1)
```

The factor N^(-2s) does not change this coefficient, since the unnormalized
sum already vanishes to order at least two. Extracting actual PRIME pairs
would still require the known proper-power correction; positivity of (1)
alone is not being promoted into Goldbach.

## Uniform averaging theorem

For all 0<s<=1, even N>=6, and integers y>=2, (Goal) holds with an ABSOLUTE
implied constant, independent of s,N,y. Its proof uses no prime-pair
distribution or exceptional-zero hypothesis.

Set q_(s,y)(n)=product_(p|n,p<=y)(1-p^(-s)). For n>=1,

```text
0<=q_(s,y)(n)-q_s(n)<=sum_(p|n,p>y)p^(-s).
```

The difference of the two pair products is at most the sum of the two
individual differences. Reflection preserves I_N, and w_s<=1, so replacing
q_s by q_(s,y) in F_N costs at most

```text
(2/N)sum_(n<=N)sum_(p|n,p>y)p^(-s)
 <=2 sum_(p>y)p^(-1-s)<=2 y^(-s)/s.                      (2)
```

There is NO extra endpoint error for each prime: the number of multiples
in the enlarged interval [1,N] is floor(N/p)<=N/p. The final inequality
uses the integral bound for the sum over all integers >y.

The truncated pair product is periodic of period M_y and takes values in
[0,1]. Its complete-period mean is

```text
rho_(s,y)(N)=product_(p<=y)[1-2p^(-1-s)+1_(p|N)p^(-1-2s)]. (3)
```

For p|N, the two divisibility events coincide with probability 1/p.
For p not dividing N they are disjoint, each with probability 1/p.
CRT multiplies these exact local means. Prefix discrepancy from the mean
is at most M_y. Partial summation with w_s(n/N), whose supremum and total
variation on [1/3,2/3] are bounded absolutely for 0<s<=1, gives

```text
(1/N)sum_(n in I_N)w_s(n/N)q_(s,y)(n)q_(s,y)(N-n)
 =I_s rho_(s,y)(N)+O(M_y/N).                              (4)
```

Strict endpoint discrepancies are included in this bound. All local
factors lie in [0,1], so the Euler-product tail is bounded by
2 sum_(p>y)p^(-1-s)<=2y^(-s)/s. Equations (2)-(4) prove (Goal).

## A shrinking real-parameter range is genuinely controlled

The main has an N-uniform lower bound

```text
rho_s(N)>=C_2/zeta(1+s)^2>=s^2/8,
I_s>=2/27,                    I_s rho_s(N)>=s^2/108.       (5)
```

To check the first inequality, divide each Euler factor by
(1-p^(-1-s))^2. At p|N the ratio is at least one. At p not dividing N
(hence p>=3), it is at least 1-1/(p-1)^2. Their product is at least C_2,
which exceeds 1/2 by the elementary product bound already used in the
parent note. Also zeta(1+s)<=1+1/s<=2/s. On the central interval,
u(1-u)>=2/9 and s<=1, proving the I_s bound.

Put L=log N, ell=log log N, and for sufficiently large N choose

```text
y=floor(L/(4ell)),        a_N=8 log(ell)/ell.
```

Then y>=2, M_y<=y!<=y^y<=N^(1/4), log y>=ell/2 and a_N<=1.
Uniformly for a_N<=s<=1, the error in (Goal), divided by s^2, is at most
an absolute constant times

```text
y^(-a_N)/a_N^3 + N^(-3/4)/a_N^2
 <=1/[512 ell (log ell)^3] + N^(-3/4)/a_N^2 = o(1).       (6)
```

Thus F_N(s)=I_s rho_s(N)(1+o(1)) uniformly on this shrinking range,
at EVERY sufficiently large even N. The particular constant 8 is a
conservative analytical choice from (6), not an optimized or fitted one.
This proof does not extend that asymptotic to s=0.

## Actual arithmetic falsifier of coefficient transfer

Define the comparison family using the SAME J_s on actual integers:

```text
F_N^comp(s)=N^(-2s-1)
 sum_(n in I_N, omega(n)>=2, omega(N-n)>=2)J_s(n)J_s(N-n).
```

This deletes a pair if EITHER argument is a prime power. It is NOT a
thinned Lambda model, a signed support-localization theorem for D_R, or a
claim that this comparison still has the Lambda derivative. Precisely the
opposite is the point: every retained product vanishes to order at least
four, so for every fixed N,

```text
[s^2]F_N^comp(s)=[s^3]F_N^comp(s)=0.                     (7)
```

Yet for every real 0<s<=1,

```text
0<=F_N(s)-F_N^comp(s)
 <=(2/N)#{prime powers <=N}=O(1/log N),                   (8)
```

uniformly in s. Each normalized summand is <=1. The prime-count bound
pi(N)<<N/log N follows, for example, from
[NIST DLMF 27.12.5](https://dlmf.nist.gov/27.12.E5); proper powers have
O(sqrt(N)log N) positions by elementary counting. This bound uses only
one-point counting, not a prime-pair asymptotic. It includes the midpoint
and deliberately overcounts pairs deleted from both sides.

Since 1/(a_N^2 log N)->0, (5)-(8) prove that F_N^comp has exactly the SAME
relative asymptotic I_s rho_s(N)(1+o(1)), uniformly for a_N<=s<=1.
It is eventually positive throughout that range despite (7).

## Decision and the missing estimate

Pursuit status: `changed-under-evidence`. Positive Jordan deformations do
admit an unconditional, pointwise, uniform averaging estimate. But the
leading relative asymptotic and real positivity throughout that range,
including its shrinking lower endpoint, are unchanged by removing every
prime-power-containing pair. These facts therefore cannot justify extracting the quadratic prime-
detecting coefficient. This is the substantive falsifier of the attempted
transfer, not a new lower bound for the unresolved signed residual.

For fixed N, exact analytic values on an open interval DO determine all
Taylor coefficients. Nothing here contradicts that fact. The failure is
interchanging an N-asymptotic with boundary differentiation without a
uniform estimate at the boundary. In particular, we have not proved a
uniform complex-neighborhood estimate around zero or a remainder o(s^2)
as s->0 at fixed N. Further use of this route must supply new boundary-
sensitive information that distinguishes F_N from F_N^comp. More samples
inside the proved range cannot supply it by their leading asymptotic alone.

The positive family and exact identities remain available; the automatic
coefficient-transfer shortcut is retired. No claim rules out every Jordan
transform method or estimates the best possible boundary scale. No new
joint unit/squarefree mask, prime existence theorem, effective Goldbach
threshold or finite remainder is proved. Preserve all earlier q286/Q46189,
signed compensation, Type I, L2, thinning and exceptional-zero boundaries.
The full prove-or-disprove objective remains active. Exact fixtures check
the divisor identities, local CRT means, tail bound and coefficient orders;
they are not numerical evidence for the asymptotic theorem.
