# q286-WBSS centered-support inequality ledger

## Question

What exact lower-modulus centered signed-correlation bounds would keep the
q286-WBSS centered error above the positive local factor?

## Receipt

```text
tools/build_q286_wbss_centered_support_inequality_ledger.py
evidence/q286-wbss-centered-support-inequality-ledger.json
```

## Raw Ledger

Let `P0_a(N)` denote the ordinary strict-central binary-prime principal main
scale for `N == a mod 10010`, produced inside the same raw major/minor arc
argument.  For a support bucket `B`, let `K_B(N)` be its centered contribution
before any division by the actual mass `T_N`.

A sufficient ledger shape is

```text
K_B(N) >= -beta_B * P0_a(N)
```

for `B in {286,154,70,tail}`, with

```text
sum_B beta_B < m_a / principal_mean
```

for every sufficiently large covered `N`.

This is not a normalized `T_N` theorem.  If a proof first assumes actual
`T_N>0`, it collapses to conditional distribution control.

## Budget Model

The receipt fixes one explicit sufficient budget:
coefficient-max-absolute proportional allocation with a `10%` reserve.

```text
weakest local factor ratio:       0.6039353780830684
allocated negative budget total:  0.5435418402747616
unallocated reserve:              0.060393537808306826
```

Bucket obligations:

```text
dominant_286: modulus 286
dominant_154: modulus 154
dominant_70:  modulus 70
tail:         moduli 10,14,22,26,130
```

The tail carries only `0.003967120777371179` of centered character energy, but
it still needs either a combined raw lower bound or separate support bounds
whose budgets sum no larger than the tail allocation.

## Decision

`TARGET_centered_support_inequality_ledger_open`.

The q286 route now has a four-bucket raw inequality ledger.  A future theorem
attempt must pay the raw lower bounds for `286`, `154`, `70`, and the tail, or
replace this sufficient ledger with a sharper source-backed inequality.  This
is stronger than finite row evidence and proves no pointwise centered-error
theorem.

This is a theorem-obligation ledger only.  It proves no source theorem fit,
major/minor arc estimate, pointwise centered-error estimate, signed
prime-correlation theorem, positive-mass theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.
