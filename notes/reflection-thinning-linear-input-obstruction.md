# Reflection thinning saturates the one-prime-input relaxation

Owner: Goldbach research. Parent: `449a1a7713ca76ce2ee5af0a71f0e20a71185789`.
Purpose: determine whether the retained linear distribution estimates and
leading one-point moments alone force the missing positive margin.
Novelty: `new-to-this-task`; this is an elementary probabilistic construction,
not a claim of historical originality or a general sieve-parity theorem.

## Question declared before computation

Can a nonnegative reweighting of actual prime-power support eliminate all
central reflected pairs while retaining the one-prime progression inputs?
Mechanism: independently choose one endpoint of each already-colliding
reflected pair, doubling its original weight and deleting the other.
The expectation keeps each noncentral-fixed-point weight unchanged;
a simultaneous concentration bound controls all relevant linear tests.

Changed prediction: the relaxed inputs permit a residual correlation
`-H+o(N)`, so they cannot force `>=-(1-epsilon)H` for fixed `epsilon>0`.
Required bound, before any fixture: the sum over `q<=sqrt N` of maximum
progression-prefix perturbations must be
`O(N^(3/4)log(N)^(3/2))`, smaller than `N/log(N)^J` for every fixed `J`.
A failed simultaneous bound, a surviving midpoint pair, or incompatible
support/moment requirements would falsify the construction as stated.

Budget: one analytic construction, one separate mathematical review, and
exact finite algebra fixtures. No random search, cutoff scan or prime-pair
horizon extension. This connects the old zero-mass logical concern with
the new exact residual gate; the model has substantial one-prime mass,
unlike simply setting every mass to zero. Creative tools checked: curiosity,
inventive synthesis, hypothesis preservation. Stop after deciding this
specified relaxation, without claiming the actual arithmetic gate is false.

## What the theorem does and does not construct

Let `Lambda` be the actual von Mangoldt function on the positive integers, and use
the strict interval `I_N={n:N/3<n<2N/3}` for even `N>=6`.
First construct a finite measure `a_N`, then glue disjoint instances into
ONE globally defined nonnegative sequence `a(n)`. It satisfies
`0<=a(n)<=2 Lambda(n)`: only weights on actual prime powers change, and no
composite outside that support is added. Positive support is a subset,
not necessarily equal. This is a weighted sequence, not alternate primes.

The construction does NOT preserve exact values `Lambda(p)=log p`, the
full frozen Mobius identity, multiplicativity-type identities, or all
lower-order terms of higher moments. The existing periodic-envelope theorem
concerns the actual Mobius coefficients; it is not asserted for this model.
These exclusions are part of the theorem, not omitted loopholes.

## Pairwise construction

Partition the distinct pairs `{n,m}` with `n,m in I_N`, `n+m=N`, and
`Lambda(n)Lambda(m)>0`, taking `n<m`. Assign an independent uniform sign
`sigma_{n,m} in {-1,1}` to each. All randomness is in the constructed
weights; no randomness or independence of the primes is assumed. Define

```text
a_N(n) = (1+sigma_{n,m})Lambda(n),
a_N(m) = (1-sigma_{n,m})Lambda(m).
```

Leave all other weights equal to `Lambda`, except set `a_N(N/2)=0`.
The fixed midpoint cannot be assigned a two-endpoint sign and must be
removed separately. Then, for EVERY orientation of the signs,

```text
C(a_N,a_N) = sum_(n in I_N)a_N(n)a_N(N-n) = 0.           (1)
```

All noncolliding endpoints, including those outside `I_N`, remain unchanged.
The only deterministic expectation bias is the removed midpoint.

## Simultaneous progression control, proved directly

For integers `q>=1`, `0<=r<q`, `0<=x<=N`, let

```text
Z(q,r,x) = sum_(n<=x,n=r mod q) [a_N(n)-Lambda(n)].
```

Write `1_B` for membership in this progression prefix. Exactly,

```text
Z = sum_(pairs n<m) sigma_{n,m} v_{n,m} + beta,
v_{n,m} = Lambda(n)1_B(n)-Lambda(m)1_B(m),
beta = -Lambda(N/2)1_B(N/2).                             (2)
```

Because the endpoint weights are nonnegative,
`(u-v)^2<=u^2+v^2`, so the variance proxy is bounded by

```text
V=sum v_{n,m}^2 <= sum_(n in B)Lambda(n)^2
                <= (N/q+1)log(N)^2.                    (3)
```

This keeps the negative covariance when both endpoints lie in the same
prefix. It does not incorrectly model the endpoints as independent.
Also `|beta|<=log N`.

Here is the concentration proof, requiring no uncited probabilistic input.
For independent signs, the exponential moment is `product cosh(t v)`.
The inequality `cosh u<=exp(u^2/2)` follows by integrating
`tanh u<=u` for `u>=0` and using evenness. Markov's inequality, optimized
at `t=z/V`, therefore gives

```text
Pr(|sum sigma v|>=z) <= 2 exp(-z^2/(2V)).                (4)
```

If `V=0`, the sum is identically zero. For every `1<=q<=N`, put

```text
t_q = log N * sqrt(12 (N/q+1)log(2N)).
```

For each triple, (3)--(4) give failure probability at most `2(2N)^(-6)`.
There are at most `(N+1)sum_(q<=N)q<=2N^3` triples. The union bound is
at most `4N^3/(2N)^6<1`; hence an orientation exists for which

```text
max_(r,x) |Z(q,r,x)| <= t_q+log N       for every q<=N.  (5)
```

No independence between different progression tests is needed. The
all-modulus form will permit gluing the blocks below. In particular,
restricting now to `Q=floor(sqrt N)` and summing
`sqrt(N/q+1)<=sqrt(N/q)+1` and `sum_(q<=Q)q^(-1/2)<=2sqrt Q` proves

```text
sum_(q<=sqrt N) max_(r,x)|Z(q,r,x)|
    << N^(3/4)log(N)^(3/2)
     = o(N/log(N)^J) for every fixed J>0.               (6)
```

An integer prefix suffices, since both finite sums are step functions.
This is deterministic existence by the probabilistic method, not an
assertion that every orientation satisfies (5).

## Transfer of the actual one-prime estimates

The established progression input for `Lambda` is Bombieri-Vinogradov at
every fixed level below `1/2`; a sufficient primary statement is equation
(1.30), printed p.8, in
[Goldston and Yildirim, Integers 3 (2003), A05](https://math.colgate.edu/~integers/d5/d5.pdf).
The ordinary prime number theorem is also used below. The source is not
being cited for the new reweighting construction.

Equation (6) transfers the available progression estimates to `a_N` with
an additional error smaller than every fixed logarithmic saving. This
claim applies where the ORIGINAL estimate for `Lambda` is valid; it does
not extend its level of distribution. Both strict central endpoints are
comparable to `N`, so the preceding mixed-term argument is covered.

More directly, for fixed `0<theta<1/2`, `R=floor(N^theta)`, put
`A_R(n)=sum_(d|n,d<=R)mu(d)log(R/d)`. Reflection and (5) imply

```text
|C(A_R,a_N)-C(A_R,Lambda)|
 <= 2 log R * sum_(d<=R) max_(r,x)|Z(d,r,x)|
 << sqrt(NR)log(N)^(5/2)
  = o(N/log(N)^J) for every fixed J>0.                  (7)
```

The factor two is for the difference of the endpoint prefixes. The same
chosen orientation works for all such cutoffs, since (5) covers every
`d<=sqrt N`. The constants in the final asymptotic may depend on fixed
`theta,J`.

The reviewed actual estimates `C(A_R,Lambda)=H+O_J(N/log(N)^J)` and
`C(A_R,A_R)=H+O_J(N/log(N)^J)` now give, for `F_N=a_N-A_R`,

```text
C(F_N,F_N) = -H(N)+O_(theta,J)(N/log(N)^J).              (8)
```

Here (1) is exact. Thus for any fixed `epsilon>0`, the desired bound
`C(F_N,F_N)>=-(1-epsilon)H` fails eventually for these pair-free models,
using `H>=N/3` to compare the errors. All linear mixed inputs have been
retained. This does not apply (8) to the actual `D=Lambda-A_R`.

## Leading one-point moments can also be retained

Let `K_N` count ordered central endpoints with
`Lambda(n)Lambda(N-n)>0`, including the midpoint if positive. The number
of prime powers up to `2X` is `O(X/log X)`: use PNT for primes and the
elementary `O(sqrt X log X)` bound for proper powers. Each ordered pair
determines its sum, so

```text
sum_(even N in [X,2X]) K_N << X^2/log(X)^2.              (9)
```

Since there are order `X` even targets, there is a fixed constant `C_0`
such that the set `G={even N: K_N<=C_0 N/log(N)^2}` meets every sufficiently
large dyadic block. In particular `G` is unbounded. This is an averaging
argument, not a Goldbach asymptotic or a finite search for good targets.

For `N in G`, any orientation changes at most `K_N+1` weights, each at
most `log N` originally and at most `2 log N` afterward. For each fixed
integer `k>=2`,

```text
|sum_(I_N)a_N(n)^k - sum_(I_N)Lambda(n)^k|
 <= sum_(I_N)|a_N(n)^k-Lambda(n)^k|
 <= (2^k+1)(K_N+1)log(N)^k
  = O_k(N log(N)^(k-2)).                               (10)
```

The actual leading moment, by PNT, is
`sum_(I_N)Lambda(n)^k ~ (N/3)log(N)^(k-1)`. Proper prime powers are
lower order. Equation (10) therefore preserves EVERY fixed leading
one-point moment on `G`; it does not preserve the lower-order terms.
The first moment is preserved more accurately by (5) with `q=1`.

## Gluing into one globally consistent sequence

For each sufficiently large integer `j`, select
`N_j in G intersect [8^j,2*8^j]`. This is possible by (9).
Then `N_(j+1)>=4N_j`, so the strict intervals `I_(N_j)` are disjoint.
For each selected target, choose an orientation satisfying the ALL-MODULUS
bound (5), using the original `Lambda` weights. Define `a(n)=a_(N_j)(n)`
inside its interval, and `a(n)=Lambda(n)` elsewhere. There is no conflict
between these definitions. This is a single sequence on all positive
integers, with `0<=a<=2Lambda`, and

```text
C_(N_j)(a,a)=0 for every selected target N_j.            (11)
```

Here the subscript emphasizes the target of reflection. Both endpoints
are in the same selected interval, so other blocks cannot restore a pair.

For a global prefix bound `X`, only blocks with `N_j<3X` can contribute.
Put `L_j=log(2N_j)`. When `q<=N_j`, (5) bounds any block's contribution
in every residue and prefix by `O(L_j^(3/2)(sqrt(N_j/q)+1))`.
For `q>N_j`, a progression contains at most one changed integer of that
block, so its contribution is at most `log N_j`; the same bound remains
valid. Thus the global perturbation satisfies

```text
sum_(q<=sqrt X) max_(r,0<=x<=X)
 |sum_(n<=x,n=r mod q)[a(n)-Lambda(n)]|
 << X^(1/4) sum_(N_j<3X) sqrt(N_j)L_j^(3/2)
       + sqrt X sum_(N_j<3X)L_j^(3/2)
 << X^(3/4)log(X)^(3/2) + sqrt X log(X)^(5/2)
 << X^(3/4)log(X)^(3/2).                                (12)
```

The first sum is dominated by its largest geometric scale, and there are
`O(log X)` blocks in the second. The last step uses `log X=O(X^(1/4))`.
Maxima over residues and prefixes are bounded by the sum of the individual
block maxima; no independence between blocks is needed after selection.
This proves that the SINGLE sequence inherits the available PNT and
Bombieri-Vinogradov estimates, not just a collection of finite models.

For every fixed `k>=2`, the same geometric summation of the absolute
moment-change bound on each block gives

```text
|sum_(n<=X)[a(n)^k-Lambda(n)^k]|
 <= sum_(N_j<3X) O_k(N_j log(N_j)^(k-2))
  = O_k(X log(X)^(k-2)).                                (13)
```

It also bounds a partial block, since (10) was bounded by the sum of
absolute pointwise changes. Subtracting the two endpoint-prefix formulas
shows that ALL central targets retain the fixed leading one-point moments,
not only the selected targets. The first moment has the stronger bound (12).

The global mixed reflected error is at most `2 log R` times the sum in
(12) at `X=N`, hence is `O(N^(3/4)log(N)^(5/2))=o(N/log(N)^J)`.
Consequently, for the global `F=a-A_R`,

```text
C_(N_j)(F,F)=-H(N_j)+O_(theta,J)(N_j/log(N_j)^J).         (14)
```

The global sequence also retains the earlier finite-cutoff leading ordinary
Gram data: `<a,a>~(N/3)log N` by (13); on primes `A_R(p)=log R`, so
`<A_R,a>~(N/3)theta log N` by the first-moment estimate.
The proper-power contribution is `o(N)` using `a<=2Lambda` and
`|A_R(n)|<=tau(n)log N`. The pure `<A_i,A_j>` data is unchanged.
Consequently the old leading norm floor does not distinguish this family
from the actual one. Lower-order information at scale `N` might distinguish
them, and is not ruled out by this argument.

## Decision and exact exclusions

Pursuit: `changed-under-evidence`. The endpoint `-H` is attainable in the
relaxation retaining these one-prime progression inputs, actual prime-power
support, and fixed leading moments, with ONE globally consistent sequence
attaining it along infinitely many targets. Merely combining those inputs cannot
prove a fixed positive gap in that relaxation. This is stronger than an
abstract zero-mass vector: the one-prime mass and distribution survive.

The construction deliberately consults actual colliding pairs and changes
their weights. It is an existence countermodel for a logical implication,
not a procedure for disproving Goldbach or discovering the real pairs.
It does not satisfy the exact frozen Mobius identity. Therefore it is NOT
a countermodel to the full current arithmetic route, the actual periodic
envelope theorem, or a correctly proved estimate for the actual `E_D`.
Do not call it a universal impossibility theorem or a new parity barrier.

Reactivation of a route using these statistics needs an explicitly retained
arithmetic identity, lower-order constraint or
other information that this family does not preserve, plus a demonstrated
use of that information. Naming such an ingredient alone does not solve
the gap. The full prove-or-disprove Goldbach goal, q286 zero-mass boundary,
Q46189 transfer gap and absence of an effective threshold remain unchanged.

`reflection_thinning.py` and its tests check deterministic pair deletion,
the fixed midpoint, exact progression forms and variance proxies, moment
support and the residual identity. They do not prove the concentration
theorem by finite examples. Review and validation are recorded separately.
