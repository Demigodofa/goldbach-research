# Mobius moment-square degree-5 Q46189 source-pair bucket compensation audit

## Question

Can the `q=38038` replacement-packet bucket compensation be localized
in exact ordered source-conductor-pair cross terms, and how does that
differ from `Q=46189`?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_source_pair_bucket_compensation_audit.py
evidence/mobius-moment-square-degree5-q46189-source-pair-bucket-compensation-audit.json
```

## Result

```text
q=38038 middle A..10A:             -0.939992990438763
q=38038 non-middle sum:            0.09269980585259228
q=38038 off/diag-half:             -0.8472931845861708
q=38038 top-four non-middle sum:   0.07765412336759717
q=38038 top-four non-middle share: 0.8376945631480589
Q=46189 middle A..10A:             -0.2840414834738627
Q=46189 non-middle sum:            -0.721340442056593
Q=46189 off/diag-half:             -1.0053819255304557
```

The top four `q=38038` non-middle terms are exactly the ordered
mirror block on source pairs `(143,266)` and `(266,143)`.

## Decision

The `q=38038` survivor is not protected by a uniformly friendly bucket
profile.  Its `middle_A_to_10A` bucket is very adverse, but the
near/far/tail buckets compensate enough to keep the total above `-1`.
The exact source-pair cross-term decomposition localizes most of that
positive non-middle compensation in the mirror block
`(143,266)/(266,143)`.

`Q=46189` differs in the direction that matters: its aggregate
non-middle contribution is negative, so there is no analogous
non-middle rescue.  This supports a mirror-source-pair compensation
theorem target, but remains finite diagnostic evidence only.

This proves no source-pair compensation theorem, mirror-block theorem,
replacement-packet compensation theorem, strict-central Goldbach
theorem, or Goldbach proof.
