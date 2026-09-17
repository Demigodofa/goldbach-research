# Unconditional Type I control and the actual coprime Vaughan remainder

Owner: Goldbach research. Parent: `4c719fcf1cbb41dc94590d3d4aa774580531a1a2`.
Purpose: remove a conditional prerequisite for an actual-arithmetic bilinear
reduction, while retaining the exact unresolved signed coefficients.
Novelty label: `new-to-this-task`, not a new Vaughan identity or worldwide claim.

## Question declared before computation

Does the cutoff residual have unconditional, divisor-weighted progression
control sufficient for a unit-restricted Vaughan transfer? The previous
`unexceptional_vaughan_gate.py` used a different residual, `Lambda-Gamma_S`,
and a Type I input only in its unexceptional branch. The present question
concerns `D_R=Lambda-A_R`, not an upgrade of that old kernel theorem.

Mechanism: match the exact progression density of `A_R` to the Mangoldt
main, cancel the nonreduced main by Mobius inclusion-exclusion, and combine
Bombieri-Vinogradov with a prefix mesh and fixed divisor-moment bounds.
The extra divisor weights pay for the unit mask in the exact transfer.

Changed prediction: an unconditional Type I theorem for the actual residual,
followed by an unconditional reduction to one exact coprime bilinear sum.
This would remove the exceptional-branch prerequisite for this new route;
it would not estimate that bilinear sum or exclude exceptional zeros.

Falsifiers: surviving nonreduced main, nonuniform excluded-divisor estimate,
unjustified prefix maximum, divisor multiplicity larger than the paid bound,
or a nonunit tail of main-term size. The exact bound is (1) below. Budget:
one proof, exact algebra fixtures and a separate source/mathematical review.
No constant scans or finite data as acceptance. Curiosity, inventive synthesis
and hypothesis preservation were checked; the old absolute remainder
obstruction already includes coprime configurations and is not retried.

## Definitions and primary inputs

Fix `0<alpha<kappa<theta<1/2`. Let `L=1+log N`, `R=floor(N^theta)`,
`Q=floor(N^kappa)`, and `I_N=(N/3,2N/3) intersect Z`, with N even.
Write

```text
A_R(n) = sum_(d|n,d<=R) mu(d) log(R/d),   D_R = Lambda-A_R.
C(f,g) = sum_(n in I_N) f(n)g(N-n).
H(N) = S_2(N) N/3,   Delta_0 = T_N-H(N),
```

where `T_N` is the ordered PRIME-only central logarithmic mass, not the
Mangoldt pair sum. Parent proofs give `C(Lambda,A_R)=H+O_J(N/L^J)` and
the proper-power correction `C(Lambda,Lambda)=T_N+O_J(N/L^J)`.
Their constants, like those below, are independent of the target N, with
dependence on fixed exponents and J allowed. They do not give an effective
starting point for a Goldbach lower bound.

Primary sources checked 2026-09-16:

- Goldston and Yildirim, [Higher correlations of divisor sums related to
  primes I](https://math.colgate.edu/~integers/d5/d5.pdf), equation (1.30),
  printed p.8, for ordinary Bombieri-Vinogradov; Lemma 2.1, equations
  (2.11)-(2.12), printed p.16, with `j=0`; equation (2.8) for `S_1(q)=q/phi(q)`.
- Tao, [254A Notes 3](https://terrytao.wordpress.com/2015/01/10/254a-notes-3-the-large-sieve-and-the-bombieri-vinogradov-theorem/),
  Lemma 18 equation (32), for the exact Vaughan identity. Our U and V
  names are interchanged relative to that display. Its free convolution
  factor `1` is retained. No use of the excluded Linnik argument in Notes 7.

Neither a restricted-shift correlation theorem nor a conjectural
equidistribution level is used here.

## The unconditional weighted Type I theorem

For every fixed integer `K>=0` and every fixed `J>0`,

```text
I_K(N,Q) = sum_(q<=Q) tau(q)^K max_(r mod q) sup_(N/3<=x<=2N/3)
              |sum_(N/3<n<=x, n=r mod q) D_R(n)|
           <<_(theta,kappa,K,J) N/L^J.                         (1)
```

The maximum includes nonreduced residue classes. Any subinterval of the
central window is a difference of two prefixes. Strict upper endpoints
are obtained by a left limit; they do not add boundary atoms.

### Exact progression density

Define

```text
rho_R(q,r) = sum_(d<=R,(d,q)|r) mu(d)log(R/d)/lcm(d,q).
sum_(N/3<n<=x,n=r mod q) A_R(n)
    = (x-N/3)rho_R(q,r)+O(R).                                (2)
```

Each compatible CRT count differs from interval length divided by lcm by
at most one; `sum_(d<=R)|mu(d)|log(R/d)<=R` pays for all errors.
Set `g=gcd(q,r)`, allowing `r=0`. On squarefree support, split `d=h*b`
with `h|rad(g)` and `(b,q)=1`. Since `lcm(h*b,q)=q*b`, exactly

```text
rho_R(q,r) = (1/q) sum_(h|rad(g)) mu(h)
               sum_(b<=R/h,(b,q)=1) (mu(b)/b) log(R/(h*b)).    (3)
```

The inner cutoff `R/h` is real, not rounded in the logarithm. For `q<=Q`,
all h in this sum satisfy `h<=q`, so `R/h>=R/Q`. Consequently
`log q/log(R/h)` is bounded by a constant depending only on the fixed gap
`theta-kappa`. GY Lemma 2.1 with `j=0`, `Y=R/h`, `k=q` applies uniformly:

```text
inner sum = q/phi(q)+O_(theta,kappa)(exp(-c sqrt(log N))).
rho_R(q,r) = 1_((q,r)=1)/phi(q)
                 +O(tau(q)/q * exp(-c sqrt(log N))).          (4)
```

Here `sum_(h|rad(g))mu(h)=1_(g=1)` cancels the entire nonreduced main,
including repeated factors in q. The case q=1 is included.
The exponent gap is fixed; no uniform extension to a gap shrinking with
N is claimed.

For each fixed integer B, `tau(n)^B<=d_(2^B)(n)`. On a prime power, a
B-tuple in `{0,...,e}^B` injects into multisets of e binary columns by
writing each coordinate as a monotone column sequence. The column counts
are a weak composition into `2^B` bins, giving the inequality; extend
multiplicatively. Thus

```text
sum_(q<=Q) tau(q)^B/q <<_B L^(2^B),
sum_(q<=Q) tau(q)^B   <<_B Q L^(2^B).
```

Equations (2)-(4), after weighting, have total error

```text
O_K(N L^C_K exp(-c sqrt(log N)) + R Q L^C_K).                 (5)
```

Since `theta+kappa<1`, this is `O_J(N/L^J)` for every fixed J.

### Mangoldt prefixes without a hidden maximal theorem

First prove the unweighted version for

```text
E_q = max_(r mod q) sup_(N/3<=x<=2N/3)
      |sum_(N/3<n<=x,n=r mod q) Lambda(n)
                   -(x-N/3)1_((q,r)=1)/phi(q)|.
```

GY (1.30), with unconditional level `1/2` and fixed exponent slack, applies
at every fixed endpoint `x comparable to N` because `kappa<1/2`.
To move the supremum INSIDE the q-sum, take a common mesh of the central
interval, including both ends, with `O(L^B)` points and spacing
`h=O(N/L^B)`. For a reduced residue, monotonicity of `psi(x;q,r)` brackets
any endpoint by its neighbors. Its error is at most the larger neighboring
error plus `h/phi(q)`. Summing all mesh-point BV estimates and using
`sum_(q<=Q)1/phi(q)<=sum tau(q)/q<<L^2` gives

```text
sum_(q<=Q) max_(r reduced) sup_x |psi(x;q,r)-x/phi(q)|
    << N L^(B-A) + N L^(2-B).
```

Choose B for the desired saving, then the source BV exponent A larger
still. Subtract the lower endpoint to obtain central prefixes. This does
not exchange a supremum and a sum for free.

In a nonreduced residue, a prime contributing in the central window would
divide q, hence be at most `Q<N/3`, impossible for large N. Only proper
prime powers remain. Their total mass per q is `O(sqrt(N)L^2)`, so summing
over q costs `O(Q sqrt(N)L^2)`, a fixed power saving. Therefore
`sum E_q<<_J N/L^J` with all residue classes included.

Finally, a trivial progression count and `q/phi(q)<=tau(q)` give
`E_q<<N L tau(q)/q` for `q<=Q`. Cauchy on nonnegative errors gives

```text
(sum_(q<=Q) tau(q)^K E_q)^2
    <= (sum E_q)(sum tau(q)^(2K) E_q),
sum tau(q)^(2K) E_q << N L sum tau(q)^(2K+1)/q <<_K N L^C_K.
```

Choosing the unweighted logarithmic saving sufficiently strong proves the
weighted bound. No `N^o(1)` factor is multiplied into a mere logarithmic
saving. Subtracting (5) proves (1).

## Exact Vaughan transfer

Take `U=V=floor(N^(alpha/2))`. The identity, valid independently of N, is

```text
Lambda = Lambda_<=U + mu_<=V * log
         - mu_<=V * Lambda_<=U * 1 + mu_>V * Lambda_>U * 1.   (6)
```

On `I_N`, the first term vanishes eventually. Pair the second term with
`D_R(N-n)`. For each `d<=V`, the reflected variable lies in residue N
modulo d. Abel summation for `log(n/d)` costs `O(L)` times (1).
The third term groups into `sum_(d|n) C_d`, where

```text
C_d = sum_(ab=d,a<=V,b<=U) mu(a)Lambda(b),
support d<=UV<=N^alpha,   |C_d|<=sum_(b|d)Lambda(b)=log d.
```

It is controlled by (1) with another logarithmic loss. Arbitrary fixed
logarithmic savings absorb both losses. Group the last free factor `1`
into the Lambda factor, retaining

```text
B_U(b) = sum_(d|b,d>U) Lambda(d),   0<=B_U(b)<=log b,
T_R(N) = sum_(a>V,b>U,ab in I_N) mu(a) B_U(b) D_R(N-ab).
C(Lambda,D_R) = T_R(N)+O_J(N/L^J).                           (7)
```

Do NOT replace `B_U` by Lambda or log, or add `(a,b)=1`. For example,
`B_3(15)=log 5`, distinct from both `Lambda(15)` and `log 15`.
Both factor scales exceed `N^(alpha/2+o(1))` and can extend to
`N^(1-alpha/2+o(1))`; this is not a balanced-square-root-only reduction.

The accepted parent mixed estimate and proper-power correction now give

```text
Delta_0 = C(Lambda,D_R)+O_J(N/L^J) = T_R(N)+O_J(N/L^J).      (8)
```

## Paying for the unit restriction

This is an aggregate cancellation argument, not permission to delete
noncoprime divisor tuples. First,

```text
sum_(n in I_N,(n,N)>1) Lambda(n)D_R(N-n) <<_delta N^(1/2+delta)L^3.
```

The first argument is a proper prime power, or a prime dividing N inside
the window. In the latter case it can only be `N/2`, with prime partner;
there is at most one such midpoint. Use `|D_R(m)|<<tau(m)L` and the
elementary proper-power count. The displayed bound is negligible.

Restrict each Type I piece of (6) by the exact mask

```text
1_((n,N)>1) = -sum_(g|rad(N),g>1) mu(g) 1_(g|n).
```

Put `Z=N^(kappa-alpha)`. For `g<=Z`, combine `g|n` with the original
Type I index `d|n`, `d<=UV<=N^alpha`, to get `q=lcm(d,g)<=N^kappa`.
For each q, at most `tau(q)^2` pairs `(d,g)` occur. Coefficients and Abel
variation cost `O(L)`. Consequently (1) with `K=2` controls their entire
sum, including overlaps and nonreduced reflected residues.

For `g>Z`, each of the two original Type I functions is bounded pointwise
by `tau(n)L`; its product with `D_R(N-n)` is `O_delta(N^delta L^2)` for
any fixed delta>0. There are `O(N/g)` central multiples when `g<=N`.
The remaining tail is at most

```text
O_delta(N^(1+delta) L^2 sum_(g|rad(N),g>Z)1/g)
    <<_delta N^(1+delta) tau(N)L^2/Z.                        (9)
```

Choose delta small relative to the fixed positive gap `kappa-alpha`, and
absorb `tau(N)<<_delta N^delta`. This is a power saving. Thus the nonunit
parts of both Type I terms are negligible. Subtracting them from the
restricted exact identity (6) shows that the WHOLE nonunit Type II part
is negligible too. No individual summand is asserted small or zero.

We have proved the unconditional transfer

```text
T_R^unit(N) = sum_(a>V,b>U,ab in I_N,(ab,N)=1)
                    mu(a) B_U(b) D_R(N-ab),
Delta_0 = T_R^unit(N)+O_(theta,kappa,alpha,J)(N/L^J).          (10)
```

Here `(ab,N)=1` is equivalent to `(a,N)=(b,N)=1`, not `(a,b)=1`.
Combining with the already proved localization also identifies
`E_D=C_unit(D_R,D_R)+O_J=T_R^unit+O_J`, with the same scope of errors.

## What changed and what remains open

The result is more than an algebraic restatement: (1) supplies an
unconditional analytical input with fixed divisor weights and all residue
classes, and (9) pays for a mask not licensed by termwise deletion.
It creates a new unconditional actual-residual Vaughan route. The older
`Lambda-Gamma_S` unexceptional route and its hypotheses remain unchanged.

A sufficient, still OPEN, pointwise estimate is: some fixed `epsilon>0`
satisfies

```text
T_R^unit(N) >= -(1-epsilon)H(N)
```

for every sufficiently large even N. An absolute `o(N)` bound would be
stronger than necessary. Neither (1) nor (10) bounds this signed bilinear
sum. Smooth-kernel hypotheses do not automatically include its actual
Mobius/divisor coefficients. The old absolute-remainder obstruction,
q286 missing-mass failures, Q46189 transfer gap, finite-cutoff L2 floor
and both reflection-thinning boundaries remain intact. No effective
threshold, finite-remainder closure, or Goldbach proof/disproof is supplied.

Exact fixtures: `residual_type_i_transfer.py` and
`test_residual_type_i_transfer.py`. They verify density regrouping, full
periods, nonreduced main cancellation, strict endpoints, multiplicity,
divisor-moment domination and the unchanged Vaughan coefficients on each
of the unit and nonunit sets. They are not evidence for an asymptotic rate.

Separate fresh-context Sol supplied-proof/source review returned scoped
PASS with no material findings; see `notes/review-receipts.md`. The ten
new tests pass independently in normal and optimized modes. The lead's
combined 123 tests and optimized affected/adjacent 88 tests pass. The
first handwritten expected vector in one fixture was corrected from its
direct divisor expansion before these passing runs; no analytical
correction was required by the reviewer.
