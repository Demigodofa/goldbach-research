# q286-WBSS coefficient-discrepancy budget HOLD

## Question

Finite evidence is no longer the acceptance condition.  Can the q286-WBSS
adverse-drag target be stated as an exact analytic estimate whose proof would
pay the remaining bridge?

## Theorem-shaped budget

Let

```text
Delta_{d,s}(N) = Pi_{N,d}(s) - U_{a,d}(s)
a = N mod 10010
d in {70,130,154,286}
```

where `Pi` is the actual strict-central binary-prime left-prime residue mass
modulo `d`, and `U` is the corresponding local uniform residue mass.  The
four-modulus projection formula gives

```text
E_d(N) = sum_s c_{d,s}(a) Delta_{d,s}(N)
adverse_drag(N) = A_-(N) = sum_d max(0, -E_d(N))
```

The direct one-sided sufficient theorem is:

```text
max(0, -E_d(N)) <= B_d(N) for each d
sum_d max(0, B_d(N)) < local_main(N)
```

for every sufficiently large covered even `N`.

A stronger but easier-to-state per-residue corollary is:

```text
|Delta_{d,s}(N)| <= eta_d(N) for every projected residue s
sum_d L1_d * eta_d(N) < local_main(N)
```

because `|E_d(N)| <= L1_d * eta_d(N)`.

## Exact coefficient budget

From `evidence/q286-wbss-four-modulus-projection-formula.json`:

```text
L1_70:              32.74465079141701
L1_130:              7.137019529057295
L1_154:             84.29326326706732
L1_286:            248.78706848859338
total L1:          372.962002076135
minimum local main: 0.6039353780830684
equal eta cap:       0.0016192946592982506
```

So a very strong sufficient theorem would prove

```text
|Delta_{d,s}(N)| < 0.0016192946592982506
```

for every projected residue in the four moduli and every sufficiently large
covered even `N`.  That is sufficient, not necessary; a one-sided theorem for
the actual coefficient directions could be weaker and still close the bridge.

## Finite context

The current finite calibration remains useful only as calibration and
falsifier data:

```text
checked rows:                         348
adverse_drag < local_main rows:       348 / 348
tightest known adverse-drag target:   1124642
tightest adverse-drag ratio:          0.23148438379145228
tightest adverse-only expectation:    0.6835668462365216
```

It does not prove the universal estimate.  The fresh holdout already rejected
literal frozen per-modulus constants, with modulus `286` exceeding its fitted
horizon value on two fresh rows.

## HOLD

The missing object is a source-backed pointwise fixed-modulus binary-prime
residue discrepancy estimate, or a sharper one-sided signed estimate, strong
enough to prove one of the displayed inequalities for all sufficiently large
covered even `N`.

No such theorem is currently present in the repository.  Therefore the state
is:

```text
HOLD_for_pointwise_prime_pair_correlation_estimate
```

This receipt proves no fixed-modulus binary-prime discrepancy theorem,
pointwise adverse-drag theorem, q286 threshold theorem, strict-central
Goldbach theorem, or Goldbach proof.
