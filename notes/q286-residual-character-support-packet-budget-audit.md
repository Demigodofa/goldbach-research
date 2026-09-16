# q286 residual character support-packet budget audit

Status: finite theorem-budget audit.  This is not a support-packet theorem,
character-sum theorem, signed binary-prime correlation theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof.

## Question

The full-character triangle route was too broad because it expanded the
target-specific residual into almost all `2880` characters of `U_10010` and
then paid for every character independently.

Can a smaller dictionary earn its keep if the characters are aggregated into
CRT conductor-support packets before any theorem budget is imposed?

## Mechanism

Use the same exact character expansion as the previous audit, but group
characters by nonempty support among the prime factors `5`, `7`, `11`, and
`13`.  This gives `15` signed support packets.

For each target, write

```text
full(N) = aligned(N) + sum_g A_g(N)
```

where `A_g(N)` is the exact signed action of one support packet.

The signed packet budget is:

```text
eps < full_actual(N) / sum_g |A_g(N)|.
```

This keeps cancellation inside each packet and asks for a signed packet
estimate, not independent control of every character.

## Receipt

```text
tools/build_q286_residual_character_support_packet_budget_audit.py
evidence/q286-residual-character-support-packet-budget-audit.json
```

## Result

```text
selected targets:                           7
actual full-positive rows:                  5
support packets per row:                   15
maximum packet reconstruction error:        9.992007221626409e-16
tight positive row:                         94856
tight signed packet abs sum:                0.22679673835446376
tight signed packet budget:                 0.055452588891044076
tight rowwise adverse packet margin:       -0.05008710016072493
positive-only component envelope sum:       0.20972827541918798
tight positive-only component margin:      -0.09568220367997388
all-row component envelope sum:             1.2001268887790304
```

The tight row `94856` is the decisive split:

```text
actual full action:        0.012576466293799767
aligned action:            0.1140460717392141
signed residual action:   -0.10146960544541431
sum |packet actions|:      0.22679673835446376
signed budget:             0.055452588891044076
adverse packet sum:        0.16413317189993903
rowwise adverse margin:   -0.05008710016072493
```

So packetization does reduce the source budget from the previous sub-percent
residual sign-split regime to about `5.545%` on the tight row, but only if the
theorem preserves signed packet structure.

The one-sided adverse-packet route fails even on the actual tight row.  The
row is positive only because favorable packets offset adverse packets.  The
stricter disconnected component envelopes also fail the tight row, including
the envelope fitted only on positive rows.

## Decision

The smaller support-packet dictionary earns a next test, but not as an
adverse-only envelope.  The live theorem-shaped target is now a signed
support-packet binary-prime correlation estimate:

```text
sum_g A_g(N) > -aligned(N)
```

with packet-level signed control, or an equivalent source-backed estimate for
`<nu_N,h_a>`.

Do not promote this to a theorem.  The audit is finite and uses the seven
frozen signed-pair operator targets.  It proves no support-packet estimate, no
uniform character-sum bound, no q286 threshold theorem, no strict-central
Goldbach theorem, and no Goldbach proof.
