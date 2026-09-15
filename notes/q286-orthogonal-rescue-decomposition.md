# q286 orthogonal-rescue decomposition

Status: coefficient decomposition and theorem obligation.  This is not an
orthogonal residual bound, signed pair-correlation theorem, q286 threshold
theorem, or Goldbach proof.

## Question

The signed pair-correlation definition identified the exact bad branch:

```text
<nu_N,gamma_F3_a>   <= -0.3
<nu_N,gamma_full_a> <= -<u_a,gamma_full_a>.
```

The next question is whether the full-action failure is caused by the aligned
first-three direction itself or by a remaining perpendicular component.

Executable receipt:

```text
tools/build_q286_orthogonal_rescue_decomposition.py
evidence/q286-orthogonal-rescue-decomposition.json
```

## Decomposition

For each target residue `a`, use the uniform-weighted reflection-orbit inner
product and decompose:

```text
gamma_full_centered = alpha_a * gamma_F3_a + h_a
<h_a,gamma_F3_a>_u = 0.
```

For actual prime-pair discrepancy `nu_N`, this gives:

```text
full(N) =
  uniform_full_a
  + alpha_a * first_three(N)
  + <nu_N,h_a>.
```

The q286 row is positive exactly when:

```text
<nu_N,h_a> > -uniform_full_a - alpha_a * first_three(N).
```

## Evidence

Across the seven frozen selected targets/residues:

```text
alpha_a:
  minimum 0.9958093998571658
  mean    1.0074643494421425
  maximum 1.0202017493335502

uniform_full_a:
  minimum 0.7110192034986899
  mean    1.083620180782198
  maximum 1.2391609565397612

orthogonality error:
  maximum 4.309053114326389e-15
```

The aligned-only full action is positive for all seven selected targets:

```text
aligned_only_positive_target_count: 7 / 7
actual_full_positive_target_count:  5 / 7
```

The two actual bad-branch targets are exactly the targets where the
orthogonal residual erases that positive aligned margin:

```text
orthogonal_residual_erases_aligned_margin_targets:
  14138
  14996
```

Compact rows:

```text
target   F3/P          full/P        aligned-only/P   h/P
14138   -0.895014587  -0.876941273   0.257627710    -1.134568983
14996   -0.992369421  -0.203502246   0.056253960    -0.259756206
94856   -0.585152037   0.012576466   0.114046072    -0.101469605
1222142 -0.307587760   0.945716266   0.919994972     0.025721294
1240888 -0.274684102   0.934161262   0.895919810     0.038241452
1242118 -0.286426743   0.674104300   0.728531409    -0.054427109
1379072 -0.339413884   0.944998867   0.897493145     0.047505722
```

## Decision

This sharply narrows the next theorem target.

The first-three aligned component is not what makes the selected rows fail.
Even the failing early rows have positive aligned-only margin.  They fail
because the orthogonal residual `h_a` is too negative.

Therefore the next proof route should not try to control the whole residue
measure, and should not retry generic L1 or variance balls.  The next route is
a one-residual signed moment lower bound:

```text
<nu_N,h_a> > -uniform_full_a - alpha_a * first_three(N)
```

after whatever finite boundary layer is explicitly checked.

## Candidate Theorem

Candidate, not proved:

For every sufficiently large even `N` in the q286 first-three tail lane, the
orthogonal residual component satisfies:

```text
<nu_N,h_a> >= -epsilon_a(N)
```

where `epsilon_a(N)` is smaller than the aligned-only margin
`uniform_full_a + alpha_a*first_three(N)`.

This would imply `full(N)>0` without needing a global uniformity theorem.

## Falsifier

A proposed residual cone is falsified if an LP finds a reflected nonnegative
synthetic measure with:

```text
aligned-only full action > 0
<nu,h_a> <= -aligned-only full action.
```

The early targets `14138` and `14996` show that such residual overturns are
real in the boundary layer.  Any eventual theorem must split them away or
explain why their residual behavior cannot persist.

## Next Move

Build a residual-cone LP:

```text
variables: reflected orbit masses
fixed:     gamma_F3_a, gamma_full_a, h_a
cone:      one predeclared lower-bound family for <nu,h_a>
bad:       F3<=-0.3 and h<=-uniform_full-alpha*F3
```

If the cone fails, preserve the synthetic bad measure.  If it survives, seek
the external analytic estimate or finite boundary split that would put actual
prime-pair measures inside it.
