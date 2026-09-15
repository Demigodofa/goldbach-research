# q286 raw signed witness threshold holdout

Status: finite fresh holdout for a threshold candidate.  This is not an
eventual threshold theorem, pointwise signed prime-correlation theorem,
strict-central Goldbach theorem, or proof of Goldbach.

## Question

The previous raw signed-witness census showed:

```text
last nonpositive raw signed action: 88346
finite positive suffix start:       90080
prior scanned end:                  130118
```

This receipt asks whether the first fresh full-cycle block after that prior
scan immediately falsifies the `90080` threshold candidate.

Executable receipt:

```text
tools/build_q286_raw_signed_witness_threshold_holdout.py
evidence/q286-raw-signed-witness-threshold-holdout.json
```

## Candidate

Candidate, not proved:

```text
RawFull(N) > 0 for every even N >= 90080.
```

If proved, this would imply `T_N>0` for every covered strict-central target,
because the absence of strict-central prime pairs makes every nonnegative
residue weight `W_N(r)` equal zero and therefore makes the raw signed action
zero.

## Fresh holdout

The holdout is the next twelve complete `M=10010` cycles after the prior
census:

```text
fresh base target:              130120
fresh end target:               250238
fresh cycles:                   12
fresh even targets scanned:     60060
fresh nonpositive raw actions:  0
fresh worst target:             194384
fresh worst centered ratio:     -0.8263994946792758
```

Together with the previous positive suffix, the finite checked positive
interval is now:

```text
start target:                90080
end target:                  250238
consecutive even targets:    80080
nonpositive raw actions:     0
```

Cycle-by-cycle fresh nonpositive counts:

```text
0,0,0,0,0,0,0,0,0,0,0,0
```

## Interpretation

This is meaningful finite evidence because it tested new rows after the
observed positive suffix, rather than re-sorting selected q286 rows.  It also
does not repeat the earlier mistake of treating a clean block as a theorem:
the prior census already showed clean cycles `4..6` followed by two failures
in cycle `7`.

Epistemic state:

```text
90080 threshold candidate: supported by finite holdout, not proved
from-10000 threshold:      directly contradicted
signed-witness route:      active
```

Reactivation/falsifier:

```text
Any future unchanged full-cycle holdout at or above 90080
with RawFull(N)<=0 falsifies the current threshold candidate.
```

Promotion gate:

An eventual theorem still needs an analytic reason later recurrences cannot
happen: a pointwise signed binary-prime correlation estimate, an explicit
formula bound for this coefficient, or a non-post-hoc residue/correlation
condition plus finite checking of its complement.

Goldbach remains open.
