# Actual logarithmic cutoff and the RH approximation norm

Owner: Kevin; lead: Rill. Purpose: determine whether the Goldbach cutoff
machinery transfers to a non-circular RH target before creating new numerical
or visual tools. Parent: `riemann-crossover-inventory.md`. Source checkpoint:
`60323ae913518b1c2cc043c5e31abb10faded64a`.

## Question and decision contract

Question: does the actual logarithmic Mobius cutoff enter the published
Nyman--Beurling approximation problem, and do the old cutoff estimates pay
its norm? Mechanism: fractional parts turn the same divisor coefficients into
a summatory cutoff discrepancy. Prediction to test: a proved logical bridge
can replace the earlier unproved transfer, but an unestimated arithmetic
range may remain. Falsifier of automatic reuse: the needed norm contains a
term outside the scope of the saved estimates. Required bound, before any
computation: the FULL J_R defined below must tend to zero as R tends to
infinity. No finite scan, best-fit constant or selected window suffices.

Creative tools checked. This joins an older actual Mobius cutoff with Kevin's
reverse-implication idea. It is `new-to-this-task` as a dictionary, NOT a new
mollifier or a new RH criterion. Stop after the transfer, dependency audit,
tail estimate and exact fixtures; do not launch coefficient optimization.

## Published authority and circularity boundary

[Baez-Duarte, Theorem 1.1](https://arxiv.org/pdf/math/0205003)
identifies RH with L2(0,infinity) approximation of chi=1_(0,1) by linear
combinations of rho_d(x)={1/(d*x)}, d positive integers. Thus proving
convergence of one specified family is sufficient. The criterion does not
claim every chosen family converges under RH. This affine target is nonzero:
the zero approximation has squared error one. Generic homogeneous L2
arguments from q286 are not being promoted.

[Bettin--Conrey--Farmer, pp.1-2 and Lemma 3](https://arxiv.org/pdf/1211.5191)
use exactly the logarithmically weighted polynomial below. Their Theorem 1
assumes RH AND a bound on the inverse-square zeta-derivative moment at zeros;
the latter entails simple zeros. Lemma 3 uses those hypotheses to bound the
zero-residue sum. Its decay estimate is not unconditional input for proving
RH. We make no claim that every result for this polynomial needs those extra
assumptions, or that this is the latest possible estimate.

## Exact arithmetic dictionary

Let integer R>=2, L=log R, and retain the actual coefficients

```text
a_d=mu(d)log(R/d), 1<=d<=R,
A_R(m)=sum_(d|m,d<=R)a_d,
c_R=sum_(d<=R)a_d/d,
V_R(s)=L^(-1)sum_(d<=R)a_d*d^(-s).
```

These a_d and A_R are the existing cutoff, not fitted replacements. Define

```text
e_R(x)=chi(x)+L^(-1)sum_(d<=R)a_d*{1/(d*x)},
J_R=int_0^infinity |e_R(x)|^2 dx.
```

The sign is PLUS: the approximation to chi is the negative fractional-part
sum. With Mellin convention M f(s)=int_0^infinity f(x)x^(s-1)dx,

```text
M chi(s)=1/s,
M rho_d(s)=-zeta(s)/(s*d^s), 0<Re(s)<1.
```

For completeness, substitute t=1/(d*x). The second integral becomes
d^(-s)int_0^infinity {t}t^(-s-1)dt. Split at one; integrate the floor
function on [1,infinity) for Re(s)>1 and continue the resulting identity
zeta(s)=s/(s-1)-s*int_1^infinity {t}t^(-s-1)dt to Re(s)>0.
The integral on (0,1) is 1/(1-s), giving the displayed minus sign.
Both endpoint integrals for M rho_d are absolutely convergent in the
stated strip. Each finite e_R is bounded near zero and O_R(1/x) near
infinity, hence is in L2. Mellin-Plancherel at Re(s)=1/2 therefore yields

```text
J_R=(1/(2pi))int_(-infinity)^infinity
        |1-zeta(1/2+it)*V_R(1/2+it)|^2 dt/(1/4+t^2).       (1)
```

There is no RH assumption in (1). J_R->0 would prove RH via the published
criterion. We do NOT assert the converse for this particular V_R.

Set y=1/x and C_R(y)=sum_(m<=y)A_R(m). Counting multiples, exactly,

```text
L*e_R(1/y)=L*1_(y>1)+y*c_R-C_R(y),
C_R(y)=sum_(d<=R)a_d*floor(y/d).                          (2)
```

For 2<=m<=R all divisors are retained, so Mobius inversion gives
A_R(m)=Lambda(m); separately A_R(1)=L. Proper prime powers are included.
Consequently, for 1<y<=R, (2) is y*c_R-psi(y), where
psi(y)=sum_(m<=y)Lambda(m). At y=1 the strict indicator instead gives
c_R-L; this isolated endpoint does not affect an integral.

Changing variables dx=dy/y^2 gives the disjoint NONNEGATIVE ledger

```text
L^2 J_R = c_R^2
 + int_1^R |c_R-psi(y)/y|^2 dy
 + int_R^infinity |L+y*c_R-C_R(y)|^2 dy/y^2.              (3)
```

The first term integrates 0<y<1 exactly. No signed cancellation between
these three terms is available. Neither a Goldbach reflected correlation
nor an arithmetic progression average is the last integral in (3).

## Unconditional removal of the far tail

For every real Y>=R, (2) and 0<={u}<1 imply

```text
int_Y^infinity |L+y*c_R-C_R(y)|^2 dy/y^2
 <= (L+sum_(d<=R)|a_d|)^2/Y
 <= (L+R)^2/Y <= 4R^2/Y.                                (4)
```

Indeed sum|a_d|<=sum_(d<=R)log(R/d)<=R: the decreasing nonnegative
function log(R/t) on (0,R] has integral R and dominates its right-endpoint
sum. Also log R<=R. Thus taking Y=R^3 leaves norm error at most
4/(R*log(R)^2), which tends to zero without RH.

This actually removes the infinite far-tail obligation for this family.
The required finite-but-growing-window estimate is now exactly

```text
c_R^2 + int_1^R |c_R-psi(y)/y|^2 dy
      + int_R^(R^3) |L+y*c_R-C_R(y)|^2 dy/y^2
                                                    = o(log(R)^2). (5)
```

By (3)-(4), (5) is equivalent to J_R->0 and hence sufficient for RH.
The saved smoothed Mobius estimate c_R->1 controls the first term only.
No estimate for the two remaining integrals is proved here. A bound supplied
by PNT must be integrated and squared with this measure; a small relative
pointwise error by itself is not a payment for a growing-range norm.
The one-sided Goldbach residual estimate remains independently open.

## Decision

Status: `changed-under-evidence`. The transfer to an RH-sufficient target is
real and non-circular; the same weight family has established prior art.
The far tail is paid, while (5) remains open. This is a checked dictionary
and scoped tail estimate, NOT a new strategy resolving RH or proof that all
possible uses of the old estimates fail. The benefit is identifying the
exact missing estimate and preventing a circular import of a conditional one.
No RH or Goldbach proof/disproof, effective threshold or finite closure.

Fixtures: `rh_mobius_cutoff_transfer.py` and
`test_rh_mobius_cutoff_transfer.py`. Exact rational log-prime vectors check
the original cutoff mapping, floor/fractional-part identity, prime-power
jumps and strict endpoint. They do not test the asymptotic conclusion.
## Review and validation

Fresh-context read-only Sol reviewer
`01a0ad23-3113-7003-a181-50319ae64ae5` independently checked the mathematical
claims, written files and primary sources. PASS, no findings. The reviewer
confirmed the full Mellin measure/sign, endpoint, prime-power terms, tail
normalization, and the distinction between a sufficient chosen family and
the published all-polynomial equivalence.

Lead: 38 focused/adjacent tests passed in normal and optimized modes (the new
7 tests plus Jordan, cutoff-normalized and complementary-divisor parents).
Reviewer: separately ran all 7 new tests in both modes; passed. No Qwen,
coefficient scan or numerical zeta-zero experiment was used. Review and finite
tests do not establish (5) or either conjecture.
