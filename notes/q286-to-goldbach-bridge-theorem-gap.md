# q286 to Goldbach bridge theorem gap

Status: theorem-shaped pivot and implication-gap certificate.  This is not a
q286 threshold theorem, signed prime-correlation theorem, strict-central
Goldbach theorem, or proof of Goldbach.

## Purpose

The q286 work has produced strong finite structure, but the current loop can
become endless if we keep auditing normalized rows.  A Goldbach proof needs a
bridge from the q286 action to existence of a prime pair for every even target,
not just positivity on checked q286 rows or selected residue classes.

This note states the candidate theorem that would be enough, identifies the
objects that must be proved about, and names the precise implication gaps left
by the current q286 evidence.

Novelty label: `new-to-this-task`.

Creative-tools status: `aha-candidate`.  The useful pivot is to move the live
question from normalized residue geometry to an unnormalized action whose
strict positivity itself creates a strict-central prime pair.

## Objects

Let

```text
M = 10010
a = N mod M
U = (Z/MZ)^*
A_a = {r in U : gcd(a-r,M)=1}
```

For an even target `N`, define the strict-central weighted binary-prime residue
mass

```text
W_N(r) =
  sum log(p)log(N-p)
```

over primes satisfying

```text
N/3 < p < 2N/3
p == r mod M
N-p is prime.
```

Let

```text
T_N = sum_{r in A_a} W_N(r).
```

If `T_N>0`, then `N` has a strict-central Goldbach representation, hence a
Goldbach representation.  The normalized measure

```text
mu_N(r) = W_N(r)/T_N
nu_N    = mu_N-u_a
```

is therefore downstream of existence.  Any theorem that starts by assuming
`mu_N` is defined cannot by itself prove Goldbach unless a separate positive
lower bound for `T_N` has already been proved.

## Candidate Bridge Theorem

Candidate, not proved:

There are explicit finite data `N0` and a finite exceptional set `E`, and for
each even residue `a mod M` there are q286 coefficient functions
`gamma_F3_a`, `gamma_full_a`, and an orthogonal residual `h_a` such that every
even `N>=N0` with `N mod M=a` satisfies an unnormalized signed-witness
inequality

```text
L_N =
  T_N * (
    uniform_full_a
    + alpha_a * <nu_N,gamma_F3_a>
    + <nu_N,h_a>
  )
```

with

```text
L_N > 0.
```

Since every `W_N(r)` is nonnegative, `L_N>0` implies at least one
`W_N(r)>0`, hence `T_N>0`.  A stronger sufficient form would be an
ordinary minorant

```text
0 < L_N <= T_N
```

or another nonnegative-weight lower-bound certificate, but coefficientwise
minorant structure is not logically necessary for existence.  A strictly
positive signed prime-pair sum is already an existence witness.

Then, after checking every even `N<N0` and every `N in E`, Goldbach follows.

## Required Complement Rescue Inequality

For every covered even target in the q286 tail lane, the current orthogonal
decomposition gives

```text
full(N) =
  uniform_full_a
  + alpha_a * first_three(N)
  + <nu_N,h_a>.
```

The exact rescue inequality is therefore

```text
<nu_N,h_a>
  > -uniform_full_a - alpha_a * first_three(N).
```

Equivalently, in the earlier complement notation

```text
A(N) = F3(N) + C(N)
S(N) = 1 + F3(N)
D(N) = max(0, 1-C(N)),
```

full positivity is

```text
S(N) > D(N)
```

whenever `C(N)<=1`; if `C(N)>1`, complement already supplies positive surplus.

In sign/landing form for the residual coefficient `h_a`, split its orbit
support into positive and negative parts:

```text
P_h = {orbit : h_a(orbit)>0}
N_h = {orbit : h_a(orbit)<0}.
```

Let the actual prime-pair mass on those parts have masses and average landings

```text
m_plus,  ell_plus
m_minus, ell_minus.
```

Then

```text
<nu_N,h_a> = m_plus*ell_plus - m_minus*ell_minus
```

up to the already-accounted uniform centering, and the complement rescue
obligation is

```text
m_plus*ell_plus
  + uniform_full_a
  + alpha_a * first_three(N)
> m_minus*ell_minus.
```

This is the current finite-dimensional theorem target.  A proof must control
the signed landing of actual binary prime-pair mass, not just the size of
`nu_N`.

## What The q286 Evidence Does Prove

The current receipts prove finite identities and finite measurements:

- the q286 coefficients induce exact centered functionals on the strict-central
  residue measure;
- on the seven frozen selected targets,
  `gamma_full_centered = alpha_a*gamma_F3_a + h_a` with numerical
  orthogonality error at floating precision;
- the aligned-only term is positive on those seven selected targets;
- the two bad selected targets fail because the orthogonal residual is too
  negative;
- generic L1, variance, chi-square, small-channel, and simple label-dictionary
  routes are too blunt for the observed rows.

These are proof-shaping facts, not a universal theorem.

## Gap From q286 To Every Even Integer

The implication from the q286 result to Goldbach is currently open at these
places:

1. Coverage gap.  The checked q286 rows and selected residues do not cover
   every even integer.  A theorem must quantify over every even residue
   `a mod M`, or provide a disjoint covering of all even targets by other
   proved lanes.
2. Boundary gap.  Early failures such as `14138` and `14996` show that the
   residual-overturn phenomenon is real.  A proof must either include them in
   a finite checked exceptional set or prove a condition excluding their
   behavior after an explicit threshold.
3. Normalization gap.  `mu_N` and `nu_N` are only defined when `T_N>0`.
   Positivity of a normalized q286 action cannot be the first existence
   theorem.  The bridge must be stated as an unnormalized signed action, an
   unnormalized minorant, or must be paired with an independent lower bound
   for `T_N`.
4. Minorant gap.  A coefficientwise nonnegative minorant would be especially
   useful, but it is stronger than necessary.  The current q286 full action may
   instead be a signed witness: direct proof of its strict positivity would
   imply existence, but the proof would have to be a pointwise signed
   prime-correlation theorem.
5. Analytic gap.  The required lower-tail estimate
   `<nu_N,h_a> > -uniform_full_a-alpha_a*first_three(N)` is a pointwise signed
   binary-prime correlation theorem.  Existing AP upper bounds, marginal lower
   bounds, and broad uniformity estimates do not imply it at the needed
   strength.
6. Assembly gap.  Even a successful strict-central theorem for large `N` needs
   a finite verification below `N0` and a written endpoint/noncentral assembly
   showing the strict-central lane really implies the original Goldbach
   statement.

## Smallest Useful New Mathematical Problem

Define the q286 Complement Rescue Inequality Problem:

For fixed `M=10010` and every even residue `a mod M`, find explicit
`N0(a)` and `eta_a(N)>0` such that every even `N>=N0(a)` with `N mod M=a`
and `first_three(N)<-0.3` satisfies

```text
<nu_N,h_a>
  >= -uniform_full_a - alpha_a*first_three(N) + eta_a(N).
```

If this is proved only after proving `T_N>0`, it is a rescue theorem inside an
already-proved Goldbach-strength statement.  To act as a bridge toward
Goldbach, it must be reformulated as an unnormalized signed-witness inequality,
for example

```text
sum_{r in A_a} W_N(r) * h_a(r)
  >= -T_N*(uniform_full_a + alpha_a*first_three(N)) + eta'_a(N),
```

where the resulting full unnormalized action is strictly positive.  A
coefficientwise lower-bound/minorant step would be a stronger alternative, but
not the only bridge.

## Falsifier

The candidate bridge fails in its current q286-only form if any of the
following happens:

- a synthetic or actual admissible row satisfies the q286 rescue inequality but
  the proposed unnormalized minorant is not positive;
- the rescue inequality holds only after assuming `T_N>0` with no independent
  existence input;
- a fresh predeclared residue class outside the selected q286 lane produces
  full-action failure after the same threshold;
- no sourced pointwise binary-prime correlation theorem can control the exact
  residual statistic, leaving the route equivalent to Goldbach-in-progressions.

## Decision

The next strategy should not be another broad q286 audit.  The next useful
step is to build or reject an unnormalized q286 witness:

```text
positive raw q286 signed action => T_N>0.
```

If that witness cannot be proved directly, and no nonnegative minorant can be
extracted, then q286 remains a diagnostic and theorem generator rather than a
direct Goldbach bridge.  The surviving mathematical target is the complement
rescue inequality above, explicitly understood as a pointwise signed
binary-prime correlation theorem.

## Coefficientwise Minorant Audit

`tools/build_q286_unnormalized_witness_minorant_audit.py` generated
`evidence/q286-unnormalized-witness-minorant-audit.json`.

Result: the existing q286 aggregate coefficient is sign-indefinite:

```text
negative unit coefficients: 1228 / 2880
positive unit coefficients: 1652 / 2880
minimum coefficient: -516900.46805732243
maximum coefficient: 1770168.728092706
```

Every even target residue modulo `10010` has both positive and negative
coefficient values in its admissible support.  Therefore positive scalar
multiples of the existing q286 full-action coefficient cannot be a
coefficientwise nonnegative minorant for `T_N`.

Decision: demote the nonnegative-minorant shortcut for this coefficient, but
preserve the signed-witness route.  A direct proof that the unnormalized q286
full action is strictly positive would still imply a Goldbach pair; it is just
not a nonnegative sieve lower bound.

## Raw Signed-Witness Census

`tools/build_q286_raw_signed_witness_census.py` generated
`evidence/q286-raw-signed-witness-census.json`.

Result: the signed-witness implication is valid, but the naive threshold
starting at `10000` is false on the checked finite block.

```text
base target:                   10000
cycles scanned:                12
targets per cycle:             5005
total even targets scanned:    60060
nonpositive raw signed action: 89
last nonpositive target:       88346
positive suffix in this scan:  cycle 8, target 90080
```

Nonpositive raw signed-action counts by cycle:

```text
75, 3, 5, 4, 0, 0, 0, 2, 0, 0, 0, 0
```

This is a useful warning.  Cycles `4..6` are clean, but cycle `7` has two
nonpositive targets.  Therefore a finite clean run does not establish a
monotone threshold.  Any eventual signed-witness theorem must either start
after the last checked nonpositive target or prove a reason that later
recurrences cannot happen.

## Raw Signed-Witness Threshold Holdout

`tools/build_q286_raw_signed_witness_threshold_holdout.py` generated
`evidence/q286-raw-signed-witness-threshold-holdout.json`.

Result: the first fresh holdout after the prior scan preserves the
`90080` threshold candidate.

```text
fresh base target:              130120
fresh end target:               250238
fresh cycles:                   12
fresh even targets scanned:     60060
fresh nonpositive raw actions:  0
fresh worst target:             194384
fresh worst centered ratio:     -0.8263994946792758
```

Combined with the earlier clean suffix, this gives finite evidence:

```text
RawFull(N)>0 on every checked even N from 90080 through 250238
checked consecutive even targets: 80080
```

This supports but does not prove an eventual threshold after `88346`.
The active falsifier is any future unchanged full-cycle holdout at or above
`90080` containing `RawFull(N)<=0`.

## Local Main-Term Positivity Audit

`tools/build_q286_local_main_term_positivity_audit.py` generated
`evidence/q286-local-main-term-positivity-audit.json`.

Result: the existing assembled q286 coefficient has positive local main-term
average on every even target residue modulo `10010`.  For

```text
A_a = {r in U_10010 : gcd(a-r,10010)=1},
```

the support average

```text
LocalMean(a) = (1/|A_a|) sum_{r in A_a} c(r)
```

has `0` nonpositive cases across all `5005` even residues.  The
local/principal ratio ranges from `0.6039353780830684` at residue `4124` to
`1.5716524655081636` at residue `8856`.

Decision: the raw signed-witness bridge is not blocked by a local-main-term
sign obstruction.  The remaining gap is sharper: prove the unnormalized
pointwise centered-error inequality

```text
CenteredError_a(N) > -LocalMain_a(N)
```

for all sufficiently large even `N == a mod 10010`, then finite-check the
remaining targets.  This is still a signed binary-prime correlation theorem,
not a consequence of the finite coefficient audit.

## Centered Character-Burden Audit

`tools/build_q286_centered_character_burden_audit.py` generated
`evidence/q286-centered-character-burden-audit.json`.

Result: the remaining centered coefficient does not have full `10010`
character support.  Every nonzero support descends to a lower CRT natural
modulus:

```text
10, 14, 22, 26, 70, 130, 154, 286
```

The top three supports carry `0.9960328792226287` of the centered character
energy:

```text
11x13 -> 286, energy fraction 0.70082890257693
7x11  -> 154, energy fraction 0.15893232135172436
5x7   -> 70,  energy fraction 0.13627165529397434
```

Decision: the next theorem should be stated as a lower-modulus character
correlation problem:

```text
RawFull(N)
  = LocalMain_a(N)
  + E_286(N)
  + E_154(N)
  + E_70(N)
  + E_tail(N),
```

with

```text
E_286(N)+E_154(N)+E_70(N)+E_tail(N) > -LocalMain_a(N).
```

This sharpens the analytic target but does not prove any of the needed
prime-pair estimates.

## Three-Support Action Decomposition

`tools/build_q286_three_support_action_decomposition.py` generated
`evidence/q286-three-support-action-decomposition.json`.

Result: on a selected `10`-target hard-row fixture, the three dominant supports
preserve the full raw-action sign decisions:

```text
full-action positive count:             7
principal+E_286+E_154+E_70 positive:    7
tail sign-decision changes:             0
nonpositive targets in both versions:   14138, 14996, 88346
tail/principal ratio range:             -0.09817000756761152..0.09363293903366753
```

Decision: the lower-modulus compression is action-level useful on the tested
hard rows.  The tail is small enough on this fixture to be treated as a
separate explicit bound, but this remains finite evidence.  The theorem still
requires a pointwise signed-prime correlation estimate for
`E_286+E_154+E_70+E_tail`.

## Three-Support Known-Extremals Audit

`tools/build_q286_three_support_known_extremals_audit.py` generated
`evidence/q286-three-support-known-extremals-audit.json`.

Result: the selected-row simplification does not survive the stronger
known-extremals fixture.  Across `113` deduplicated targets built from every
recorded census raw-action failure, census cycle minima, fresh holdout cycle
minima, the fresh global minimum, and the selected hard fixture, the tail
changes `16` sign decisions.  All `16` occur inside the census raw-action
failure source; fresh holdout cycle minima have `0` tail sign changes.

Decision: a pure three-support theorem is too narrow for the current bridge.
The useful object is the full signed support-tail control inequality

```text
LocalMain_a(N) + E_286(N) + E_154(N) + E_70(N) + E_tail(N) > 0,
```

possibly split into an early/boundary tail-control regime and a later
tail-stable threshold regime.  This is still a pointwise signed binary-prime
correlation obligation, not a consequence of the finite q286 evidence.

## Signed Support-Tail Control Definition

`tools/build_q286_signed_support_tail_control_definition.py` generated
`evidence/q286-signed-support-tail-control-definition.json`.

This receipt turns the known-extremals falsifier into the exact
principal-scaled proof obligation:

```text
A_N = P_N + D_N + R_N
D_N = E_286(N)+E_154(N)+E_70(N)
R_N = E_14(N)+E_26(N)+E_130(N)+E_10(N)+E_22(N)
A_N/P_N = 1+d_N+r_N.
```

The sufficient inequalities are:

```text
1+d_N >= eta_a(N) > 0
r_N > -eta_a(N).
```

The support tail is small in coefficient energy but decisive on the known
boundary failures: all `16` observed support-tail flips are negative-tail
kills of positive principal-plus-top-three partial sums, not positive-tail
rescues.  Therefore the next theorem is tail lower-control, not tail
discarding.

## Support-Tail Stability Window Audit

`tools/build_q286_support_tail_stability_window_audit.py` generated
`evidence/q286-support-tail-stability-window-audit.json`.

Result: in the checked post-boundary window `90080..250238` and the fresh next
arithmetic cycle `250240..260248`, the support-tail split has no sign flips:

```text
targets checked:                         85085
full-action nonpositive count:           0
principal+dominant nonpositive count:    0
negative-tail kill count:                0
positive-tail rescue count:              0
```

The tail still frequently erodes positive partial margins, but not enough to
erase them in this finite later fixture.  This supports, but does not prove,
a boundary/later split for the signed support-tail control theorem.

## Support-Tail Coefficient Minorant Audit

`tools/build_q286_support_tail_coefficient_minorant_audit.py` generated
`evidence/q286-support-tail-coefficient-minorant-audit.json`.

Result: the stronger coefficientwise shortcut fails for every even target
residue modulo `10010`:

```text
partial coefficients all positive: 0/5005
full coefficients all positive:    0/5005
separated tail-control passes:     0/5005
```

Thus the q286 bridge cannot be proved for arbitrary nonnegative residue mass.
It must use actual prime-pair distribution.  The remaining proof obligation is
to constrain the landing of `W_N(r)` on the positive and negative coefficient
cells strongly enough that

```text
sum_r W_N(r)*(P+D)(r) > 0
sum_r W_N(r)*R(r) > -sum_r W_N(r)*(P+D)(r).
```
