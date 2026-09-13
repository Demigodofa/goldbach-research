# q286 complement-versus-alignment theorem obligation

Status: theorem obligation and finite-vector obstruction; Goldbach not proved.

Date: 2026-09-13.

## Fixed objects

The implemented q286 first-three functional has modulus `286` and `120` unit
residues.  For an even target residue `a = N mod 286`, let

```text
A_a = {r in U_286 : a-r is also in U_286}.
```

The admissible counts are `99`, `108`, `110`, or `120`, depending on `a`.
Let `W_N(r)` be the strict-central weighted prime-pair mass with
`p == r mod 286`:

```text
W_N(r) = sum log(p)log(N-p)
```

over strict-central prime pairs `N/3 < p < 2N/3`.  Let

```text
mu_N = (sum_{r in A_a} W_N(r)) / |A_a|,
d_N(r) = W_N(r) - mu_N  for r in A_a,
d_N(r) = 0              otherwise.
```

The first-three q286 contribution is exactly the finite inner product

```text
F_3(N) = <c_a, d_N>,
```

where `c_a` is the real q286 first-three coefficient vector centered on the
same admissible set.  In principal-normalized form, the implemented L2 bound is

```text
B_2(N) = ||c_a||_2 ||d_N||_2 / P(N).
```

The measured singular values defining the uncentered first-three q286
functional are approximately

```text
158279.09383760378
124234.1882436279
21476.920434701242
```

Across target residues, the centered admissible coefficient norms measured from
the implementation are:

```text
||c_a||_2 range: 737130.2261974699 .. 2216691.1337206536
||c_a||_1 range: 5385068.449447754 .. 10612733.570460552
```

## Sufficient theorem candidate

After excluding and finitely checking the boundary/full-negative layer, a
direct sufficient theorem is:

```text
F_3(N) / P(N) >= -0.4 * B_2(N)
full_without_first_three(N) / P(N) > 0.4 * B_2(N)
```

at least for every target in the first-three lower-tail set.  Together these
give positive recombined strict-central action on that set.  The non-tail set
still needs its own quantified complement statement, but it is not the active
failure mode in the current diagnostics.

## Finite-vector obstruction

The alignment inequality cannot be proved from finite-vector geometry,
admissible support, nonnegativity, and total mass alone.

Fix any target residue `a` with nonzero centered coefficient vector `c_a`.
For any total mass `M > 0`, set the uniform admissible mass
`mu = M / |A_a|`.  For sufficiently small `epsilon > 0`, define

```text
d(r) = -epsilon * c_a(r)  for r in A_a,
W(r) = mu + d(r).
```

Because `c_a` is centered on `A_a`, the new weights still have total mass
`M`; because `epsilon` can be chosen small, all `W(r)` are nonnegative.  But

```text
<c_a, d> = -epsilon ||c_a||_2^2
||c_a||_2 ||d||_2 = epsilon ||c_a||_2^2,
```

so the alignment cosine is exactly `-1`.  Therefore every ceiling
`theta < 1`, including `.4`, is false for arbitrary admissible nonnegative
weights.  A proof of the measured `.4` behavior must use arithmetic facts
about actual binary prime-pair weights, not only residue support or Cauchy
geometry.

## What must be proved or identified

The first missing theorem is a coefficient-matched binary-prime residue
discrepancy estimate:

```text
<c_a, d_N> >= -0.4 ||c_a||_2 ||d_N||_2
```

for all sufficiently large relevant even `N`, or for all such `N` in the
first-three lower-tail regime.

The second missing theorem is a complement lower-envelope estimate:

```text
full_without_first_three(N) / P(N)
    > 0.4 ||c_a||_2 ||d_N||_2 / P(N).
```

This complement statement is not equivalent to a local admissibility theorem.
It must use the actual remaining strict-central coefficient action.  If the
only available route to either statement is pointwise prime-pair occupancy in
specific residue channels strong enough to imply restricted binary Goldbach
classes, then this lane has reached a hard theorem-equivalence obstruction
rather than a proof.

## Current finite evidence

The window receipt
`q286_first_three_tail_alignment_complement_window_receipt` checks this
sufficient condition on finite windows.  On global cycles `105..136`, with
tail threshold `.3` and alignment ceiling `.4`, it found three tail targets
`1222142, 1323632, 1379072`; all three were certified by the measured
complement, and none was an actual full-action negative.

The same sufficient condition fails at boundary target `14138`, where the
complement is only `0.018073313793834367` principal and the target is actually
full-negative in the assembled strict-central action.  Thus any theorem route
must split the boundary layer from the eventual estimate.
