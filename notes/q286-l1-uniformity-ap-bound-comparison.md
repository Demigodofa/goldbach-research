# q286 L1-uniformity AP-bound comparison

Status: source-backed strategy decision.  This is not an AP-uniformity theorem,
binary Goldbach-in-progressions theorem, q286 threshold theorem, signed
correlation theorem, or Goldbach proof.

## Question

The demoted L1 cone candidate showed that each selected residue has a
nearest-bad radius:

```text
minimum: 0.05724560696825869
mean:    0.09720394355055242
maximum: 0.11764562474360012
```

The pivot question was whether published fixed-modulus prime-in-arithmetic-
progression bounds can supply an explicit AP-uniformity radius in this range.

## Source

The comparison uses Bennett, Martin, O'Bryant, and Rechnitzer, *Explicit
bounds for primes in arithmetic progressions*, Illinois J. Math. 62 (2018),
427-532; arXiv:1802.00085.

The executable receipt downloads the authors' public computation tables:

```text
http://www.nt.math.ubc.ca/BeMaObRe/c-psi-theta-pi/c_all_rounded.txt
http://www.nt.math.ubc.ca/BeMaObRe/x-psi-theta-pi/x0-all-xm-xe.txt
```

and records their SHA-256 hashes in:

```text
evidence/q286-l1-uniformity-ap-bound-comparison.json
```

## Comparison model

For a one-dimensional AP theorem at modulus `q`, BMOR supplies constants of
the shape:

```text
|theta(x;q,a) - x/phi(q)| < c_theta(q) x/log(x)
|pi(x;q,a) - Li(x)/phi(q)| < c_pi(q) x/log(x)^2
```

After normalizing by total prime mass and applying a crude union bound across
all reduced residue classes, both yield the first-order probability L1 proxy:

```text
phi(q) * c / log(x).
```

This is only a marginal residue-distribution proxy.  The q286 cone uses a
binary reflected strict-central prime-pair measure modulo `10010`, so a
successful marginal comparison would still need a bridge theorem.

## Evidence

BMOR table rows used by the receipt:

```text
q=143:
  c_theta=0.0008409, c_pi=0.0008769
  x_theta=85881413, x_pi=86891851
  marginal L1 proxy at threshold: theta 0.0055236128640936645, pi 0.00575640009385811

q=286:
  c_theta=0.0008411, c_pi=0.0008772
  x_theta=85881413, x_pi=86891851
  marginal L1 proxy at threshold: theta 0.00552492660243689, pi 0.005758369440451972

q=10010:
  c_theta=0.0008291, c_pi=0.0008646
  x_theta=10723716, x_pi=11763491
  marginal L1 proxy at threshold: theta 0.14750510727702712, pi 0.15294654772000832
```

The `q=143` and `q=286` proxies are below the computed L1 radii, but they are
not the cone denominator.  The strict-central binary measure lives on the
assembled period `10010`.

At `q=10010`, the marginal proxy is larger than even the largest computed
nearest-bad L1 radius.  To close the minimum radius by this blunt proxy would
require:

```text
theta-style x >= 1.303568776017155e+18
pi-style    x >= 7.776406097957707e+18
```

This is before paying any additional cost to pass from one-dimensional AP
counts to the reflected binary prime-pair measure.

## Decision

Published fixed-modulus AP bounds are real and useful background, but they do
not close the current L1 cone route.  The denominator lift from `286` to
`10010` is the decisive issue: the q286 bound alone looks strong because
`phi(286)=120`, while the actual assembled period has `phi(10010)=2880`.

This should stop the loop of larger label-only or blunt-uniformity audits.
The next proof route needs a mathematical definition that controls the actual
signed operator:

- coefficient-sensitive signed character moments;
- q286 mass/landing inequalities on reflection-orbit sign classes;
- PSD/covariance constraints for the strict-central prime-pair measure;
- or a genuine binary Goldbach-in-progressions theorem for the same reflected
  pair measure and signed functionals.

## Rethink

The local AP theorem is not wrong; it is just answering the wrong problem.  The
hole is not closing because "residue classes are eventually uniform" is too
coarse for the observed q286 mechanism.  The observed rescue is signed and
correlated.  The mathematical object to define next is therefore not a bigger
audit set, but the cone of prime-pair measures whose signed coefficient action
cannot enter:

```text
F3(mu) <= -0.3
full_action(mu) <= 0.
```

If that cone can be described by non-post-hoc arithmetic inequalities, LP or
Farkas duality can become proof machinery.  If it cannot, the q286 data stays
finite evidence rather than a theorem.
