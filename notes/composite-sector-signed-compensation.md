# Pointwise signed compensation in the composite sector

Owner: Goldbach research. Parent: `8d7d8f82840357f3cfd7bd4471ded37eb1f8e583`.
Purpose: decide whether the main-scale adverse composite blocks can defeat
their whole actual composite-composite sector, rather than produce more
factor-shape examples. Novelty: `new-to-this-task` application of established
inputs; no worldwide originality claim.

## Question declared before computation

For fixed 0<theta<1/2, does the ACTUAL signed residual correlation on
composite-composite pairs have a positive main-scale lower bound at EVERY
sufficiently large even target, despite its adverse sub-blocks?

Mechanism: subtract the prime-containing terms from the controlled cutoff
correlation. The prime-cutoff term requires a proved 1/log(t)-weighted
estimate. The remaining unknown prime-pair term has a nonnegative sign.
Changed prediction: the whole composite sector compensates its own adverse
mass pointwise, including the earlier six-factor block. Required bound:

```text
C(D_c,D_c) >= (1-2theta-o_theta(1))H(N),                   (Goal)
```

where D_c is D restricted to actual composites, including proper powers.
Falsifiers: the weighted prime estimate is not licensed by BV; prime powers
or ordered-pair overlap are omitted; the unknown pair term has the wrong
sign; or recombination hides a circular claim about the full residual.
Budget: one analytic sector theorem, exact algebra fixtures and a separate
source/math review. No parameter scan. Sleep the claim if the weighted
input or power correction cannot be paid. Creative tools checked:
curiosity, inventive synthesis, hypothesis preservation. No Qwen.

The older cutoff normalization supplies the independent correlation mains;
the recent adverse block makes their consequence for this sector worth
examining. This is not a new support-elimination theorem or an assumption
that the recent positive-sign sector is itself compensated internally.

## Statement

Let N tend to infinity through even integers. Fix 0<theta<1/2 and put

```text
I_N=(N/3,2N/3) intersect Z,   R=floor(N^theta),   a=log R,
A(n)=sum_(d|n,d<=R)mu(d)log(R/d),   D(n)=Lambda(n)-A(n),
C(f,g)=sum_(n in I_N)f(n)g(N-n),    H=S_2(N)N/3.
```

Let P(n) indicate actual primes, Lambda_p(n)=P(n)log n, and
Q(n)=Lambda(n)-Lambda_p(n), supported on PROPER prime powers. Define

```text
D_p=P D,        D_c=(1-P)D,
Z_N=C(P,P),     M_N=C(Lambda_p,P),     T_N=C(Lambda_p,Lambda_p),
J_N=integral_(N/3)^(2N/3) dt/log t.
```

All pair quantities are ORDERED; a prime midpoint occurs once.
For every fixed J>0 we prove

```text
C(D_c,D_c) = H - 2a S_2(N) J_N + a^2 Z_N
                  + O_(theta,J)(N/log(N)^J).              (1)
```

The nonnegative term a^2 Z_N is retained, not evaluated or assumed
positive. Since a=theta log N+o(1) and
J_N=N/(3log N)+O(N/log(N)^2), this implies (Goal). In particular,

```text
C(D_c,D_c) >= (1-2theta)H/2 > 0                           (2)
```

for all sufficiently large even N, with theta fixed. No numerical onset
is supplied. No uniformity as theta approaches 1/2 is claimed.

If C_cc^+ and C_cc^- are the positive and negative parts of the actual
composite-pair products, (2) states C_cc^+ >= C_cc^-+(1-2theta)H/2.
The earlier adverse six-factor block is contained in C_cc^-; its existence
is consistent with, and now accompanied by, this pointwise compensation.
Compensation can come from other factor counts or signs. It is not proved
inside that six-factor sector alone, or on a new joint squarefree/unit mask.

## Inputs and the weighted prime estimate

Reuse the accepted target-uniform deduction

```text
C(A,A)=H+O_(theta,J)(N/log(N)^J)
```

from `cutoff-normalized-complementary-remainder.md`. We do not reprove its
common-divisor analysis. The primary inputs for the weighted step are
Goldston and Yildirim,
[Higher correlations of divisor sums related to primes I](https://math.colgate.edu/~integers/d5/d5.pdf),
ordinary BV (1.30), printed p.8, with its unconditional exponent 1/2;
Lemma 2.1 (2.11)-(2.12), printed p.16. Checked 2026-09-16. No restricted-
shift pair theorem is applied at shift N, and no two-prime distribution
claim is an input.

We need and prove

```text
C(P,A)=S_2(N)J_N+O_(theta,J)(N/log(N)^J).                  (3)
```

Put l=N/3, u=ceil(2N/3)-1 and, for l<=t<=u,

```text
V_N(t)=sum_(l<m<=t)Lambda(m)A(N-m).
```

Expand A. For (d,N)=1 the inner progression has residue N mod d and
endpoints l,t. Choose a fixed epsilon>0 with theta<1/2-epsilon. For all
sufficiently large N, R<=t^(1/2-epsilon), uniformly for t in [l,u].
The residue maximum in BV covers N mod d, and each coefficient is at most
log R in absolute value. Its extra logarithm is paid by choosing the BV
logarithmic saving larger. The endpoint t is COMMON to all d. Applying
BV at each such t, with constants uniform in t, bounds

```text
sup_t sum_(d<=R) max_(r reduced)|psi(t;d,r)-t/phi(d)|
      <<_(theta,J) N/log(N)^J.                            (4)
```

The supremum is OUTSIDE the modulus sum. No exchange to a sum of separate
prefix maxima is asserted, and no mesh or shrinking cutoff-gap extension
of the earlier Type I theorem is needed.

For (d,N)>1, any prime m in that progression would divide d and hence
satisfy m<=R<l, impossible. Only proper powers remain. Summing first over
their actual positions, rather than charging R once per position, gives

```text
sum_(m in I_N, m proper power) Lambda(m)
    sum_(d|N-m,d<=R) |mu(d)|log(R/d)
 <<_eta N^(1/2+eta)(log N)^3                               (5)
```

for any fixed eta>0, using tau(k)<<_eta N^eta and the elementary
O(sqrt N log N) count of proper powers. Choose eta<1/2. This is smaller
than N/log(N)^J for every fixed J. The same bound is uniform in t.

The reduced scalar main is

```text
W_R(N)=sum_(d<=R,(d,N)=1)mu(d)log(R/d)/phi(d)
      =S_2(N)+O_theta(exp(-c_theta sqrt(log R)))            (6)
```

by Lemma 2.1, with log N/log R bounded in terms of fixed theta. Thus,
for each requested saving, uniformly throughout the common prefix,

```text
V_N(t)=(t-l)S_2(N)+O_(theta,J)(N/log(N)^J).                (7)
```

Apply Stieltjes partial summation with w(t)=1/log t. Its supremum and
total variation on this central interval are O(1/log N). Equation (7)
therefore gives

```text
sum_(m in I_N) [Lambda(m)/log m] A(N-m)
     =S_2(N) integral_l^u dt/log t+O_J(N/log(N)^J).         (8)
```

Removing the proper-power terms on the left costs at most
O_eta(N^(1/2+eta)(log N)^2), since Lambda(p^k)/log(p^k)=1/k.
Replacing u by 2N/3 in the integral costs O(S_2(N)/log N), negligible
at the asserted scale (for example S_2(N)<<tau(N)). This proves (3),
with strict endpoints paid. Multiplying its error by a later costs a
logarithm, paid by starting with one more saving.

Taking t=u in (7) and removing Q similarly gives

```text
C(Lambda_p,A)=H+O_(theta,J)(N/log(N)^J).                  (9)
```

This proof never replaces a signed prime-cutoff sum by an unproved small
absolute one. That shortcut would not justify the weighted estimate.

## Exact sector subtraction and the power correction

For all large N, every central prime exceeds R, so A(p)=a exactly. Put

```text
B=A-aP=(1-P)A.
```

The exact pointwise formulas are

```text
D_p=Lambda_p-aP,        D_c=-B+Q.
```

Hence

```text
C(D_c,D_c)=C(B,B)-2C(B,Q)+C(Q,Q),
C(B,B)=C(A,A)-2a C(P,A)+a^2 Z_N.                         (10)
```

The reflection symmetry of I_N gives the factor 2. On central arguments,
|B(n)|<<tau(n)log N, |Q(n)|<=log N, and Q is supported at O(sqrt N log N)
positions. Therefore both correction correlations in (10) are
O_eta(N^(1/2+eta)(log N)^3), with eta fixed less than 1/2.
This is a signed/absolute estimate for these power corrections only, not
an estimate of absolute composite mass. Substituting (3) and the accepted
cutoff main into (10) proves (1).

For clarity the explicit main has the conservative bound

```text
1 - 6a J_N/N >= 1 - 2theta/(1-log(3)/log N).              (11)
```

It follows from a<=theta log N and log t>=log N-log 3. The right side
tends to 1-2theta>0. Since S_2(N)>=2C_2>0, the error in (1) divided by H
tends to zero, proving (2). Inequality (11) is not a numerical threshold
for the full theorem: the analytical remainder still needs its constants.

## No free margin for Goldbach

Keep the unknown Z_N,M_N,T_N exact. The other two sectors satisfy

```text
C(D_p,D_p) = T_N-2aM_N+a^2 Z_N,                           (12)
2C(D_p,D_c) = -2H+2a S_2(N)J_N+2aM_N-2a^2 Z_N
                         +O_J(N/log(N)^J).               (13)
```

For (13), expand C(Lambda_p-aP,-B), use (3),(9), and pay C(D_p,Q) by
the same proper-power count. There is one orientation in C(D_p,D_c);
the total mixed sector has two. Equations (1),(12),(13) recombine to

```text
C(D,D)=T_N-H+O_J(N/log(N)^J),                             (14)
```

with EVERY occurrence of a S_2 J_N, a M_N and a^2 Z_N cancelling.
The positive composite main has already been spent by the mixed main.
It is not an additional positive margin for (14). In particular this
sector theorem is compatible with hypothetical T_N=0: it neither proves
nor disproves that such targets exist.

## What changed

Pursuit status: `changed-under-evidence`. A full ACTUAL signed sector now
has a uniform positive lower bound, without assuming any prime pairs.
This removes the obligation to regard composite-composite correlation as
an uncontrolled NET adverse term. Its internal adverse blocks remain real
and need compensating positive mass, which the theorem now guarantees.
The result is not merely a restated identity: (3) and the paid corrections
turn the exact partition into the pointwise inequality (2).

It supplies no favorable excess after full recombination. A further step
must control the remaining prime-bearing coupling or bring a genuinely
different input, not count the composite margin twice. We have not proved
compensation within any narrower factor/sign sector or joint support mask.
The original cutoff-normalized C(D,D), S_sf, E_D and unit/Vaughan gates
remain open at Goldbach strength. No effective starting point, finite
remainder closure or Goldbach proof/disproof exists here. Preserve q286
missing mass, Q46189 transfer gaps, the absolute-remainder and finite-
cutoff L2 obstructions and both reflection-thinning boundaries.

The exact helpers in `composite_sector_compensation.py` and their tests
guard prime/composite classification, retained proper powers, ordered
reflection, exact unknown pair terms, the main coefficient and the
no-double-counting identity. They do not establish any asymptotic rate.
Review and actual test receipts are recorded separately.
