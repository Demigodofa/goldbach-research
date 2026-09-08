"""Earlier-bound correction for semiprime pairs sharing ANY prime factor.

Owner: Kevin's mathematical investigation; purpose: isolate the remaining
coprime composite-pair correlation without computing a high prime square.
The identity and input ranges were independently checked by Sol, 2026-09-08.

Let C be the cubic survivors' composite set and L the diagonal-only bound.
Distinct semiprimes c1,c2 with a common factor have gcd equal to exactly one
prime ell. Write c1=ell*r,c2=ell*s, r!=s, r,s>z; necessarily ell divides N.
Squares cause no exception. If T=N/ell>=2(z+1), put
  e_ell=sum_{odd prime p<=z}1_prime(T-p), d_ell=1_prime(T/2).
Then G(T)-2e_ell-d_ell counts these ordered off-diagonal pairs exactly.
There is no overlap in the small-prime subtraction because T>2z.
Subtracting d_ell removes each center diagonal even if a nonsquare center
has two distinct prime factors and thus occurs under both labels.
Consequently
  L + sum_ell(G(T)-2e_ell-d_ell)
    = G(N)-2*#{unordered distinct COPRIME C-pairs summing to N}.

For earlier parity-correct lower bounds J(T), use max(0,J(T)-2e_ell-d_ell).
This contribution is even, nonnegative and <=the exact contribution. It
dominates the same-least-factor correction from the same input J: its
eligibility T>=2(z+1) is weaker and its exclusion set p<=z is smaller.
Each distinct off-diagonal pair has only one common prime, so no correction
is counted twice. The resulting bound can exceed the older raw bound R.

All ell and cofactor flags are within the earlier cubic cofactor range:
ell<=N/(2(z+1))<=H/(z+1), and T-p<=T-3<=H/(z+1). Thus T<=B+3<=E,
where B=odd_floor(E/2) and E>=6 is the prior prefix end. At most two primes
ell>z divide even N, giving total gain<=N/(z+1)=O(N**(2/3)); the gain
vanishes on powers of two. No exception-elimination theorem is proved.
"""
from cubic_batch import _block_shape
from parity_bound_bootstrap import _odd_floor, recover_parity_primes


def shared_prime_gain(bounds: list[int], target: int, *, exact: bool = False) -> dict:
    """Return an additive correction to canonical L, NOT to the refined J.

    Conditional input meaning: every supplied value is <=G at its earlier
    label and has G's parity. These premises are not certified by type/range
    checks. Canonical generate_prefix(...,same_factor=True) supplies them.
    Adding this gain on top of a same-factor gain would double count pairs.
    With exact=True, only truthful earlier PARITIES are required: count the
    distinct cofactor-prime pairs directly from the recovered smaller flags.
    This computes the complete shared-prime correction, without a high-target
    prime square or a complete exact-count prefix. At most two smaller
    cofactor targets are inspected. No primality oracle is used here.
    """
    if type(exact) is not bool:
        raise ValueError("exact must be an exact boolean")
    _, high, z = _block_shape(target, 1)
    endpoint, classified, primes = recover_parity_primes(bounds)
    if target <= endpoint:
        raise ValueError("target must follow the earlier bound prefix")
    if z > classified or _odd_floor(high // (z + 1)) > classified:
        raise ValueError("earlier prime flags do not cover the cubic cofactor range")
    prime_set = set(primes)
    small = [p for p in primes if p <= z]
    terms = []
    for ell in primes:
        if 2 * ell * (z + 1) > target:
            break
        if ell <= z or target % ell:
            continue
        t = target // ell
        if t > endpoint or t - 3 > classified:
            raise RuntimeError("required earlier input is outside the proved range")
        excluded = sum(t - p in prime_set for p in small)
        diagonal = int(t // 2 in prime_set)
        prior = bounds[(t - 6) // 2]
        candidate = prior - 2 * excluded - diagonal
        if not exact and candidate % 2:
            raise RuntimeError("earlier parity contradicts the recovered center flag")
        gain = (2 * sum(z < p < t - p and t - p in prime_set for p in primes)
                if exact else max(0, candidate))
        terms.append({"shared_prime": ell, "earlier_target": t,
                      "prior_bound": prior, "small_prime_exclusions": excluded,
                      "cofactor_diagonal": diagonal, "gain": gain})
    gain = sum(term["gain"] for term in terms)
    if len(terms) > 2 or gain > target // (z + 1):
        raise RuntimeError("input labels contradict the proved correction ceiling")
    return {"target_even": target, "cubic_cutoff": z, "input_prefix_end": endpoint,
            "classified_last_odd": classified, "gain": gain, "terms": terms,
            "gain_ceiling": target // (z + 1),
            "largest_prior_target": max((term["earlier_target"] for term in terms), default=0),
            "exact_shared_correction": exact,
            "input_meaning": ("conditional on truthful earlier PARITIES" if exact else
                              "conditional on earlier parity-correct LOWER bounds"),
            "add_to": "diagonal-only canonical L; replaces any same-factor gain"}
