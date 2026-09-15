# q286 centered character-burden audit

Status: finite coefficient-spectrum diagnostic and theorem-shaping result.
This is not a binary-prime correlation theorem, q286 threshold theorem,
strict-central Goldbach theorem, or proof of Goldbach.

## Question

The local main-term audit left the unnormalized target

```text
RawFull(N) = LocalMain_a(N) + CenteredError_a(N)
CenteredError_a(N) > -LocalMain_a(N).
```

The new question is whether `CenteredError_a` really requires a full
`q=10010` prime-pair theorem, or whether the fixed coefficient descends to a
smaller CRT character burden.

## Result

`tools/build_q286_centered_character_burden_audit.py` generated
`evidence/q286-centered-character-burden-audit.json`.

The centered coefficient has no full `10010` support.  Every nonzero character
support descends to a lower natural modulus, with reconstruction and descent
errors at floating precision.

```text
nonzero natural moduli:              10, 14, 22, 26, 70, 130, 154, 286
full 10010 support present:          false
dominant supports for >99% energy:   3
top-three energy fraction:           0.9960328792226287
largest support energy fraction:     0.70082890257693
```

The three dominant supports are:

```text
support 11x13 -> natural modulus 286, energy fraction 0.70082890257693
support 7x11  -> natural modulus 154, energy fraction 0.15893232135172436
support 5x7   -> natural modulus 70,  energy fraction 0.13627165529397434
```

The remaining supports together carry less than half a percent of the centered
character energy.

## Interpretation

This is a useful compression.  The q286 bridge does not need to begin as a
generic `U_10010` uniformity theorem.  The fixed coefficient's centered burden
is concentrated on three lower CRT supports:

```text
286 = 2*11*13
154 = 2*7*11
70  = 2*5*7
```

The next theorem target should therefore be a three-dominant-support signed
correlation statement plus an explicit small-tail bound, not another broad
residue scan and not a simple label dictionary.

## New Problem

Define the q286 Three-Dominant-Support Signed Correlation Problem:

For every even residue `a mod 10010`, decompose the raw action as

```text
RawFull(N)
  = LocalMain_a(N)
  + E_286(N)
  + E_154(N)
  + E_70(N)
  + E_tail(N).
```

Prove explicit eventual bounds

```text
E_286(N) + E_154(N) + E_70(N) + E_tail(N)
  > -LocalMain_a(N)
```

for all sufficiently large even `N == a mod 10010`, with `LocalMain_a(N)>0`
given by the previous audit and with a finite verification below the threshold.

The coefficient audit says this is the right reduced problem to try.  It does
not prove the needed prime-pair estimates.
