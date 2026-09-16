# Cutoff normalization removes the separate main and mixed obligations

Owner: Goldbach research. Parent: `b1a17f9755aa2e0de2111600a1b750b7a16634a2`.
Purpose: use the freedom in the exact frozen divisor identity to identify
the genuinely unresolved complementary correlation. This is a new-to-this-task
application of classical estimates, not a novelty claim or Goldbach proof.

## Question declared before computation

The full frozen divisor sum is independent of its scale. Can choosing the
scale equal to the cutoff put the main and mixed terms within known uniform
estimates, rather than treating all three terms as new unknowns?

Mechanism: normalize the short part to the standard truncated von Mangoldt
sum, use a common-divisor split for its binary density, and use average
prime distribution in progressions for the mixed correlation. Prediction:
both terms have the same independent main `H(N)`, leaving one residual
correlation. Falsifier: an invalid uniformity hypothesis, an uncontrolled
common-divisor tail, or a missing prime-power/endpoint contribution.
Budget: one primary paper, one separate mathematical/source review, and
small identity tests; no parameter scans. Sleep the claim if its uniform
source hypotheses cannot be met. The recent mapping prompted the question;
the older exact scale freedom, not a visual analogy, supplies the mechanism.

## Primary inputs and the restriction not being bypassed

Goldston and Yildirim, *Higher correlations of divisor sums related to primes
I: triple correlations*, Integers 3 (2003), A05:
[primary paper](https://math.colgate.edu/~integers/d5/d5.pdf).
Lemma 2.1, printed p.16, supplies, for fixed `j=0,1` and
`log k <= C log Y` with fixed `C`,

```text
sum_(d<=Y,(d,k)=1) mu(d)/phi_j(d) log(Y/d)
    = S_(j+1)(k) + O_C(exp(-c_C sqrt(log Y))).              (L)
```

On squarefree inputs `phi_0(d)=d`, `phi_1(d)=phi(d)`;
`S_1(k)=k/phi(k)`, and `S_2` is the binary singular series (zero for odd
arguments). These specializations meet the lemma's `p(j)|k` condition.
Equation (1.30), printed p.8, gives the unconditional Bombieri-Vinogradov
input at level below `1/2`, with maximum over reduced residues and arbitrary
fixed logarithmic savings. These are established external inputs.

The paper's pair-correlation Theorem 5.1 has `|k|<=R`. We do NOT substitute
`k=N` into it when `R=N^.32`. The uniform extension needed here is proved
below directly from (L). No fixed-shift asymptotic is silently made uniform.

## Normalization and exact identity

Fix `0<theta<1/2`, let `R=floor(N^theta)`, and let `N` tend to infinity
through positive even integers. All constants below may depend on fixed
`theta` and the requested logarithmic saving, never on the target `N`.
Put `I_N={n:N/3<n<2N/3}`, `H(N)=S_2(N)N/3`, and

```text
C(f,g) = sum_(n in I_N) f(n)g(N-n),
A(n) = sum_(d|n,d<=R) mu(d)log(R/d),
D(n) = Lambda(n)-A(n) = sum_(d|n,d>R) mu(d)log(R/d).
```

The last identity holds for `n>1`, hence throughout `I_N` for `N>=6`.
It uses the already proved full frozen identity, not a prime-pair assumption.
This changes the decomposition, not the original arithmetic sum. If
`M_R(n)=sum_(d|n,d<=R)mu(d)`, the previous scale-`N` short part satisfies
`A_old=A+log(N/R)M_R`; its long part changes by the negative of that term.
We do not assert a new bound for the old scale-`N` density separately.

## The short-short density is uniform in the target

Define

```text
K_R(N) = sum_(d,e<=R,(d,e)|N)
           mu(d)mu(e)log(R/d)log(R/e)/lcm(d,e).
```

The strict-interval CRT count from the preceding checkpoint gives

```text
C(A,A) = (N/3)K_R(N) + O(R^2).                            (1)
```

Indeed the progression error is at most one and
`sum_(d<=R)|mu(d)|log(R/d) <= sum_(d<=R)log(R/d) <= R-1`
for integer `R>=1`, by comparing `log(R!)` to the integral of `log t`.

Write `d=ga`, `e=gb`, where `g=gcd(d,e)|N`. The nonzero Mobius weights
force `g,a,b` squarefree and pairwise coprime. Put `Y=R/g`,
`L=1+log R`, and split at `g=sqrt(R)`.

For the small-common-divisor part, its exact expansion is

```text
sum_(g|N,g<=sqrt(R)) mu(g)^2/g
  * sum_(b<=Y,(b,g)=1) mu(b)/b log(Y/b)
  * sum_(a<=Y,(a,bg)=1) mu(a)/a log(Y/a).                 (2)
```

Here `Y>=sqrt(R)` and `bg<=R`, so `log(bg)<=2 log Y`.
Apply (L) with `j=0` to the innermost sum. Its main is `bg/phi(bg)`.
Since `(b,g)=1`, the main of (2) becomes

```text
sum_(g|N,g<=sqrt(R)) mu(g)^2/phi(g)
  * sum_(b<=Y,(b,g)=1) mu(b)/phi(b) log(Y/b).
```

Apply (L) with `j=1`, now with `log g<=log Y`. The result is

```text
sum_(g|N,g<=sqrt(R)) mu(g)^2 S_2(g)/phi(g)
    + O(L^3 exp(-c sqrt(log R))).                         (3)
```

For completeness, the first accumulated error uses
`sum_(b<=Y)log(Y/b)/b <= L^2` and `sum_(g<=sqrt R)1/g<=L`.
The second uses `1/phi(g)<=tau(g)/g` on squarefree `g` and
`sum_(g<=sqrt R)tau(g)/g<=L^2`. The uniformity constants in (L) are fixed.

The discarded original part `g>sqrt(R)` has absolute value at most
`tau(N)L^4/sqrt(R)`, after dropping coprimality and signs. Its corresponding
main tail is at most `2 tau(N)^3/sqrt(R)`, because
`S_2(g)<=2 tau(g)`, `1/phi(g)<=tau(g)/g`, and `tau(g)<=tau(N)` when `g|N`.

There is an exact Euler-product collapse:

```text
sum_(g|N) mu(g)^2 S_2(g)/phi(g) = S_2(N).                 (4)
```

For even `N`, only even squarefree `g` contribute. After factoring out
`2C_2`, the sum is `product_(p|N,p>2)(1+1/(p-2))`, precisely the singular
series multiplier. Repeated prime factors of `N` do not change the product.
For odd `N`, both sides are zero.
This same Euler collapse is used in the primary paper's proof of Theorem 5.1;
the new-to-this-task step is the target-uniform common-divisor tail control.

We have therefore proved the quantitative uniform bound

```text
K_R(N) = S_2(N)
   + O(L^3 exp(-c sqrt(log R)) + tau(N)^3 L^4/sqrt(R)).    (5)
```

The elementary bound `tau(N)=N^o(1)` is sufficient: for every `eta>0`,
large primes obey `a+1<=2^a<=p^(eta*a)` and each of the finitely many
smaller primes contributes a bounded factor in `(a+1)/p^(eta*a)`.
Their product gives `tau(N)<=C_eta N^eta`.
Consequently, for every fixed `J>0`, (1) and (5) give

```text
C(A,A) = H(N) + O_(theta,J)(N/(log N)^J).                 (6)
```

The cutoff `theta=8/25` works, but nothing was optimized or fitted to it.

## The mixed term has the same main

Expanding the short factor and reflecting the strict interval gives

```text
C(A,Lambda) = sum_(d<=R) mu(d)log(R/d)
                sum_(m in I_N,m=N mod d) Lambda(m).       (7)
```

Let `u=ceil(2N/3)-1`, `l=floor(N/3)+1`. For `(d,N)=1`, the inner sum
is `psi(u;d,N)-psi(l-1;d,N)`. Apply Bombieri-Vinogradov at both endpoints,
which are comparable to `N`. Since `theta<1/2`, `R` lies below their
permitted modulus range with a fixed power margin. The residue `N mod d`
may change with `N`: the theorem's maximum over reduced residues covers it.
Multiplication by `|mu(d)log(R/d)|<=log R` costs one logarithm only.

For `(d,N)>1`, a contributing prime would divide `d`, hence be at most
`R<N/3` for large `N`, outside `I_N`. The remaining contributions are
proper prime powers. A deliberately coarse bound for their total in (7) is
`O(R sqrt(N) log(N)^3)`, from at most `sqrt(N)floor(log_2 N)` such integers
up to `N`, each weighted by at most `log N`, for each of the `R` divisors.
This is smaller than `N/(log N)^J` for every fixed `J`, because `theta<1/2`.

The scalar main in (7) is

```text
W_R(N) = sum_(d<=R,(d,N)=1) mu(d)log(R/d)/phi(d)
       = S_2(N) + O_theta(exp(-c_theta sqrt(log R))),      (8)
```

by (L) with `j=1`: `log N <= C_theta log R` for all large `N`.
The integer interval length differs from `N/3` by at most a constant;
the resulting error is `O(L^3)`, using the absolute scalar sum and
`1/phi(d)<=tau(d)/d` on its squarefree support.
Together these estimates prove, for every fixed `J>0`,

```text
C(A,Lambda) = H(N) + O_(theta,J)(N/(log N)^J),
C(A,D) = O_(theta,J)(N/(log N)^J).                        (9)
```

No distribution of TWO primes has been assumed. The only prime-distribution
input in this step is the established average over progression moduli.

## What is now the one remaining estimate?

Let `T_N` be the ordered prime-only central log mass and
`P_N=C(Lambda,Lambda)-T_N`. The previous elementary bound gives
`0<=P_N<=2 sqrt(N)floor(log_2 N)log(N)^2`.
The exact relation, before discarding any error, is

```text
Delta_0 = C(D,D) + 2[C(A,Lambda)-H] - [C(A,A)-H] - P_N.
```

Thus (6) and (9) prove the reduction

```text
Delta_0(N) = C(D,D) + O_(theta,J)(N/(log N)^J)             (10)
```

for every fixed `J>0`, pointwise through all sufficiently large even `N`.
This removes the separate main adjustment and mixed-term obligations in
the NEW normalization. It does not estimate the residual correlation.

A still-unproved sufficient bound is, for some fixed `epsilon>0`,

```text
C(D,D) >= -(1-epsilon)H(N)                               (11)
```

for all sufficiently large even `N`. Since `S_2(N)>=1`, (10)--(11)
would give positive central prime mass eventually. A finite remainder would
still require verification; no effective numerical starting point is supplied
here. A mere absolute or L2 bound at a larger scale
does not establish (11); nor does a finite fitted cap. No Q46189 energy
transfer to (11) is proved. For q286, multiply (10) by `M(a)` and retain
its `sum U_d` term; that additional projected error has not disappeared.

## Decision and validation boundary

Pursuit status: `changed-under-evidence`.
The frozen-scale choice connects the
previous exact identity to established estimates and a target-uniform
common-divisor argument. It is a useful theorem reduction, not a claim that
the remaining Goldbach-strength problem is easy or historically new.
No numerical success criterion was used. The next question should address
signed `C(D,D)` or test a different mechanism with greater information value.

`cutoff_normalized_remainder.py` and its tests check the exact Euler collapse,
common-divisor grouping, scale change, and residual identity. Finite tests
do not establish (L), Bombieri-Vinogradov, or any asymptotic uniformity; those
come from the cited inputs and the proof above. Independent review and final
validation results are recorded in `notes/review-receipts.md`.
