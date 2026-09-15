# q286 signed pair-correlation definition

Status: coefficient-sensitive theorem definition and proof obligation.  This
is not a signed pair-correlation estimate, binary Goldbach-in-progressions
theorem, q286 threshold theorem, or Goldbach proof.

## Why this pivot is needed

The latest source-backed AP comparison demoted the blunt L1-uniformity bridge.
The issue is not that AP bounds are unavailable.  The issue is that the q286
finite mechanism is not a one-dimensional residue-count statement.

The actual object is a reflected, strict-central, binary prime-pair measure on
the assembled period `10010`.  A theorem must control the signed action of
that measure against the q286 coefficients.

Executable receipt:

```text
tools/build_q286_signed_pair_correlation_definition.py
evidence/q286-signed-pair-correlation-definition.json
```

## Fixed definition

Let `M=10010`.  For an even target `N`, set:

```text
a = N mod M
U = (Z/MZ)^*
A_a = {r in U : gcd(a-r,M)=1}
```

Define the strict-central weighted binary-prime residue mass:

```text
W_N(r) = sum log(p)log(N-p)
```

where the sum is over primes satisfying:

```text
N/3 < p < 2N/3
p == r mod M.
```

Normalize:

```text
mu_N(r) = W_N(r) / sum_s W_N(s)
u_a(r)  = 1/|A_a| on A_a
nu_N    = mu_N - u_a.
```

The verifier induces two frozen coefficient functions on the reflection-orbit
coordinates:

```text
gamma_F3_a    first-three q286 singular-mode coefficient
gamma_full_a  full q286 action coefficient
```

with:

```text
F3_a(mu)   = <mu, gamma_F3_a>
Full_a(mu) = <mu, gamma_full_a>.
```

The receipt verifies on the frozen selected residues that:

```text
<u_a, gamma_F3_a> = 0
```

up to floating error.  The maximum absolute error is:

```text
1.0039712117215771e-16
```

## Exact bad branch

In centered discrepancy form, the q286 non-rescue branch is:

```text
<nu_N, gamma_F3_a>   <= -0.3
<nu_N, gamma_full_a> <= -<u_a, gamma_full_a>.
```

For the seven frozen residues, the local-uniform full-action baseline is:

```text
minimum: 0.7110192034986899
mean:    1.083620180782198
maximum: 1.2391609565397612
```

So the full-action bad inequality is not a tiny perturbation.  It asks the
actual prime-pair discrepancy to erase a positive baseline of size roughly
`0.71..1.24` in principal-normalized units.

## New candidate

Candidate:

```text
Signed Pair-Correlation Cone K_a
```

Mechanism: describe actual strict-central prime-pair discrepancies `nu_N` by
fixed signed moment, covariance, or binary in-progressions inequalities strong
enough to rule out the two centered bad inequalities above.

Bridge: unlike L1 uniformity, the cone is built in the same coordinates as the
bad branch.  It asks only for estimates against `gamma_F3_a`, `gamma_full_a`,
or a small predeclared family that implies them.

Prediction: a surviving cone should imply:

```text
nu in K_a and <nu,gamma_F3_a> <= -0.3
    => <nu,gamma_full_a> > -<u_a,gamma_full_a>.
```

Falsifier: if an LP finds a reflected nonnegative synthetic measure satisfying
the proposed cone and both bad-branch inequalities, that cone is insufficient.

Smallest useful test: choose one non-post-hoc cone family and run the LP
falsifier on the frozen seven operator rows in
`evidence/q286-signed-pair-correlation-definition.json`.

Novelty label: `new-to-this-task`.

Promotion gate: a cone must survive LP falsification, have a sourced analytic
path to actual prime-pair measures, and receive independent mathematical
review before it can become more than a proof candidate.

## What the coefficient geometry says

Across the seven frozen residues:

```text
cosine(gamma_F3_a, centered gamma_full_a):
  minimum 0.7795203896833228
  mean    0.8387607557705606
  maximum 0.8764725525194792
```

This is important.  The first-three and full-action coefficient directions
are strongly positively aligned after centering.  That means a negative
first-three push naturally tends to push full action down too.  The rescue
cannot be explained by generic geometry; it must come from how the actual
prime-pair measure lands on the coefficient orbits.

The first-three sign split is fairly balanced but residue-dependent:

```text
negative first-three uniform mass:
  minimum 0.43636363636363645
  mean    0.5226551226551226
  maximum 0.5858585858585856

positive first-three uniform mass:
  minimum 0.4141414141414141
  mean    0.4773448773448773
  maximum 0.5636363636363638
```

This keeps the mass/landing formulation alive.  The theorem is probably not
"avoid all negative mass"; it is a signed landing-quality inequality.

## Abandon condition for the next lane

Do not continue a cone family if it fails either condition:

- it is not stated without using the measured pass/fail labels;
- it admits a synthetic reflected bad measure under the LP falsifier.

If every plausible cone reduces to a pointwise signed binary-prime correlation
estimate, that is a valid endpoint, not a failure of the research.  It means
the q286 observation has been reduced to the named hard analytic input.
