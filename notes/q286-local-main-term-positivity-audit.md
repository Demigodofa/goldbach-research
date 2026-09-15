# q286 local main-term positivity audit

Status: finite coefficient-side diagnostic.  This is not a binary
Goldbach-in-progressions theorem, q286 threshold theorem, strict-central
Goldbach theorem, or proof of Goldbach.

## Question

After the coefficientwise nonnegative-minorant shortcut failed, the surviving
bridge is a raw signed witness:

```text
RawFull(N)>0 => T_N>0.
```

This can only plausibly become an eventual theorem if the fixed q286
coefficient has a positive local main term in every even target residue.  For

```text
M = 10010
a = N mod M
U = (Z/MZ)^*
A_a = {r in U : gcd(a-r,M)=1},
```

this audit computes

```text
LocalMean(a) = (1/|A_a|) sum_{r in A_a} c(r),
```

where `c(r)` is the assembled raw q286 coefficient on `U_10010`.

## Result

`tools/build_q286_local_main_term_positivity_audit.py` generated
`evidence/q286-local-main-term-positivity-audit.json`.

Every even residue modulo `10010` has positive local main term:

```text
even target residues checked:      5005
nonpositive local main terms:      0
support size range:                1485..2880
local/principal ratio range:       0.6039353780830684..1.5716524655081636
weakest residue:                   4124
strongest residue:                 8856
```

The local main-term real values range from `26574.674023291926` to
`69156.65725917745`, against global principal mean
`44002.512499999146`.  The imaginary local means are zero up to floating
precision, with maximum absolute mean about `1.2156747741841028e-9`.

## Interpretation

This keeps the raw signed-witness route alive in a sharper form.  The existing
coefficient cannot be a coefficientwise nonnegative minorant, but its local
singular/equidistribution prediction is positive in every target residue.

The remaining theorem is not another finite q286 scan.  It is the pointwise
centered-error inequality

```text
RawFull(N) = LocalMain_a(N) + CenteredError_a(N)
CenteredError_a(N) > -LocalMain_a(N)
```

for all sufficiently large even `N == a mod 10010`, followed by a finite check
below the threshold.  Stating the error relative to `T_N` would be circular
unless an independent lower bound for `T_N` has already been proved; the useful
bridge must be an unnormalized signed-prime correlation theorem.

## New Problem

Define the q286 Local Positive-Main-Term Signed Correlation Problem:

For each even residue `a mod 10010`, prove an explicit positive main term
`LocalMain_a(N)` for the raw q286 signed action and an explicit threshold
`N0(a)` such that every even `N>=N0(a)` with `N mod 10010=a` satisfies

```text
CenteredError_a(N) > -LocalMain_a(N).
```

If proved directly for the unnormalized raw action, this would imply
`T_N>0` and therefore a strict-central Goldbach representation for all
sufficiently large targets in every residue class.  The current audit only
checks the coefficient-side positivity required for that route.
