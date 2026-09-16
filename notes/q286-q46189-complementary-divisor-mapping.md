# Exact complementary-divisor mapping from the original source

Owner: Goldbach research. Purpose: decide whether the Q46189 source operators
control the missing mass direction or the full q286 signed remainder.
Parent checkpoint: `ec5a9cf79b149a5f0acd551101d7aa20eeaf5b0c`.

Status: proved algebraic identities and elementary error bounds below;
the required signed main adjustment and mixed/long-divisor estimate remains
OPEN. New-to-this-task mapping,
not a claim of novel CRT or Mobius inversion, and not a Goldbach proof.

## Question and pre-computation decision

Mechanism: retain the original divisor coefficients but replace same-argument
divisibility with complementary divisibility at `n` and `N-n`. Predict that
the target needs both CRT compatibility and its target-dependent residue.
Falsifier: a failed exact convolution identity, incorrect endpoint bound,
or a source identity already controlling the missing terms. Smallest check:
exact rational CRT/source tests and a log-prime coefficient identity check,
not a scan of thresholds or candidate constants.

The bound was stated before computation: with `B=floor(N^(8/25))`, the
short-short counting discrepancy is at most `B^2 log(N)^2=o(N)`.
The unproved target is the remaining signed main adjustment and long-divisor
correlations, quantified below. Sleep the direct Q46189 transfer unless its
new operator retains those terms and the complementary CRT residues.

## 1. What Q46189 actually measures

In `lcm_sawtooth_incomplete_covariance.py`, put `D={a:V<a<=B, mu(a)!=0}`,
`X=m*ell_freeze`, `c_a(X)=mu(a)log(X/a)`, and

```text
Z_X(n) = sum_(a in D,a|n) c_a(X),
K_q(X) = sum_(a,b in D,lcm(a,b)=q) c_a(X)c_b(X),
kappa_X = sum_q K_q(X)/q.
```

Expanding the square and counting multiples gives the exact identity

```text
F_m(ell) = sum_(t=1..m-1) Z_X(m*ell+t)^2 - (m-1)kappa_X
         = sum_q K_q(X) [floor((m*ell+m-1)/q)-floor(m*ell/q)-(m-1)/q].
```

This is a centered block sum of a square, not a binary prime correlation.
`lcm_sawtooth_incomplete_frequency.py` rewrites it with
`S_d=sum_(d|q)K_q/q` and primitive frequencies `k/d`.
`lcm_sawtooth_lifted_endpoint_frame.py` then groups frequency pairs in
`|F_m(ell)|^2` by their reduced difference denominator `Q`. If
`k/d-h/e=b/q`, `q=lcm(d,e)`, `g=gcd(|b|,q)`, its phase is
`exp(2*pi*i*r*ell/Q)`, where `Q=q/g`, `r=m*(b/g) mod Q`.
Writing the grouped component as
`T_Q(ell)=sum_r D_Q(r)exp(2*pi*i*r*ell/Q)`, its energies are

```text
D_full,Q   = Q sum_r |D_Q(r)|^2,
D_active,Q = (Q/A) sum_(ell in active window) |T_Q(ell)|^2.
```

The lifted frame retains selected cells `Q>mA`; its numerator selects
endpoint pairs. Its generalized eigenvalue ranges over arbitrary `R^6`,
a relaxation of the realizable rank-one polynomial squares. Failure of
that relaxation does not prove failure or impossibility for the actual
Mobius family. These restrictions are explicit in the original frame code.

Thus `Q=46189` is a frequency-difference denominator in a fourth-moment
construction, not the target `N` or a pair-residue modulus. The lifted
matrices encode these polynomial energies. Their degree-five cross entry
is not itself a signed prime-pair error.

The checked-scale route uses `M`, inferred scale `M^(1/.59)`, `A` of scale
`N^.41`, prime `m` in `[M,2M]`, `V` of scale `N^.15`, and divisor ceiling
`B` of scale `N^.32`. This `B` is NOT the small CRT factor cutoff of scale
`N^.009` in `prime_band_vaughan_type_i.py`. That older active-band route
still explicitly requires endpoint/kernel transfer and an arithmetic
remainder estimate; it does not supply a direct estimate for `Delta_0`.

## 2. Exact mapping to the mass direction

Let `N>=6` be even, `I_N={n:N/3<n<2N/3}`, and use natural logarithms.
For **all** actual divisors and any fixed `X>0`, Mobius inversion gives,
for `n>1`,

```text
sum_(a|n) mu(a)log(X/a)
  = log(X)sum_(a|n)mu(a) - sum_(a|n)mu(a)log(a) = Lambda(n).
```

Proof: the first divisor sum is zero; `Lambda=mu*log` gives the second
identity after writing `log(n/a)=log(n)-log(a)`.
The statement excludes `n=1`, where the frozen sum is `log(X)`.
All points of `I_N` satisfy `n>1`.

Now fix `X=N`, an integer cutoff `1<=B<=N`, and define

```text
c_a = mu(a)log(N/a),
A_B(n) = sum_(a|n,a<=B)c_a,
R_B(n) = sum_(a|n,a>B)c_a,
C(f,g) = sum_(n in I_N) f(n)g(N-n).
```

There is no frozen-log remainder in `A_B+R_B=Lambda`. However, freezing
does NOT cancel inside the original middle band alone:

```text
Z_N(n) = Z_X(n) + log(N/X) sum_(a in D,a|n)mu(a).
```

Any transfer from its stored `X=m*ell_freeze` must retain this correction.

Set `q=lcm(a,b)`, `g=gcd(a,b)`. The two divisibility conditions
`a|n`, `b|N-n` are compatible exactly when `g|N`. If compatible,

```text
r = a * ((N/g)*(a/g)^(-1) mod (b/g)),  0<=r<q,
```

with the parenthesis defined as zero if `b/g=1`. Put
`L=floor(N/3)+1`, `U=ceil(2N/3)-1`. Their exact count is

```text
C_N(a,b) = floor((U-r)/q)-floor((L-1-r)/q)
         = N/(3q) + epsilon_N(a,b),  |epsilon_N(a,b)|<=1.
```

For incompatible pairs the count and density are both zero. The error bound
uses the length of the real OPEN interval, `N/3`, not its integer point
count. Equality at one is possible: `N=12,q=4,r=0` has no interior point
and density one. This proves the bound, including strict endpoints.

Consequently, define

```text
K_B(N) = sum_(a,b<=B,gcd(a,b)|N) c_a c_b/lcm(a,b),
E_B(N) = sum_(a,b<=B,gcd(a,b)|N) c_a c_b epsilon_N(a,b).
```

Then the following is universal, not fitted:

```text
C(A_B,A_B) = (N/3)K_B(N)+E_B(N),
|E_B(N)| <= (sum_(a<=B)|c_a|)^2 <= B^2 log(N)^2.             (1)
```

Let `T_N=sum_(n in I_N,n and N-n prime)log(n)log(N-n)` be the ordered
prime-only central log mass. Define
`P_N=C(Lambda,Lambda)-T_N`, the contribution with at least one proper
prime-power argument. It is nonnegative. There are at most
`sqrt(N)*floor(log_2 N)` proper prime powers up to `N`, by counting each
exponent separately. A union bound over the two arguments proves

```text
0 <= P_N <= 2 sqrt(N) floor(log_2 N) log(N)^2 = o(N).        (2)
```

Reflection of `I_N` gives `C(A_B,R_B)=C(R_B,A_B)`. With the independently
defined singular series and `H(N)=S(N)N/3`, the requested EXACT mapping is

```text
Delta_0(N) = T_N-H(N)
 = (N/3)(K_B(N)-S(N)) + E_B(N)
   + 2 C(A_B,R_B) + C(R_B,R_B) - P_N.                      (3)
```

Neither `K_B=S(N)` nor a small long-divisor contribution is asserted.
The signed terms can be large and cancel. Omitting them is invalid.

## 3. Required analytical bound, with its scale

Put `G_B=(N/3)(K_B-S)+2C(A_B,R_B)+C(R_B,R_B)`. A sufficient pointwise
theorem for all sufficiently large even `N`, with a fixed `epsilon>0`, is

```text
G_B(N) >= -(1-epsilon)H(N).                               (4)
```

Indeed, (1)--(3) yield `T_N >= epsilon H - B^2 log(N)^2 - P_N`.
The preceding checkpoint proved `S(N)>=1` for positive even `N`. For
`B=floor(N^(8/25))` the two proved error/main ratios are at most

```text
3 N^(-9/25) log(N)^2,
6 N^(-1/2) floor(log_2 N) log(N)^2,
```

respectively. Both tend to zero. Their sum below `epsilon` gives strict
positivity. This is an asymptotic sufficient theorem, not a checked finite
threshold or a proof covering the remaining finite range. Alternatively the
exact one-sided requirement is `G_B+E_B-P_N>-H`.

For `N>39`, the q286 periodic witness has the already established identity
`W_phi=M(a)T_N+sum_d U_d`; `M(a)` is its uniform admissible-residue mean and
`U_d` are the unnormalized signed projected errors, as defined in
`q286-independent-local-density-and-mass-direction.md`. Therefore its full
signed remainder is exactly

```text
W_phi-M(a)H = M(a)(G_B+E_B-P_N) + sum_d U_d.                (5)
```

For classes where `M(a)>0`, a sufficient bound is
`M(a)G_B+sum U_d >= -(1-epsilon)M(a)H`; the same two error/main ratios
apply. This is NOT implied by centered channel bounds or Q46189 energies.
The earlier numerical all-class positivity of `M(a)` is not silently
promoted to an exact uniform theorem here. The unweighted route (4) avoids
that issue entirely. At zero prime support (3) gives `Delta_0=-H`; an actual
proof of (4) would exclude zero for large N, unlike the homogeneous caps.

## 4. What survives and what the source loses

The shared object is a divisor-pair expansion, but its target kernel changes:

- Q46189 begins with `a|n,b|n`, hence residue zero modulo `lcm(a,b)`.
- The binary target uses `a|n,b|N-n`, hence compatibility `gcd(a,b)|N`
  and the residue `r` above. The natural grouped target coefficient has
  indices `(q,r)`, not just `q`.
- At `N=32`, `(a,b)=(2,15)` gives `(q,r)=(30,2)` and no central point;
  `(a,b)=(6,5)` gives `(30,12)` and one. Both are compatible, squarefree
  divisor pairs with the same lcm. A common count depending only on `q`
  cannot replace both. This is a count-operator obstruction, not a
  counterexample to a possible arithmetic inequality using richer data.
- The source uses only `V<a<=B`. Even its complementary middle-middle
  counting error has the elementary bound (1). The entire short-short
  rectangle `a,b<=B` also does. The hard obligations in (4) instead retain
  the main adjustment and at least one divisor above `B`.

This is useful progress: the short-short binary counting error and
prime-power correction need no Q46189 fourth-moment estimate. It does NOT
prove that Q46189 is useless for its original active-band problem, rule out
all indirect transfers, or make the long-divisor theorem easy. No exact
operator map from the existing Q46189 energies to those remaining signed
terms has been established.

## 5. Curiosity follow-through: the sign under divisor switching

Kevin explicitly freed the continuation from a prescribed route. The bounded
question chosen here is whether the same-argument square suppresses a sign
that reappears in the complementary product. This is an algebraic check,
not a claim that Mobius signs are random or an appeal to an unproved
decorrelation conjecture.

For the long part the substitution `a=n/b` gives EXACTLY

```text
R_B(n) = sum_(b|n,b<n/B) mu(n/b)log(N*b/n).
```

When `n` is squarefree, `mu(n/b)=mu(n)mu(b)`. Thus `R_B(n)=mu(n)H_B(n)`,
where `H_B` is the displayed sum with `mu(b)` in place of `mu(n/b)`.
The same substitution for the original middle band gives

```text
Z_X(n) = mu(n) J_X(n),
J_X(n) = sum_(b|n,n/B<=b<n/V) mu(b)log(X*b/n)               (n squarefree).
```

Consequently its diagonal square is `J_X(n)^2`, but, when both arguments
are squarefree, its complementary product is
`mu(n)mu(N-n)J_X(n)J_X(N-n)`. The explicit outer sign cancels in one
and remains in the other. The inner weights still depend on `n`; this does
NOT prove statistical independence, impossibility of an arithmetic transfer,
or loss of all sign information from the complete source construction.

The squarefree qualification is essential, not a disposable prime-power
error: at `n=12`, `D=(2,7]`, the actual middle-band sum is `-log(2)`, while
the erroneous factorization by `mu(12)` gives zero. Nonsquarefree integers
in these divisor sums cannot all be discarded as proper prime powers.

Decision: retain this sign-sensitive decomposition as a candidate locator,
not an estimate. The next useful question is whether an available arithmetic
input controls the resulting **mixed complementary kernel**, with the actual
Mobius weights and nonsquarefree part intact. A new magnitude-only moment
or a constant scan does not answer it. The full prove-or-disprove objective
remains active; no path is mandatory merely because it was proposed.

## Validation

`complementary_divisor_correlation.py` and its focused tests retain the
source block-square identity, exact CRT cells, endpoint equality, residue
compression obstruction, scale-independent full log-prime identity, and
the two-by-two correlation split. Numerical log evaluation is explicitly
only an identity smoke check. Proofs of (1)--(3) are the derivations above,
not extrapolation from those tests. Review and final test counts belong in
`notes/review-receipts.md`.
