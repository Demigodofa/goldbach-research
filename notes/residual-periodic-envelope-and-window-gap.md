# The full residual has a negligible periodic envelope

Owner: Goldbach research. Parent: `d04c233e0d1b2f38cad4f9fee0789521585a8884`.
Purpose: distinguish arithmetic signs surviving complete-period averaging
from the incomplete reflected interval, and decide which one can contain
the unresolved adverse mass. Novelty label: `new-to-this-task`.

## Question and acceptance condition before computation

Can the full residual's complete-period reflected contribution be bounded
uniformly, even with absolute values on individual Ramanujan conductors?
Mechanism: exact Ramanujan diagonalization retains the target-dependent
arithmetic signs; uniform Mobius cancellation controls low conductors,
and a common-divisor tail controls high conductors.

Changed prediction: the periodic adverse mass itself is negligible. The
unresolved `O(N)` obstruction then lies in incomplete-period discrepancy,
not in an uncontrolled complete-period residual main. Required analytical
bound: `B_D(N)=O_(theta,J)(log(N)^(-J))` for every fixed `J>0`, pointwise
for all sufficiently large positive even `N`. A surviving low-conductor
main, an invalid unsmoothed lemma application, or an uncontrolled high
common-divisor tail falsifies that prediction.

Budget: the existing primary paper, one separate mathematical/source
review, and exact small kernel fixtures. No parameter scan. The earlier
Selberg coordinates and the older missing Q46189 window transfer motivate
the question; it is a new use of those facts, not a novelty claim about
Ramanujan sums. Creative tools checked: curiosity, inventive synthesis,
hypothesis preservation. Stop this lane after proving or falsifying the
periodic bound; do not substitute it for the Goldbach inequality.

## Actual residual and its exact periodic model

Fix `0<theta<1/2`, `R=floor(N^theta)`,
`I_N={n:N/3<n<2N/3}`, and `U=ceil(2N/3)-1`.
For all sufficiently large `N`, `1<R<U`. The coefficients

```text
b_d = mu(d)log(R/d) for R<d<=U; zero otherwise
```

give the ACTUAL residual from the preceding cutoff normalization on `I_N`:
`D(n)=sum_(d|n)b_d=Lambda(n)-Lambda_R(n)`. This uses all divisors above
`R` that could divide a central argument, not a selected middle band.
Outside that interval the finite periodic divisor sum need not equal the
same arithmetic residual. All averaging below is of that frozen finite sum.

Let `c_q(n)=sum_(a mod q,(a,q)=1) exp(2 pi i a n/q)` denote the real
integer Ramanujan sum, and define

```text
y(q) = sum_(q|d) b_d/d,
K_D(N) = sum_(d,e,(d,e)|N) b_d b_e/lcm(d,e),
B_D(N) = sum_(q<=U) |c_q(N)| y(q)^2.
```

For any finite real divisor coefficients, not only these Mobius weights,

```text
D(n) = sum_q y(q)c_q(n),
K_D(N) = sum_q c_q(N)y(q)^2.                             (1)
```

Indeed `sum_(q|g)c_q(N)=g*1_(g|N)` gives both identities after exchanging
finite sums. Equivalently, over a full common period,
`average_n c_q(n)c_r(N-n)=1_(q=r)c_q(N)`, so `K_D` is the exact mean
reflected product of the finite periodic model. Thus `|K_D|<=B_D`.
The ordinary norm instead has weight `phi(q)`; replacing `c_q(N)` by
`phi(q)` would erase the sign information being tested here.

## Primary input, including the unsmoothed estimate

Goldston and Yildirim, *Higher correlations of divisor sums related to primes
I: triple correlations*, Integers 3 (2003), A05, Lemma 2.1, printed p.16,
equations (2.11)--(2.13):
[primary paper](https://math.colgate.edu/~integers/d5/d5.pdf).
For `log k<=C log Y`, fixed `C`, its `j=0` case supplies

```text
F(Y,k) = sum_(a<=Y,(a,k)=1) mu(a)/a log(Y/a)
       = k/phi(k) + O_C(exp(-c_C sqrt(log Y))),
M(Y,k) = sum_(a<=Y,(a,k)=1) mu(a)/a
       = O_C(exp(-c_C sqrt(log Y))).                     (2)
```

The second formula is explicitly equation (2.13), not an unjustified
derivative of the first formula's error. The lemma's divisibility condition
is automatic at `j=0`. No two-prime estimate or large-shift pair theorem
is used in the periodic bound below.

## Low conductors: the mains cancel within each coefficient

Set `Q=sqrt R` and `L=1+log N`. Since the nonzero `b_d` have squarefree
indices, `y(q)=0` for nonsquarefree `q`. For squarefree `q<=Q`, write
`d=qa` and retain `(a,q)=1`. Exactly,

```text
y(q) = (mu(q)/q) [F(U/q,q) + log(R/U) M(U/q,q)
                                 - F(R/q,q)].           (3)
```

Here `R/q>=sqrt R`, `U/q>=R/q`, and
`log q/log(R/q)<=1`, so both uses of (2) have a fixed uniformity constant.
The two mains `q/phi(q)` cancel exactly. Since `|log(R/U)|<=log N`,

```text
|y(q)| << (L/q) exp(-c sqrt(log R))    (q<=Q).           (4)
```

On squarefree support `|c_q(N)|=phi((q,N))<=q`.
After squaring (4) and summing `1/q`, with a possible change of `c`,

```text
sum_(q<=Q) |c_q(N)| y(q)^2
    << L^3 exp(-c sqrt(log R)).                         (5)
```

This cancellation is inside each arithmetic coordinate. It does not rely
on favorable cancellation between positive and negative conductors.

## High conductors: the target divisor tail is uniform

For every `q<=U`, discarding signs gives

```text
|y(q)| <= (log N/q) sum_(a<=U/q) 1/a <= L^2/q.          (6)
```

On the squarefree support, `|c_q(N)|<=gcd(q,N)`. Extending a nonnegative
tail to all positive integers is therefore legitimate. For any real `Q>=1`,

```text
sum_(q>Q) gcd(q,N)/q^2
 = sum_(g|N) phi(g)/g^2 * sum_(h>Q/g) 1/h^2
 <= 2 tau(N)/Q.                                        (7)
```

The identity uses `gcd(q,N)=sum_(g|q,g|N)phi(g)`.
For `g<=Q`, the inner sum is at most `2g/Q`; for `g>Q`, it is at most
`2`. Both contributions for a single divisor are at most `2/Q` because
`phi(g)<=g`. In particular, divisors larger than the split are not omitted.
Combining (6)--(7) bounds the high-conductor envelope by
`2 tau(N)L^4/sqrt R`.

Thus, without normalizing by any observed prime mass, the bound is

```text
B_D(N) << L^3 exp(-c sqrt(log R)) + tau(N)L^4/sqrt R
       = O_(theta,J)(1/log(N)^J) for every fixed J>0.     (8)
```

The last implication uses the already established elementary
`tau(N)=N^o(1)` and fixed positive `theta`. Constants may depend on fixed
`theta,J`, never on the target. Therefore even the separately adverse
complete-period conductors have total mass `O_J(N/log(N)^J)` after
multiplication by `N/3`. This is an analytical bound, not a finite fitted cap.

## What remains after the periodic bound

For compatible `d,e`, let `q=lcm(d,e)` and let `r` be the exact residue
from the earlier CRT construction: `d|n` and `e|N-n`. With
`l=floor(N/3)+1`, the strict central count is

```text
L_N(d,e) = floor((U-r)/q) - floor((l-1-r)/q).
```

Define the weighted incomplete-period discrepancy, with all long divisors,

```text
E_D(N) = sum_(R<d,e<=U,(d,e)|N) b_d b_e
                    [L_N(d,e) - N/(3 lcm(d,e))].         (9)
```

It obeys the EXACT identity `C(D,D)=(N/3)K_D+E_D`. The preceding
cutoff-normalized reduction and the NEW envelope (8) prove

```text
Delta_0(N) = E_D(N) + O_(theta,J)(N/log(N)^J).            (10)
```

The equivalent spectral form keeps the missing interval kernel explicit:

```text
E_D = sum_(q,r) y(q)y(r) [sum_(n in I_N)c_q(n)c_r(N-n)
                         - (N/3)1_(q=r)c_q(N)].         (11)
```

This includes same-conductor endpoint discrepancy AND cross-conductor
couplings. Calling it only an off-diagonal error would be incorrect.
An open sufficient estimate is still, for some fixed `epsilon>0`,

```text
E_D(N) >= -(1-epsilon)H(N)                               (12)
```

for every sufficiently large positive even `N`. It would yield
`T_N>=epsilon H+o(H)>=(epsilon/2)H>0` eventually, using `H>=N/3`.
No bound (12), effective
starting point or finite remainder verification has been obtained.
The elementary per-cell error `<=1` is valid but its absolute coefficient
sum at full cutoff is too large to infer (12).

## A concrete failure of automatic period-to-window sign transfer

This small example is an arbitrary divisor sum, NOT the actual residual
`D`, and NOT a counterexample to Goldbach. It falsifies only automatic
transfer of complete-period positivity to a finite reflected interval.

Take `f(n)=c_15(n)` and `N=34`. Its divisor coefficients are
`{1:1, 3:-3, 5:-5, 15:15}`. Its only nonzero Selberg coordinate is
`y(15)=1`, and its complete-period reflected mean is `c_15(34)=1>0`.
But on the exact strict interval `12<=n<=22`,

```text
sum f(n)f(34-n) = 2*(-2-2-4+8-2) + 1 = -3.
```

The discrepancy relative to `(N/3)K` is `-3-34/3=-43/3`.
All coefficient indices lie below `U=22`. Thus this is an arithmetic
divisor-sum example within the same finite-window operator, not a geometry
analogy. It does not disprove a bound specific to the actual Mobius weights.

## Decision

Pursuit status: `changed-under-evidence`. The complete-period adverse
envelope is now controlled analytically, even without cancellation between
conductors. This removes a real periodic-density obligation and locates the
remaining signed problem in (9)/(11); it does not make that problem easier
by assertion. Retain the new bound and the exact interval operator.

Do not use complete-period positivity or energy as a substitute for the
missing interval estimate. A Q46189 transfer would have to bound (9) or
(11) on the actual coefficients and strict interval; it is not established.
The earlier finite-cutoff L2 obstruction, q286 zero-mass failures, and
the distinction from the old scale-`N` decomposition remain intact.
This is not a bound on q286's actual signed projected errors; no transfer
to those four-modulus channels is being asserted.
The full prove-or-disprove Goldbach objective remains open.

`ramanujan_density_channels` and `test_residual_periodic_kernel.py` check
exact identities and the finite sign-transfer falsifier. Tests do not prove
Lemma 2.1, the uniform envelope, or Goldbach. Source/math review and the
validation receipt are recorded separately in `notes/review-receipts.md`.
