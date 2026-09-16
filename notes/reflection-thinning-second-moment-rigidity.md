# The quadratic price of deleting reflected pairs

Owner: Goldbach research. Parent: `dc9d6657bcf8d8e77661b841b734fd8d6eb4b47c`.
Purpose: decide whether the preceding countermodel can retain the missing
scale-N second-moment information without a new arithmetic assumption.
Novelty label: `new-to-this-task`; no historical originality claim.

## Bounded question declared before computation

Can a nonnegative sequence on actual prime-power support remove central
pairs while preserving both first-moment prefixes and the second moment
to error `o(N)`? The preceding construction preserved only the leading
second moment, with an allowed `O(N)` difference.

Mechanism: combine the prime identity `Lambda(p)=log p`, partial summation,
and the least squared distance to a pair-free nonnegative vector.
Changed prediction: the refined second-moment discrepancy pays for the
removed pairs. The previous keep/double construction should pay their
entire ordered logarithmic mass, up to `o(N)`.
Required analytical bounds, before fixtures:

```text
|Q_N-V_N| << eta_N log N + sqrt N log(N)^3,
V_N >= (r_N/2) T_N                   if C_N(a,a)=0,
Q_N = T_N+o(N)                      for good keep/double orientations.
```

Definitions follow below. A valid pair-free vector violating the finite
distance floor, a missing midpoint term, or an uncontrollable cross term
would falsify the candidate. Budget: one proof, exact rational fixtures,
and one separate mathematical review. No constant or target scan.
Creative tools checked: curiosity, inventive synthesis, hypothesis
preservation. The old q286 missing-mass concern motivates testing the
logical bridge, rather than declaring a new statistic sufficient.

## Definitions and primary inputs

Let `N>=6` be even, `I_N={n:N/3<n<2N/3}`, and
`C_N(f,g)=sum_(n in I_N)f(n)g(N-n)`. Write

```text
T_N = sum_(n in I_N; n,N-n prime) log n log(N-n),
delta(n) = a(n)-Lambda(n),       0<=a(n)<=2Lambda(n),
eta_N = max_(N/3<=x<=2N/3) |sum_(n in I_N,n<=x)delta(n)|,
Q_N = sum_(I_N)[a(n)^2-Lambda(n)^2],
V_N = sum_(I_N)delta(n)^2,
r_N = log(N/3)/log(2N/3) = 1-O(1/log N).
```

The first theorem is local; `a` can depend on `N`. The later equivalence
explicitly concerns ONE global sequence. `T_N` counts ordered PRIME pairs;
proper prime powers are not silently included in it.

The prime number theorem supplies `pi(N)=O(N/log N)` and, in its usual
logarithmic-saving form, the refined one-point expansion below. A primary
reference already used in this route is Goldston and Yildirim,
[Integers 3 (2003), A05](https://math.colgate.edu/~integers/d5/d5.pdf),
equations (1.5) and (1.30), the latter with `q=1`.
We use no prime-pair asymptotic. The number of proper prime powers through
`N` is at most `sqrt N log_2 N`, by summing the elementary bounds
`N^(1/k)<=sqrt N` for `2<=k<=log_2 N`.

## Prime-supported quadratic rigidity

Polarization gives the exact identity

```text
Q_N = V_N + 2 sum_(I_N)Lambda(n)delta(n).                (1)
```

The cross term must not be dropped. On primes, `Lambda(n)=log n`; off
prime powers, `delta=0`; on proper prime powers, `|delta|<=Lambda<=log N`.
Consequently

```text
sum_(I_N)Lambda(n)delta(n)
 = sum_(I_N)log n delta(n) + O(sqrt N log(N)^3).         (2)
```

Let `l=floor(N/3)+1`, `U=ceil(2N/3)-1` and
`B(t)=sum_(l<=n<=t)delta(n)`. Discrete partial summation gives

```text
sum_(l<=n<=U)log n delta(n)
 = log U B(U) - sum_(n=l)^(U-1) log((n+1)/n) B(n).
```

The coefficients telescope to `log(U/l)<log 2`, hence

```text
|Q_N-V_N| <= 2(log N+log 2)eta_N
                 + O(sqrt N log(N)^3) =: error bound.  (3)
```

In particular, `eta_N=o(N/log N)` makes the right side `o(N)`.
The prior global AP-prefix estimate is more than sufficient: its `q=1`
term and subtraction of two prefixes give
`eta_N=O(N^(3/4)log(N)^(3/2))`.

This is a support-sensitive rigidity statement. It does not apply to an
arbitrary real vector, and is not the old generic residual-norm Cauchy bound.

## A pair-free sequence must pay a distance cost

If `C_N(a,a)=0`, every summand is nonnegative. For each distinct actual
prime pair `{p,q}` with `p+q=N`, at least one of `a(p),a(q)` is zero.
Its contribution to `V_N` is therefore at least
`min((log p)^2,(log q)^2)`. At a prime midpoint `p=N/2`, the weight must
also be zero, costing `(log p)^2` once, not twice.

Since both primes lie in `I_N`,

```text
min((log p)^2,(log q)^2) >= r_N log p log q.
```

Distinct pairs contribute twice to `T_N`. The midpoint contributes once
and obeys the same weaker bound. Thus, exactly,

```text
V_N >= (r_N/2) T_N.                                    (4)
```

For arbitrary finite nonnegative base weights `w`, the exact unconstrained
floor is `sum_(distinct positive pairs)min(w(n)^2,w(N-n)^2)+w(N/2)^2`.
It is attained by deleting the smaller endpoint, keeping the other, and
deleting the midpoint. This sharpness does NOT impose progression or mass
constraints and does not assert an optimal constant under those constraints.

Combining (3)--(4), a pair-free model with sufficiently small prefix error
and `Q_N=o(N)` forces `T_N=o(N)`. An upper bound `Q_N<=o(N)` suffices.
Conversely, where `T_N>=cN` for a fixed `c>0`, every such pair-free model
has `Q_N>=(c/2-o(1))N`. The latter is conditional on that target's pair
mass; it is not a newly proved lower bound for `T_N`.

## The exact price of the previous thinning

Use the pairwise keep/double construction from
`reflection-thinning-linear-input-obstruction.md`, including midpoint
deletion. Regardless of orientation, `delta^2=Lambda^2` on every colliding
endpoint and is zero elsewhere. For a distinct prime pair with
`u=log p`, `v=log q`, its distance cost is

```text
u^2+v^2 = 2uv+(u-v)^2.                                 (5)
```

The midpoint cost already equals its contribution to `T_N`. Also
`|u-v|<=log 2`, and each prime-pair product is at least `log(N/3)^2`.
The total excess in (5) is therefore `O(T_N/log(N)^2)`.
Collisions involving a proper prime power have at most twice as many
endpoints as there are proper powers, and contribute
`O(sqrt N log(N)^3)`. Hence

```text
V_N = T_N + O(T_N/log(N)^2 + sqrt N log(N)^3).           (6)
```

PNT gives `T_N<=pi(N)log(N)^2=O(N log N)`, so the excess is `o(N)`.
The good local orientation from the preceding concentration proof has
`eta_N=O(sqrt N log(N)^(3/2))`. Equations (3) and (6) now give

```text
Q_N = T_N + O(N/log N + sqrt N log(N)^3) = T_N+o(N).    (7)
```

This holds uniformly for even targets and good orientations, without the
earlier good-set condition `K_N=O(N/log(N)^2)`. At the selected targets of
the global construction, the whole central interval equals its local block,
so (7) also applies there. We have not proved `T_N` is of order `N` at all
or any particular selected targets.

## Exact boundary for strengthening the global countermodel

The following two statements are equivalent:

1. There is ONE global sequence `0<=a<=2Lambda` with the previous aggregate
   AP-prefix perturbation `O(X^(3/4)log(X)^(3/2))`, prefix second-moment
   discrepancy `sum_(n<=X)[a(n)^2-Lambda(n)^2]=o(X)`, and zero central
   reflected mass at infinitely many even targets.
2. `liminf_(even N -> infinity) T_N/N = 0`.

Forward: subtract the second-moment prefixes at the two central endpoints
to get `Q_N=o(N)`, and use `q=1` of the AP-prefix bound for (3). At every
pair-free target (4) implies `T_N=o(N)` along that unbounded sequence.

Reverse: select even `N_j` with `T_(N_j)=o(N_j)` and
`N_(j+1)>=4N_j`. No upper bound on their spacing is required. In each
disjoint `I_(N_j)`, choose a good ALL-MODULUS keep/double orientation from
the previous proof; leave `Lambda` unchanged outside the selected intervals.
The same geometric summation proves the stated global AP bound: there are
`O(log X)` blocks below `3X`, and their square-root sizes sum to `O(sqrt X)`.

On every modified point the absolute square change is at most
`3Lambda(n)^2`. Thus a whole or partial block has absolute second-moment
change at most `3V_(N_j)=o(N_j)` by (6). For any fixed `epsilon>0`, all
sufficiently late blocks cost at most `epsilon N_j`; their sizes through
`3X` sum to `O(X)`, and finitely many earlier blocks cost `O(1)=o(X)`.
Letting `epsilon` tend to zero proves the global prefix `o(X)` claim.
This constructs the single sequence in statement 1 and closes the converse.

The condition in statement 2 is OPEN in this research. It is not equivalent
to a Goldbach counterexample: positive pair mass can be `o(N)` without being
zero. Conversely, ruling out statement 2 would give a positive linear lower
bound eventually for these strict-central weighted prime pairs, which is
stronger than mere existence of a representation.

## What the refined one-point formula does not prove

The actual second moment itself is not an unknown. PNT with logarithmic
savings, partial summation, and the proper-power bound give

```text
sum_(I_N)Lambda(n)^2
 = (N/3)log N + ((2log 2-log 3-1)/3)N + o(N).           (8)
```

To see this, replace `Lambda^2` by `Lambda log n` up to
`O(sqrt N log(N)^3)`, then integrate `log t` against
`sum_(n<=t)Lambda(n)=t+O_A(t/log(t)^A)` at the two central endpoints.
Endpoint rounding costs only `O(log(N)^2)`. This uses no binary estimate.

Knowing (8) for `Lambda` does not grant the same formula to `a`. The latter
is precisely the extra assumption in the equivalence. Formula (7) identifies
what a naive transfer would erase: the real pair mass at scale `N`.
The model was defined by consulting colliding pairs; its norm discrepancy
is not an independent way to compute or lower-bound their mass.

## Decision

Pursuit: `changed-under-evidence`. The scale-N second-moment information is
a genuine discriminator, not a cosmetic tightening of the leading norm.
The original countermodel remains valid exactly as stated. Strengthening it
to prefix second-moment error `o(X)` while retaining infinitely many pair-free
targets is now pinned to an explicit, unresolved density-collapse condition.
Do not assert that strengthening for free or silently use (8) for the model.

This proves neither a favorable actual reflected-residual estimate nor a
Goldbach counterexample. The actual `E_D` gate, effective starting point,
finite remainder, q286 zero-mass obstruction and Q46189 transfer gap remain
open. A next proof attempt still needs independently justified signed
arithmetic information, not merely this diagnostic identity.

`reflection_thinning.py` and `test_reflection_thinning_rigidity.py` check
finite polarization, pair-deletion costs, midpoint accounting, collision
energy and summation by parts. They do not prove asymptotics by examples.
Separate mathematical review and validation are in `review-receipts.md`.
