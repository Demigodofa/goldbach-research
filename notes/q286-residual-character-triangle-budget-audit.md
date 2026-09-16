# q286 residual character-triangle budget audit

Status: finite theorem-budget audit.  This is not a character-sum theorem,
signed binary-prime correlation theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.

## Question

The current live target is the residual lower-tail inequality:

```text
aligned(N) + <nu_N,h_a> > 0.
```

Could a full period-character theorem prove this by expanding `h_a` in
characters modulo `10010` and bounding every character discrepancy separately?

## Receipt

```text
tools/build_q286_residual_character_triangle_budget_audit.py
evidence/q286-residual-character-triangle-budget-audit.json
```

The receipt zero-extends the target-specific residual `h_a` to `U_10010`,
expands:

```text
h_a(u) = sum_chi c_chi chi(u),
```

and uses the triangle sufficient condition:

```text
|Delta_chi(N)| <= eps for all active chi
eps < aligned(N) / sum_chi |c_chi|.
```

## Result

```text
selected targets:                  7
actual full-positive rows:          5
triangle-certified positive rows:   4
active character count:             2859 .. 2879 of 2880
coefficient L1 burden:              34.558554300574116 .. 43.42360885557793
maximum reconstruction error:       3.2887841483560823e-15
```

The triangle route certifies the four easy later positive rows:

```text
1222142
1240888
1242118
1379072
```

but it fails exactly where the route is needed most.  The tight positive row
is again `94856`:

```text
aligned margin:                       0.1140460717392141
coefficient L1 burden:                34.558554300574116
uniform per-character budget:          0.003300082253073864
max actual character discrepancy:      0.12748865801232862
actual / budget ratio:                38.63196376198781
triangle bound / aligned margin:      12.887401532971005
```

## Decision

The full-character triangle route is too broad.  It converts one residual
functional into almost the entire character basis and then asks for
independent per-character control far stronger than the tight row exhibits.

This does not refute character methods.  It refutes the broad triangle route:

```text
bound every active period character independently
```

as an acceptance condition for the current q286 bridge.

The next proof object must preserve signed structure between channels, use a
much smaller residual dictionary, or source a genuinely one-sided estimate for:

```text
<nu_N,h_a>
```

rather than bounding all character channels independently.
