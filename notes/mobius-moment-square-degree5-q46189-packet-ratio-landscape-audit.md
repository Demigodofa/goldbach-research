# Mobius moment-square degree-5 Q46189 packet-ratio landscape audit

## Question

After `q=16302` falsifies the broad frozen `50A..60A` selector, does
the one-coordinate active/full ratio target survive on the broader
same-source packet landscape?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_packet_ratio_landscape_audit.py
evidence/mobius-moment-square-degree5-q46189-packet-ratio-landscape-audit.json
```

## Result

```text
same-source denominators:              35
nonadverse denominators:               34
six-pair packets:                      33
raw scalar-identity rows:              33
Q=46189 ratio minus half:              -0.0026909627652296764
nonadverse ratio-above-half count:     34 / 34
nonadverse ratio <= half count:        0
weakest nonadverse denominator:        38038
weakest nonadverse ratio minus half:   0.0763534077069109
strongest nonadverse denominator:      25935
strongest nonadverse ratio minus half: 0.8678946944880965
50A..60A share failures still present: [16302]
```

The weakest positive nonadverse row is:

```text
q:                         38038
factorization:             {'2': 1, '7': 1, '11': 1, '13': 1, '19': 1}
role:                      original_replacement
ratio minus half:          0.0763534077069109
ordered source pairs:      6
raw scalar:                -0.07083636365889087
```

For comparison, the adverse row is:

```text
q:                         46189
ratio minus half:          -0.0026909627652296764
ordered source pairs:      6
raw scalar:                -0.07475328212536138
```

## Decision

The `50A..60A` selector remains demoted: `q=16302` is still a
positive-share failure for that frozen distance window.  But the
one-coordinate active/full ratio target survives the broader finite
landscape.  `Q=46189` is the unique row below one half, while all
`34/34` nonadverse same-source denominators are above one half.

This changes the useful theorem target.  Do not rescue the distance
selector; aim at a symbolic active/full energy-ratio inequality for
the packet landscape, starting with the tight pair `Q=46189` versus
`q=38038`.

This is finite diagnostic evidence only.  It proves no one-coordinate
active/full ratio theorem, packet-landscape theorem, strict-central
Goldbach theorem, or Goldbach proof.
