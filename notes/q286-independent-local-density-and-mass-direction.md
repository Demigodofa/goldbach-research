# q286 independent local density and the missing mass direction

Owner: Kevin; derivation and integration: Rill. Date: 2026-09-16.
Purpose: decide whether q286 local positivity was incorrectly classified as
necessarily depending on existing pairs, and identify what a Q46189 transfer
would have to control. This is a proof of elementary local-model and linear
algebra identities, with an open prime-correlation estimate. No Goldbach proof
or major/minor arc error estimate is claimed. Novelty: new-to-this-task.

## Correction to the prior interpretation

The exact identity `W_phi=M(a)*T_N+centered_action` is valid. Interpreting its
first term as the circle method's major-arc main term conflates two objects.
An independently defined local-density main-term candidate exists:

```text
H(N) = (N/3) * S(N)
weighted main-term candidate = M(a) * H(N).
```

Here `S(N)` is the ordinary binary Goldbach singular series, defined below.
Neither expression uses an observed pair or assumes `T_N>0`. They are not
lower bounds for the actual pair sum without a remainder estimate.
The earlier principal-factor and local-factor-collapse receipts only computed
the decomposition involving `T_N`; they did not exclude this candidate.
Their zero-support warning remains correct, but the broader interpretation
that an independent local-density term is unavailable is superseded here.

## Exact finite local-density identity

Let `Q` be squarefree, `N` even, and

```text
A_Q(N) = {s mod Q : gcd(s,Q)=gcd(N-s,Q)=1}, K=|A_Q(N)|,
m = (1/K) sum_{s in A_Q(N)} w(s),
rho_p(N) = p-1 if p|N, and p-2 otherwise,
beta_p(N) = p*rho_p(N)/(p-1)^2.
```

The weight `w` is any real function of a residue modulo `Q`. For every
squarefree multiple `L` of `Q`, define the finite normalized density

```text
D_L(w;N) = L/phi(L)^2 * sum_{x mod L, gcd(x(N-x),L)=1} w(x mod Q).
```

Then, exactly,

```text
D_L(w;N) = m * product_{p|L} beta_p(N).
```

Proof: the forbidden classes modulo `p` are `0` and `N`, coincident precisely
when `p|N`. Thus there are `rho_p(N)` choices. CRT gives
`K=product_{p|Q}rho_p(N)`, and each admissible class modulo `Q` has exactly
`product_{p|L/Q}rho_p(N)` admissible lifts modulo `L`. Substitute this count
into `D_L`, and use `phi(L)=product_{p|L}(p-1)`. No primality assertion enters.
Signed and nonmultiplicative weights are allowed.

Consequently every admissible residue gets the same local-model factor.
A weight of admissible mean zero has zero local-model density for every `L`.
For the repo's `Q=10010`, the uniform residue law is exactly the law used in
`admissible_units` and `orbit_coefficients` in
`tools/build_q286_cone_duality_l1_uniformity_candidate.py`; orbit masses are
orbit size divided by `K`, not equal mass per orbit.

## Infinite product, without a prime-pair assumption

For fixed positive even `N`, let the prime factors of `L` exhaust all primes. The
product converges to

```text
S(N) = 2 * product_{p>2}(1-1/(p-1)^2)
           * product_{p>2, p|N}(p-1)/(p-2).
```

This product is positive. Indeed, the second product is finite and at least
one; the first product is at least

```text
product_{k=2}^infinity (1-1/k^2) = 1/2,
```

because the odd-prime factors form a subset of these factors in `(0,1)`.
The finite telescoping product is `(b+1)/(2b)`. Hence `S(N)>=1` for every
positive even `N`. Convergence also follows from `sum_{k>=2}1/k^2<infinity`.
In particular `H(N)>=N/3>0` independently of prime-pair existence.
The `N=0` cases in the tests check only finite CRT products: at zero the
infinite product diverges and the positive-baseline conclusion does not apply.

The continuous strict-central singular integral is
`integral 1_(N/3,2N/3)(x) 1_(N/3,2N/3)(N-x) dx=N/3`.
This explains the factor `N/3`; endpoint discretization belongs to the error.
Combining this integral with the local product identifies a candidate, not
an established asymptotic for the prime convolution. For the actual q286
weight, the existing all-5005-residue coefficient audit reports positive
`M(a)` numerically. Those floating coefficient values are not promoted here
to a rigorous interval certificate or a new universal analytic bound.

External normalization check: Salmensuu, *The Goldbach conjecture with
summands in arithmetic progressions*, Section 1.3 and Section 3,
https://doi.org/10.1093/qmath/haac008, uses the product excluding primes dividing
the progression modulus and evaluates major-arc contributions separately.
Our CRT calculation restores the excluded factors. The paper's binary
existence results retain exceptions; they do not supply our pointwise bound.
The strict-central signed-weight specialization still requires an actual
major-arc derivation with its error and a pointwise minor-arc estimate.

## The exact direction that centering erases

For `N>39`, every strict-central prime is coprime to `10010`. Let `R_s(N)` be
the prime-only log-weighted ordered pair mass in admissible residue `s`, and
let `u_s=1/K`, `T=sum_s R_s`. These definitions permit `R=0`.
For any independently defined positive baseline `H`, set

```text
e = R-H*u, Delta_0 = sum e = T-H,
C = I-u*1^t.
```

Then

```text
C e = e-u*sum(e) = R-T*u,
C u = 0, C^2=C, ker(C)=span(u).
```

Proof: `sum u=1`; direct substitution proves the first three identities.
If `Cv=0`, then `v=u*sum(v)`, proving the kernel statement. In the uniform
residue coordinates just defined, `C=I-(1/K)*1*1^t` is orthogonal. The same
identities hold for any probability vector `u`; with unequal orbit masses,
`C` is generally oblique in ordinary Euclidean coordinates.

Every centered q286 channel therefore discards the scalar error `Delta_0`.
For any number of channels `c_j` with `c_j dot u=0`, all vectors `R=t*u`,
`t>=0`, give identical channel outputs, namely zero. Stacking centered
channels, using nonlinear functions of their outputs, or bounding their
norms cannot distinguish those vectors. This is an exact obstruction to
inference from those constraints alone. These are abstract nonnegative mass
vectors, not claimed realizable prime data or counterexamples to Goldbach.

This applies jointly to the four actual projected moduli, not just one
abstract channel. If squarefree `d|Q`, every admissible residue modulo `d`
has the same number `product_{p|Q/d}rho_p(N)` of admissible lifts. Thus the
pushforward of `u_Q` is `u_d`. For `R=t*u_Q`, each projected discrepancy
`Pi_d-T*u_d` is zero simultaneously. More generally take `Q` to be the lcm
of any finite collection of squarefree moduli: adding centered congruence
channels does not remove this common kernel. Arithmetic constraints on
actual primes could still exclude such mass vectors; none is supplied by
this residue argument.

For `m=w dot u`, the complete witness identity is

```text
W_w = m*H + m*Delta_0 + w dot C e.
```

At zero support, `e=-H*u`, `Delta_0=-H`, `Ce=0`. The missing scalar error
cancels the entire positive local-model term. This identifies why even
perfect centered control alone leaves existence open.

## Consequence for the adverse gate and a Q46189 combination

Using the repo's decomposition `W_phi=M(a)*T+sum_d U_d`, the corrected
independent-baseline identity is

```text
W_phi=M(a)*H + M(a)*Delta_0 + sum_d U_d.
```

For `M(a)>0`, one sufficient one-sided estimate would be

```text
max(0,-M(a)*Delta_0) + sum_d max(0,-U_d) < M(a)*H.
```

Write `A_raw_- := sum_d max(0,-U_d)`.
This is a target, not a new easier theorem: its surplus equals exactly
`M(a)*min(T,H)-A_raw_-`, which is at most the old raw gap
`M(a)*T-A_raw_-`. At zero support it is equality, never a strict pass.
The potentially sharper target retains helpful signed terms:

```text
M(a)*Delta_0 + sum_d U_d > -M(a)*H.
```

That is just the explicit remainder obligation for `W_phi>0`.

A q286/Q46189 combination must reach this missing scalar direction or control
the combined signed remainder directly. A transfer only into more centered
channels cannot suffice, regardless of the finite correlations it improves.
No mapping from the Q46189 source matrices to `Delta_0(N)` is currently given.
This obstructs only such centered-only combinations; it does not disprove
the possibility of an arithmetic relation constraining the full remainder.

## Validation and next action

`periodic_pair_local_density.py` implements exact rational fixtures.
`test_periodic_pair_local_density.py` checks direct CRT enumeration (including
the actual assembled period `10010` extended by `3` and `17`), signed and
zero-mean weights, nonuniform reference vectors, the entire uniform-deficit
family, the four q286 modulus pushforwards, the adverse-gap identity, and
invalid domains. The all-parameter
arguments above are the proofs; the tests verify the implementation.

HAL/Qwen supplied one proposal-informed algebra check after its strict
runtime test passed. Rill accepted the CRT normalization and centering
identity and corrected its orthogonality wording. This is advisory review,
not independent mathematical certification. A separate read-only Sol reviewer
checked the supplied derivation and ran all ten tests. It caught the missing
`N>0` restriction, the need to distinguish uniform and orbit coordinates,
and the omitted local definition of `A_raw_-`; Rill incorporated all three.
It also confirmed that this clarifies an interpretation of the old audit,
not an algebraic error in its exact identity. See `notes/review-receipts.md`.
The review supports these elementary deductions only, not the open analytic
estimate or Goldbach. No historical novelty is claimed.

Creative-tools outcome: changed-under-evidence. The candidate independent
local factor survives; the prediction that centered channels alone can pay
its remainder is falsified by the uniform-deficit family. Stop further
constant tuning. The next useful proof attempt must identify a term in the
original arithmetic construction that controls `Delta_0` or the full signed
remainder, and must state its mapping to actual `N` before computation.
The Goldbach goal remains open.
