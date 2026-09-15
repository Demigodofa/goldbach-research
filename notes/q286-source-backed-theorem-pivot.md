# q286 source-backed theorem pivot

Status: theorem-shaping note after a falsified simplification.  This is not a
q286 threshold theorem, signed prime-correlation theorem, strict-central
Goldbach theorem, or proof of Goldbach.

Novelty label: `new-to-this-task`.

Creative tools checked: `pursue-curiosity` and `inventive-synthesis`.  The
useful move is to stop treating the q286 evidence as a search for another
finite pattern and instead extract a standalone weighted binary-prime sign
problem.

## Why this is a pivot

The latest q286 audits close three tempting but insufficient routes:

- static bad-support dictionary: falsified by the moving lower-face support;
- coefficientwise nonnegative edge minorant: falsified on every checked
  post-discovery row;
- unweighted mass-majority cone: falsified by `18/196` post-discovery rows
  that rescue despite having more mass on negative rescue coefficients.

What survives is not a label theorem and not an unweighted cone.  It is a
coefficient-sensitive signed landing inequality.

## Source-backed external boundary

Bennett, Martin, O'Bryant, and Rechnitzer, *Explicit bounds for primes in
arithmetic progressions*, Illinois J. Math. 62 (2018), 427-532;
arXiv:1802.00085, gives explicit one-dimensional AP estimates for
`pi(x;q,a)`, `theta(x;q,a)`, and `psi(x;q,a)` for fixed moduli.  Their theorem
statements give bounds of the form:

```text
|theta(x;q,a)-x/phi(q)| < c_theta(q) * x/log(x)
|pi(x;q,a)-Li(x)/phi(q)| < c_pi(q) * x/(log x)^2
```

with explicit thresholds, and the paper points to accompanying computational
data for q-specific constants.

Earlier local q286 notes record the q-specific BMOR constants used here:

```text
c_pi = 0.0008772, x_pi = 86,891,851
c_psi = 0.0008379, x_psi = 85,882,271
c_theta = 0.0008411, x_theta = 85,881,413
```

The important boundary is that these are AP prime-count inputs.  They do not
by themselves control a binary convolution, and they do not prove a signed
17-channel q286 functional is positive.

## The extracted problem

Fix the modulus `M` used by the strict-central q286 residue calculation, and
let

```text
A_a = {r mod M : gcd(r,M)=1 and gcd(a-r,M)=1}
```

for an even target residue `a = N mod M`.

For a signed q286 coefficient function `Phi_a` on `A_a`, define the raw
weighted binary-prime sign sum:

```text
B_Phi(N) =
  sum_{r in A_a} Phi_a(r)
    sum_{N/3 < p < 2N/3
         p == r mod M
         N-p prime}
      log(p) log(N-p).
```

If `B_Phi(N)>0`, then at least one strict-central prime pair exists, because
all inner pair weights are nonnegative and the sum is zero when no such pair
exists.

The q286 edge route supplies candidate `Phi_a` from the frozen full signed
functional, or equivalently from the target-dependent edge expression
`gap-required` after clearing the normalization.

## Required complement rescue inequality

For the signed edge coefficient

```text
beta_{a,N}(r) = gap_{a,N}(r) - required_{a,N},
```

split the actual strict-central pair mass into positive and negative regions:

```text
P+ = {r : beta_{a,N}(r) > 0}
P- = {r : beta_{a,N}(r) < 0}
M+ = mass_N(P+)
M- = mass_N(P-)
A+ = average beta on P+ under mass_N
A- = average -beta on P- under mass_N.
```

The exact complement rescue condition is:

```text
M+ * A+ > M- * A-.
```

Equivalently, when both sides have positive mass:

```text
A+ / A- > M- / M+.
```

The mass-balance audit proves only finite checked evidence for this shape.  A
Goldbach bridge would need the same inequality as a theorem for all covered
large even `N`, plus a finite remainder check.

## What the borrowed ideas do and do not buy

DFT: useful.  The q286 functional is a finite residue convolution object, so
Fourier/character coordinates can diagonalize the finite residue layer and
identify which characters carry the signed weight.  DFT does not itself give
one-sided positivity.

Linear programming and Farkas duality: useful.  They can turn candidate
coefficient cones into explicit separating inequalities or show that a
proposed finite set of local constraints is insufficient.  They do not supply
prime-pair lower bounds.

Riesz-Thorin interpolation: probably only secondary.  Interpolation can bound
operator norms between finite or analytic function spaces, but the missing
claim is a pointwise lower bound for a signed prime-pair sum.  Norm control
would help only if it makes the nonprincipal signed part smaller than a
separate positive main term.

Pigeonhole/AP marginals: already demoted.  Earlier q286 AP-count bridge work
showed one-dimensional AP counts leave too much room for reflected residue
sets to avoid each other.  A pair-correlation theorem is needed.

Closed graph theorem: not relevant as a proof engine here.  The active maps
are finite-dimensional and therefore automatically continuous; topology is not
the missing ingredient.

## Continue gate

Continue the q286 lane as a proof engine only if the next move attacks one of
these proof obligations:

- a published or newly proved fixed-modulus binary Goldbach-in-progressions
  estimate with explicit error small enough for `B_Phi(N)>0`;
- a direct circle-method, dispersion, or character-sum bound for the specific
  signed q286 functionals `Phi_a`;
- a Farkas/LP certificate showing that a stated source-backed family of
  binary-prime inequalities implies the q286 signed witness;
- a finite remainder plan paired with one of the analytic theorems above.

## Abandon/sleep gate

Put the q286 lane to sleep as a Goldbach proof engine, while preserving it as
finite structure, if the next work would be only:

- more row audits without a predeclared theorem implication;
- another static label dictionary;
- another unweighted support or mass cone;
- AP marginal bounds without binary convolution control;
- normalized `mu_N` positivity without an independent route to `T_N>0`.

## New mathematical problem

Name: `q286-WBSS`, the q286 weighted binary-prime sign-sum problem.

Problem: for the explicit finite family of signed coefficient functions
`Phi_a` produced by the q286 edge/full functional, prove an explicit threshold
`N0` such that every covered even `N>=N0` satisfies:

```text
B_Phi(N) > 0.
```

Then verify every even `N<N0` computationally.  This would imply Goldbach for
the covered target class.  It is not yet known to be easier than Goldbach; its
value is that it names exactly what the q286 evidence would have to prove.

## Main-term sign refinement

`tools/build_q286_wbss_main_term_sign_audit.py` generated
`evidence/q286-wbss-main-term-sign-audit.json`.

The extracted problem is not blocked by a bad local-uniform mean.  On the
`196` post-discovery rows, the frozen full coefficient and the edge
`beta=gap-required` coefficient both have positive local-uniform mean on
`196/196` rows.

The sufficient L1 budgets are:

```text
full coefficient: 0.020711496156757627..0.06441548422792709
edge beta:        0.026797640365636533..0.18715353351948102
```

So a main-term-plus-error proof route is logically coherent: prove actual
binary-prime orbit mass stays within the relevant L1 budget, or prove
`B_Phi(N)>0` directly.  The hard missing input remains pointwise binary-prime
distribution, not q286 coefficient orientation.
