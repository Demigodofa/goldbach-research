# External Watanabe Goldbach paper triage

## Source

```text
local PDF: C:/Users/KevinPenfield/Downloads/1811.02415v7.pdf
arXiv:    https://arxiv.org/abs/1811.02415
title:    Definitive Proof of Goldbach's Conjecture
author:   Kenneth A. Watanabe
license:  arXiv non-exclusive distribution license in PDF metadata
```

## Decision

This source can be cited and used as external inspiration with
attribution.  It is not accepted here as a proof of Goldbach.

The useful part is a roughness-product baseline: approximate the
ordered prime-pair count for even numbers avoiding small prime
divisibility by multiplying `|P(n)|` by
`prod (p-2)/p` over small primes.

The dangerous part is the promotion from finite/product heuristics
and postulates to a universal proof.  The repo should not adopt that
promotion.

## Finite Checks

```text
check limit:                                  200000
rough rows checked:                           20507
error-envelope failures found:                0
Pi-star-minus-emax failures after 622 found:  0
rough lower-bound block counterexamples:      7
```

The broad lower-bound story has checked counterexamples.  Example:

```json
[
  {
    "prime_square_block_start_prime": 3,
    "block_range": [
      10,
      24
    ],
    "nonrough_minimum_row": {
      "n": 12,
      "ordered_prime_pair_count": 2,
      "rough_relative_to_sqrt": false
    },
    "rough_minimum_row": {
      "n": 10,
      "ordered_prime_pair_count": 3,
      "rough_relative_to_sqrt": true
    }
  },
  {
    "prime_square_block_start_prime": 31,
    "block_range": [
      962,
      1368
    ],
    "nonrough_minimum_row": {
      "n": 992,
      "ordered_prime_pair_count": 26,
      "rough_relative_to_sqrt": false
    },
    "rough_minimum_row": {
      "n": 1112,
      "ordered_prime_pair_count": 32,
      "rough_relative_to_sqrt": true
    }
  },
  {
    "prime_square_block_start_prime": 239,
    "block_range": [
      57122,
      58080
    ],
    "nonrough_minimum_row": {
      "n": 57602,
      "ordered_prime_pair_count": 734,
      "rough_relative_to_sqrt": false
    },
    "rough_minimum_row": {
      "n": 57692,
      "ordered_prime_pair_count": 736,
      "rough_relative_to_sqrt": true
    }
  }
]
```

## Candidate Reuse

Use the roughness-product baseline as a diagnostic feature for the
`Q=46189` packet landscape.  Compare it to the current kernel metrics:
`off_diagonal/diagonal_half`, `middle_A_to_10A`, non-middle
compensation, and source-pair mirror-block ranks.

This is finite external-source triage only.  It proves no lower-bound
theorem, no error-envelope theorem, no replacement-packet theorem, no
strict-central Goldbach theorem, and no Goldbach proof.
