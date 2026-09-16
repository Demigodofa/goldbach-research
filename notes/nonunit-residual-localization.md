# The actual reflected residual localizes to coprime arguments

Owner: Goldbach research. Parent: `c6e53a3783c8e764c5d3293b8adf5539ba87d652`.
Purpose: remove an actual arithmetic part of the unresolved residual sum,
not further refine an artificial countermodel. Novelty: `new-to-this-task`.

## Question declared before computation

For fixed `0<theta<1/2`, set `R=floor(N^theta)`,
`A_R(n)=sum_(d|n,d<=R)mu(d)log(R/d)` and `D_R=Lambda-A_R`.
Can the part of the signed reflected residual on `gcd(n,N)>1` be proved
negligible, uniformly for even `N`, leaving only the coprime arguments?

Mechanism: on multiples of a squarefree divisor `g|N`, express `A_R` as
an alternating family of cutoffs excluding primes dividing `g`. Prove that
their reflected leading terms are identical, then cancel them. Handle
overlaps by exact inclusion-exclusion and large divisors by counting.
Changed prediction and required analytical bound:

```text
sum_(N/3<n<2N/3, gcd(n,N)>1) D_R(n)D_R(N-n)
    = O_(theta,J)(N/log(N)^J)       for every fixed J>0.  (Goal)
```

Falsifiers: a nonuniform cutoff estimate, an uncancelled main, invalid
summation over common divisors, or a tail at scale N. Budget: one analytic
proof, exact algebra fixtures and a separate mathematical/source review.
No numerical caps, target scans or new countermodel refinements.
Creative tools checked: curiosity, inventive synthesis, hypothesis
preservation. The surviving squarefree Mobius sign is used explicitly.

## Source and scope

Use Goldston and Yildirim,
[Higher correlations of divisor sums related to primes I](https://math.colgate.edu/~integers/d5/d5.pdf),
Lemma 2.1, printed p.16, for `j=0,1`, with a fixed bound on
`log k/log Y`. The precise specializations are recorded in the parent
`cutoff-normalized-complementary-remainder.md`.
The Euler identity below is also (2.25), printed p.18, with `j=1`.
The restricted-shift Theorem 5.1 is NOT applied at shift `N` or `N/g`.

Throughout, `I_x` denotes the integer points in `(x/3,2x/3)`.
The original `N` is even, but `M=N/g` can be odd. None of the CRT or
excluded-prime calculations below assumes that M is even.
Write `L=1+log N`. All error constants are independent of the target;
dependence on fixed `theta,J` or a declared auxiliary exponent is allowed.

## Exact excluded-prime cutoff identity

For real `S>=1`, define

```text
F_S^(g)(m) = sum_(d|m,d<=S,(d,g)=1)mu(d)log(S/d),
```

and set this to zero for `S<1`. If `g` is squarefree, splitting each
squarefree divisor of `gm` as `h*d`, where `h|g` and `(d,g)=1`, gives

```text
A_R(gm) = sum_(h|g) mu(h) F_(R/h)^(g)(m).               (1)
```

This remains valid when `m` shares primes with g. No coprimality of `g,m`
is assumed. Squarefree support belongs to the divisor coefficients, not
to the integer argument `gm`.

## Uniform excluded-prime pair density

Take squarefree `g|N`, `g<=sqrt R`, `M=N/g`, and
`S=R/h`, `T=R/k` with `h,k|g`. In particular `sqrt R<=S,T<=R`.
Let

```text
K_g(S,T;M) = sum_(a<=S,b<=T,(a,g)=(b,g)=1,(a,b)|M)
               mu(a)mu(b)log(S/a)log(T/b)/lcm(a,b).
```

The exact strict-central CRT count differs from `M/(3*lcm(a,b))`
by at most one. Also `sum_(d<=S)|mu(d)|log(S/d)<=S` for real `S>=1`:
integrate `floor(t)/t<=1` from 1 to S. Therefore

```text
sum_(m in I_M) F_S^(g)(m)F_T^(g)(M-m)
    = (M/3)K_g(S,T;M) + O(S*T).                        (2)
```

Put `c=gcd(a,b)`, so `c|M` and `(c,g)=1`, and split at
`W=sqrt(min(S,T))>=R^(1/4)`. For `c<=W`, the exact density block is

```text
mu(c)^2/c * sum_(b<=T/c,(b,cg)=1) mu(b)/b log(T/(cb))
             * sum_(a<=S/c,(a,bcg)=1) mu(a)/a log(S/(ca)).
```

In the inner sum, `bcg<=T*g<=R^(3/2)`, while
`S/c>=sqrt(min(S,T))>=R^(1/4)`. Thus the source uniformity ratio is at
most 6. Lemma 2.1 with `j=0` replaces the inner sum by `bcg/phi(bcg)`
with error `O(exp(-c_0 sqrt(log R)))`, uniformly in all these indices.
Its accumulated error is `O(L^3 exp(-c_0 sqrt(log R)))`.

Since `(b,cg)=1`, the resulting outer sum has main form

```text
(g/phi(g)) * sum_(c|M,c<=W,(c,g)=1) mu(c)^2/phi(c)
                 * sum_(b<=T/c,(b,cg)=1)mu(b)/phi(b)log(T/(cb)).
```

Apply the same lemma with `j=1`, again with a fixed uniformity ratio.
Use `g/phi(g)<=L^2` (expand as a divisor sum and bound by
`sum_(d<=g)tau(d)/d`) and `sum_(c<=W)1/phi(c)<=L^2` on squarefree c.
The second accumulated error is `O(L^4 exp(-c_0 sqrt(log R)))`.

The discarded original tail is at most `tau(M)L^4/W`. The discarded
main tail is at most `2 L^2 tau(g)tau(M)^3/W`, using
`S_2(cg)<=2tau(cg)` and `1/phi(c)<=tau(c)/c` on squarefree c.
Since `tau(g),tau(M)<=tau(N)`, both tails are covered by the estimate below.

Finally, the exact finite Euler identity gives

```text
sum_(c|M,(c,g)=1) mu(c)^2 S_2(cg)/phi(c) = S_2(Mg)=S_2(N).
```

If g is odd, only even c contribute; if g is even, all contributing
arguments `cg` are even. Factoring the terms prime by prime gives the same
identity, including when M is odd. The full density estimate is

```text
K_g(S,T;M) = (g/phi(g))S_2(N) + O(E_N),
E_N = L^4 exp(-c_0 sqrt(log R)) + tau(N)^4 L^4/R^(1/4). (3)
```

The main is independent of BOTH cutoff choices. This uniformity is what
permits the cancellation; a separate fixed-g asymptotic would not suffice.

## Cancellation and inclusion-exclusion

Let `C_g(A,A)=sum_(n in I_N,g|n)A_R(n)A_R(N-n)`.
Scaling `n=gm` maps its strict endpoints exactly to `I_(N/g)`.
Equations (1)--(3) give, for `1<g<=sqrt R`,

```text
C_g(A,A) = (N/(3phi(g)))S_2(N) * (sum_(h|g)mu(h))^2
         + O((N/g)tau(g)^2 E_N + R^2*(sum_(h|g)1/h)^2).
```

The displayed main is zero for `g>1`. The CRT error follows from summing
`(R/h)(R/k)`; it does not cost `tau(g)^2 R^2` unnecessarily.

Overlaps of the nonunit sets must be retained. Exactly,

```text
1_((n,N)>1) = -sum_(g|rad(N),g>1,g|n)mu(g).             (4)
```

For the small-g part, the main-error multiplicity is controlled by

```text
sum_(g|rad(N))tau(g)^2/g
 <= sum_(g<=N)d_4(g)/g <= L^4.                         (5)
```

Here squarefree g has `tau(g)^2=4^omega(g)=d_4(g)`, and the last bound
comes from expanding into four harmonic sums. Using only `tau(N)=N^o(1)`
against the exponential source error would NOT justify arbitrary
logarithmic savings; the harmonic weight in (5) is essential.
The summed CRT errors are at most `R^2 tau(N)L^2`.

For `g>sqrt R`, use `|A_R(n)|<=tau(n)L`. For every fixed `delta>0`,
`tau(n)^2<<_delta N^delta` for `n<=N`. There are at most `2N/g`
central multiples of g. Hence the remaining inclusion-exclusion terms,
bounded absolutely, total at most
`O_delta(N^(1+delta)tau(N)L^2/sqrt R)`.

Writing `C_bad` for restriction to `(n,N)>1`, these estimates prove

```text
|C_bad(A,A)| <<_delta
    N L^8 exp(-c_0 sqrt(log R))
  + N tau(N)^4 L^8/R^(1/4)
  + R^2 tau(N)L^2
  + N^(1+delta)tau(N)L^2/sqrt R.                        (6)
```

Choose, for example, `delta=theta/8`. Since `R=N^(theta+o(1))`,
`theta<1/2`, and `tau(N)=N^o(1)`, each term in (6) is
`O_(theta,J)(N/log(N)^J)` for every fixed J. This is a signed estimate;
we have not replaced `C_bad(A,A)` by a sum of absolute products.

## Transfer from A to the actual residual

On the nonunit set, if `Lambda(n)>0` then n is a proper prime power,
or a prime dividing N. A central prime divisor p of N satisfies
`3/2<N/p<3`, so necessarily `N=2p`: the prime midpoint is the only case.
There are `O(sqrt N log N)` proper prime powers through N.
Using `|A_R(m)|<=tau(m)L`, for any fixed small `delta>0` we obtain

```text
|C_bad(Lambda,A)| + |C_bad(A,Lambda)|
 + |C_bad(Lambda,Lambda)| <<_delta N^(1/2+delta)L^3.      (7)
```

The nonunit set is reflection-stable, so its two mixed correlations agree.
The exact identity is

```text
C_bad(D,D) = C_bad(A,A)-2C_bad(A,Lambda)+C_bad(Lambda,Lambda).
```

Equations (6)--(7) prove (Goal), uniformly for all sufficiently large even N.
This is a new estimate for part of the ACTUAL arithmetic residual, not
an estimate for a reweighted prime model.

## What remains

Define `C_unit(D,D)=sum_(n in I_N,(n,N)=1)D_R(n)D_R(N-n)`.
The preceding exact decomposition and reviewed cutoff reduction yield

```text
Delta_0(N) = C_unit(D,D) + O_(theta,J)(N/log(N)^J).       (8)
```

The earlier periodic estimate also gives `E_D=C_unit(D,D)+O_J(N/log(N)^J)`.
A sufficient pointwise bound remains
`C_unit(D,D)>=-(1-epsilon)H(N)` for some fixed `epsilon>0` eventually.
It is still OPEN; no favorable sign on the coprime part is proved.

On these arguments every actual divisor of n or N-n is coprime to N,
and the two integers are mutually coprime. This observation does NOT
permit deletion of all `gcd(d,e)>1` terms from the original global CRT
discrepancy individually: the estimate is for an argument-restricted SUM,
after exact cancellations. Individual nonunit terms need not vanish;
at `N=60,R=7,n=30`, the actual residual is `log(7/5)`, not zero.

Pursuit: `changed-under-evidence`. The nonunit argument contribution is
controlled and no longer part of the open pointwise estimate. No absolute
nonunit-mass bound, Goldbach proof/disproof, effective threshold, finite
remainder closure, or Q46189 transfer follows. Keep the q286 missing-mass,
finite-cutoff L2 and reflection-thinning boundaries intact.

`nonunit_residual_localization.py` and its tests check cutoff identities,
excluded Euler factors, odd reduced targets, strict endpoints, overlap
corrections and exact residual algebra. They do not prove the analytical
errors through finite tests. Separate review is in `review-receipts.md`.
