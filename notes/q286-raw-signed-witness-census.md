# q286 raw signed witness census

Status: finite raw-action census and theorem-shaping falsifier.  This is not
a q286 threshold theorem, pointwise signed prime-correlation theorem,
strict-central Goldbach theorem, or proof of Goldbach.

## Question

After the coefficientwise minorant shortcut failed, the signed-witness route
remained:

```text
raw q286 signed action > 0  =>  T_N > 0.
```

This implication is valid because `T_N` is the total strict-central
binary-prime weight and every residue weight `W_N(r)` is nonnegative.  If no
strict-central prime pair exists, then every `W_N(r)=0`, so every signed sum is
exactly zero.

The finite question tested here is narrower:

```text
Is the raw q286 signed action positive for every even N>=10000
in the first twelve full M=10010 cycles?
```

Executable receipt:

```text
tools/build_q286_raw_signed_witness_census.py
evidence/q286-raw-signed-witness-census.json
```

## Result

The naive threshold candidate beginning at `10000` is falsified.

```text
base target:                   10000
cycles scanned:                12
targets per cycle:             5005
total even targets scanned:    60060
nonpositive raw signed action: 89
last nonpositive target:       88346
positive suffix in this scan:  cycle 8, target 90080
```

Nonpositive counts by cycle:

```text
cycle 0: 75
cycle 1:  3
cycle 2:  5
cycle 3:  4
cycle 4:  0
cycle 5:  0
cycle 6:  0
cycle 7:  2
cycle 8:  0
cycle 9:  0
cycle10:  0
cycle11:  0
```

Worst centered-to-principal ratio:

```text
target 14138: -1.876941273440844
```

The nonpositive cycle recurrence matters.  Cycles `4..6` are clean, but cycle
`7` has two nonpositive targets, `85496` and `88346`.  Therefore a finite clean
block is not by itself evidence of a monotone threshold.  Any eventual theorem
must either prove a threshold after `88346`, or give a residue/correlation
condition explaining why later recurrences cannot happen.

## Interpretation

This receipt does not weaken the signed-witness implication.  It only refutes
the earliest naive threshold version.

What survives:

```text
For all sufficiently large covered N,
prove raw q286 signed action(N) > 0.
```

What is falsified:

```text
For all even N>=10000,
raw q286 signed action(N) > 0.
```

The surviving statement is still a pointwise signed binary-prime correlation
theorem.  It is not a nonnegative sieve minorant and not a consequence of the
normalized q286 row geometry alone.

## Current proof obligation

Let the raw full action be written as

```text
RawFull(N) = principal_mean*T_N + CenteredError(N).
```

Then the exact sufficient inequality is

```text
CenteredError(N) > -principal_mean*T_N.
```

Equivalently, when `T_N>0` and the normalized expression is defined,

```text
centered_error(N) / principal(N) > -1.
```

For a Goldbach bridge, the unnormalized form is the one that matters:
`RawFull(N)>0` itself implies `T_N>0`; the normalized ratio is only a
diagnostic once existence is already present.

## Decision

Do not claim the q286 signed witness is eventually positive from this finite
suffix.  The next useful route is one of:

- extend the raw signed-witness census only as a predeclared threshold
  falsifier;
- prove a sourced pointwise signed correlation estimate for `RawFull(N)`;
- find a non-post-hoc residue/correlation selector that covers the nonpositive
  finite rows separately and predicts the clean suffix without using outcomes.

Goldbach remains open.
