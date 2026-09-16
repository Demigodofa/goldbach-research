# Mobius moment-square degree-5 source-start M=251 full prime sweep

## Question

The first complete fresh-scale sweep at `M=229` survived.  Does the next fresh
scale, `M=251`, also survive when every prime `p` in `[251, 502]` is checked
at the canonical source start?

## Mechanism

For `M=251`, use the original source-start construction:

```text
row_count = int((251**(1/.59))**.41) = 46
ell_freeze = row_count + row_count//2 = 69
canonical source start = row_count = 46
```

Then compute the three degree-5 component rows and the degree-5 total row for
every prime `p` in `[251, 502]`, testing:

```text
full < 0 and active/full > 1/2
```

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_start_m251_full_prime_sweep.py
evidence/mobius-moment-square-degree5-source-start-m251-full-prime-sweep.json
```

## Result

```text
scale:                            251
prime interval:                   251..502
prime rows:                       42
component rows:                   126
degree-5 total rows:              42
dominance rows:                   168
all rows pass signed dominance:   true
minimum slack above one half:     0.43435333637430296
weakest row:                      M=251, p=379, (00,12)
weakest active/full ratio:        0.934353336374303
maximum slack above one half:     0.6502274336812401
```

The checked primes are:

```text
251, 257, 263, 269, 271, 277, 281, 283, 293, 307,
311, 313, 317, 331, 337, 347, 349, 353, 359, 367,
373, 379, 383, 389, 397, 401, 409, 419, 421, 431,
433, 439, 443, 449, 457, 461, 463, 467, 479, 487,
491, 499
```

## Decision

The full `M=251` prime-row source-start sweep survives.  Together with the
full `M=229` sweep, this gives two adjacent complete fresh scales beyond the
original fixture.

The weakest row again occurs at prime `379` and component `(00,12)`.  Future
work should treat `p=379` as an attention point across nearby scales, while
preserving the boundary that this is still finite evidence only.

This is not a source-start theorem, not a source-window theorem, and not a
Goldbach proof.
