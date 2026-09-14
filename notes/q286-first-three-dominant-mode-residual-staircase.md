# q286 dominant-mode residual staircase

Status: finite residual-staircase diagnostic.  Goldbach is not proved.

This note turns the selected q286 dominant-mode portfolio into the literal
"bolt it on and ask what is left" ledger.

Receipt:
`evidence/q286-first-three-dominant-mode-residual-staircase.json`

## Mechanism Tested

The previous split fixed:

```text
prefix = (2,6), (3,1), (4,8), (4,2)
tail   = (3,11), (5,5), (4,4), (1,3), (5,3), (2,4), (4,6)
```

For each selected target, the dominant-mode floor is equivalent to:

```text
partial_portfolio_sum >= required_portfolio_for_floor.
```

The staircase freezes the prefix/tail channel order and records, after each
cumulative added channel, which selected rows are still under-rescued, which
selected failures have been over-rescued, and the exact remaining requirement.

## Measured Shape

On the full selected fixture, the first stage that clears every selected clear
row is the four-channel prefix:

```text
(2,6), (3,1), (4,8), (4,2)
```

At that stage, all selected clears pass, but five selected deficits are still
over-rescued:

```text
24424, 13822, 55864, 164598, 1222142
```

The first stage that eliminates every over-rescued selected deficit is also
the first stage matching the full selected dominant-floor classification: the
complete eleven-channel portfolio.

The tail does not behave like a monotone safety add-on.  The measured stage
transitions include:

- adding `(4,4)` makes `164598` fail again;
- adding `(1,3)` makes `55864` fail, but also temporarily knocks clear
  target `13556` below the floor;
- adding `(5,3)` restores `13556` while making `13822` fail;
- adding `(4,6)` makes the last over-rescued deficits `24424` and `1222142`
  fail again.

The final full-stage slack ranges match the tail-ablation result:

```text
failure slack: maximum -0.0088331796
clear slack:   minimum +0.0095640903
```

The worst remaining final deficit is `55864`, with remaining requirement about
`0.0992285758`.

## Consequence

This supports the fixture interpretation:

```text
prefix lower-bound theorem
    plus
full tail classification / exclusion / complement theorem.
```

It also warns that the tail is signed, not merely corrective.  A proof cannot
just say "add the tail" as a positive reserve; some tail channels push clears
down before later channels repair them.  The missing theorem must control the
signed cumulative portfolio as an arithmetic object, or replace the selected
tail with a separate deficit-exclusion/complement/lower-support theorem.

This is finite selected-fixture evidence only.  It is not a uniform theorem
and not a proof of Goldbach.
