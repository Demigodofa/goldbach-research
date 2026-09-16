# Finite cutoff mixing cannot remove the signed residual

Owner: Goldbach research. Parent: `64e5a694f130c4825f8fc12e7a5f79092df60ae2`.
Purpose: decide whether the newly available cutoff freedom can cancel the
remaining correlation or make a plain norm bound useful. This note records
an analytical obstruction for a specified family, not a Goldbach proof or
an impossibility theorem for multiscale methods. Novelty: `new-to-this-task`.

## Question declared before computation

Can finitely many cutoff residuals be mixed, allowing negative coefficients,
to cancel their fluctuations while preserving the prime signal? The bridge
is linear filtering across the free frozen scales. A successful prediction
would be a fixed-fraction gain in the reflected lower bound, or a norm small
enough for Cauchy to give that gain. The required bound remains
`C(E,E)>=-(1-epsilon)H` for a signal-preserving mixture and some fixed
`epsilon>0`, eventually at every positive even target.

Falsifier: all these residuals have the same leading reflected correlation,
and their best possible ordinary norm is still of order `N log N`.
Budget: one analytic derivation using the preceding primary source, one
separate math/source review, and exact small algebra fixtures; no constant
or target scans. Sleep this linear-mixture shortcut if the falsifier is
proved. Curiosity connects the earlier failed L2 shortcut with the newly
proved scale freedom; this is not a claim of an independently arising idea.
Creative tools checked: curiosity, inventive synthesis, hypothesis preservation.

## Scope and notation

Use the preceding note's `I_N`, `H=S_2(N)N/3`, `T_N`, `Delta_0=T_N-H`,
and reflected bilinear form `C(f,g)=sum_(n in I_N)f(n)g(N-n)`.
The ordinary inner product is instead `<f,g>=sum_(n in I_N)f(n)g(n)`.
Keep these two forms distinct.

Fix a finite strictly ordered set `0<theta_1<...<theta_k<1/2`. Put
`R_i=floor(N^theta_i)`, `A_i=Lambda_(R_i)`, and `D_i=Lambda-A_i`.
All asymptotics below are pointwise as positive even `N` tends to infinity.
Constants can depend on the fixed exponents and fixed requested log saving.
Coefficients `c_i` may depend on `N`, but must be uniformly bounded; `k`
and the exponents do not vary. Write

```text
s = sum_i c_i,       E = Lambda - sum_i c_i A_i.
```

For `s=1`, this is precisely `sum_i c_i D_i`. Unbounded weights, an
increasing number of cutoffs, nonlinear arithmetic weights, and new signed
information are outside this claim.
For a general linear combination of the `D_i` with nonzero coefficient
sum, first divide by that sum to preserve the coefficient of `Lambda`;
both correlation and required threshold rescale by its square. This stays
within the proved asymptotic class only if the normalized weights remain
uniformly bounded: a nonzero sum tending to zero can violate that condition.
A zero coefficient sum removes `Lambda` exactly.

## Cross-cutoff reflected estimate

Let `R<=S` be any two of the cutoffs. The rectangular CRT density is

```text
K_(R,S)(N) = sum_(d<=R,e<=S,(d,e)|N)
               mu(d)mu(e)log(R/d)log(S/e)/lcm(d,e).
```

The exact progression-count error is at most one, so
`C(A_R,A_S)=(N/3)K_(R,S)+O(RS)`. The coefficient absolute sums are at
most `R-1` and `S-1`, respectively.

The preceding common-divisor proof extends with `g=gcd(d,e)<=sqrt(R)`:
write `d=ga,e=gb`. In the inner `a` sum the logarithmic scale is `R/g`
and the coprimality parameter is `bg<=S`. Thus
`log(bg)/log(R/g)<=2 log S/log R`, bounded by a fixed constant for our
fixed exponents. Goldston-Yildirim Lemma 2.1 with `j=0` is applicable.
Its main is `bg/phi(bg)`. The remaining `b` sum has scale `S/g` and
parameter `g`, so the `j=1` application is also valid. This produces
`sum_(g|N,g<=sqrt R)mu(g)^2 S_2(g)/phi(g)` as before.

With `L=1+log S`, the accumulated error is
`O(L^3 exp(-c sqrt(log R)))`; the original large-`g` tail is at most
`tau(N)L^4/sqrt R`, and the extended main tail is at most
`2 tau(N)^3/sqrt R`. The exact Euler collapse remains `S_2(N)`.
Since `RS=N^(theta_i+theta_j+o(1))` has a fixed power margin below `N`,
for every fixed `J>0` this proves

```text
C(A_i,A_j) = H + O_J(N/log(N)^J).                         (1)
```

Together with the preceding mixed estimate `C(A_i,Lambda)=H+O_J`,
and its proper-prime-power correction, we obtain

```text
C(D_i,D_j) = Delta_0 + O_J(N/log(N)^J),
C(E,E) = Delta_0 + (s-1)^2 H + O_J(N/log(N)^J).           (2)
```

The error is uniform for the bounded coefficient class. Thus the leading
reflected residual matrix is the constant, rank-at-most-one matrix
`Delta_0 * 1 * 1^t` (rank zero if `Delta_0=0`).
Zero-sum differences remove the prime signal too. For `s=1` there is no
leading reflected gain. For other `s`, the correct sufficient threshold is

```text
C(E,E) >= [(s-1)^2 - (1-epsilon)] H,                     (3)
```

not the unchanged `-(1-epsilon)H`. A positive baseline obtained by changing
`s` is not free evidence of prime pairs.
More precisely, (3) for fixed `epsilon>0` implies
`T_N>=epsilon H+o(H)>=(epsilon/2)H>0` for all large `N`;
the small error must be absorbed before assigning a final margin.

## Ordinary covariance has a different kernel

The same primary paper supplies the unshifted second moment, Theorem 5.1,
equation (5.3), printed p.31:
`sum_(n<=x) Lambda_R(n)^2 = x log R + O(x)+O(R^2)`.
See [Goldston and Yildirim, Integers 3 (2003), A05](https://math.colgate.edu/~integers/d5/d5.pdf).
This is used at shift zero, not at the forbidden large shift `N`.
The other external inputs here are its uniform Lemma 2.1 and the ordinary
prime number theorem. No two-prime correlation estimate is an input.

Here is a derivation of the cross-cutoff ordinary covariance, rather than
assuming a different-cutoff theorem. For `a_R(d)=mu(d)log(R/d)` on `d<=R`,
define the finite Selberg coordinates

```text
w_R(q) = sum_(q|d,d<=R) a_R(d)/d,
Q_(R,S) = sum_(d<=R,e<=S) a_R(d)a_S(e)/lcm(d,e)
        = sum_q phi(q)w_R(q)w_S(q).                      (4)
```

The last identity follows from `gcd(d,e)=sum_(q|d,q|e)phi(q)`.
It is exact even for general coefficients on nonsquarefree indices.
For these particular Mobius coefficients, `w_R(q)=0` if `q` is not
squarefree. Otherwise it equals

```text
(mu(q)/q) sum_(a<=R/q,(a,q)=1) mu(a)/a log(R/(qa)).
```

Fix `0<delta<1` and `G=floor(R^(1-delta))`, with `R<=S`.
For `q<=G` the lemma has fixed logarithmic parameter ratio at most
`(1-delta)/delta`, giving, uniformly on squarefree `q`,

```text
w_R(q) = mu(q)/phi(q) + O_delta(exp(-c_delta sqrt(log R))/q).
```

The same error bound holds for `w_S(q)`. Hence each small-coordinate
cross product or norm in (4) is
`sum_(q<=G)mu(q)^2/phi(q)+o(1)=log G+O(1)`.
For the errors, sum `1/q` up to `G`; the exponential factor beats that
logarithm. The nonsquarefree terms are identically zero.

For completeness, the scalar estimate `sum_(q<=G)mu(q)^2/phi(q)=log G+O(1)`
can be seen without a uniform-shift theorem. Write
`mu(n)^2/phi(n)=(1/n)sum_(d|n)h(d)` with multiplicative `h` given by
`h(p)=1/(p-1)`, `h(p^2)=-p/(p-1)`, and `h(p^a)=0` for `a>=3`.
Then `sum |h(d)|(1+log d)/d` converges and
`sum h(d)/d=product_p(1+1/[p(p-1)]-1/[p(p-1)])=1`.
Sum first over `n=dm` and use the harmonic-sum estimate. The absolute
log moment bounds both truncation tails, leaving `log G+O(1)`.

Equation (5.3), or its exact divisor-count expansion followed by
`x -> infinity` with `R` fixed, gives `Q_(R,R)=log R+O(1)` with an
absolute constant. The two tails of the positive quadratic form (4) have
squared norms `log R-log G+O(1)` and `log S-log G+O(1)`.
Cauchy therefore bounds the absolute cross tail by

```text
sqrt((log R-log G+O(1)) (log S-log G+O(1))).              (5)
```

Take `N -> infinity` for a fixed `delta`, then let `delta -> 0`.
Since the exponents are fixed, (5) proves
`Q_(R_i,R_j)=min(theta_i,theta_j)log N+o(log N)`.
The ordinary central-interval progression error is `O(R_i R_j)=o(N)`.
Consequently

```text
<A_i,A_j> = (N/3)log N * min(theta_i,theta_j)+o(N log N). (6)
```

The leading ordinary kernel is `min(u,v)`, not the constant kernel in
(1). No stochastic independence or Brownian model has been assumed.

## Sharp norm floor for the entire finite family

For all central primes and all large `N`, `A_i(p)=log R_i`.
The prime number theorem and `log p=log N+O(1)` on `I_N` give

```text
<Lambda,Lambda> = (N/3)log N + o(N log N),
<Lambda,A_i> = (N/3)theta_i log N + o(N log N).           (7)
```

Proper prime powers contribute only `o(N)` to these expressions:
there are `O(sqrt N log N)` of them; use `|A_i(n)|<=tau(n)log N`
and the elementary divisor bound with, for example, exponent `1/4`.
Equations (6)--(7) imply

```text
||E||_2^2 = (N/3)log N * F(c) + o(N log N),
F(c) = 1 - 2 sum_i c_i theta_i
         + sum_(i,j)c_i c_j min(theta_i,theta_j).
```

Put `theta_0=0` and `s_j=sum_(i>=j)c_i`. Exact completion of squares gives

```text
F(c) = 1-theta_k + sum_j(theta_j-theta_(j-1))(s_j-1)^2
     >= 1-theta_k > 1/2.                                (8)
```

Equality holds exactly at `c_k=1`, all other `c_i=0`. This minimum is
over ALL real coefficients, even before imposing `s=1`; signed weights
do not evade it. For bounded varying weights the asymptotic error remains
uniform, so the same floor applies. Repeated exponents may simply be merged.

Reflection permutes `I_N`, so plain Cauchy gives only
`C(E,E)>=-||E||_2^2`. The best norm available in this family still has
leading size at least `(1-theta_k)(N/3)log N`.
Already along the explicit even sequence `N=2^m`,
`H=(2C_2/3)N` and this is too large by an unbounded logarithmic factor.
Thus this Cauchy certificate cannot meet (3) at every large even target.
We do not need any conjecture about the sign of the actual `C(E,E)` to
prove this failure of the certificate.

## Decision and surviving ideas

Pursuit: `changed-under-evidence`. The proposed finite linear-mixture
shortcut is analytically excluded in the stated fixed-exponent,
bounded-coefficient family. This is more than a rearrangement: the
rectangular target-uniform estimate and the optimal norm floor cover every
member of that family, not just fitted examples.

Do not retry coefficient or cutoff scans in this unchanged class. Retain
the exact cross-cutoff and Selberg-coordinate identities. A reactivation
requires genuinely signed information, a justified nonlinear operation,
or a changed cutoff/weight regime with its own analytical estimates.
Merely adding more fixed cutoffs does not change the result.

The open pointwise lower bound for the original residual remains OPEN.
No effective starting point, strict-central Goldbach theorem, q286
homogeneous/centered zero-mass repair, or Q46189 transfer follows here.
The old scale-`N` decomposition has not been separately estimated.
The full prove-or-disprove Goldbach objective is unchanged.

The helper and `test_finite_cutoff_mixture.py` check exact rectangular CRT
grouping, Selberg diagonalization, completion of squares and the residual
baseline shift. Tests do not prove the asymptotics. Review and execution
results are recorded separately in `notes/review-receipts.md`.
