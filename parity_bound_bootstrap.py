"""Canonical finite lower-bound recursion whose own outputs preserve prime parity.

Owner: Kevin's research; purpose: test a composable bound without exact G input.
For a cubic band, P=A-C is the odd-prime indicator. Set
  L(N)=[A*A]_N-2[A*C]_N+C(N/2).
The last term is zero unless N/2 is an odd C-entry. Then
  G(N)-L(N)=[C*C]_N-C(N/2)
is twice the number of unordered DISTINCT composite pairs. Thus L<=G and
L=G mod2. In particular L(2m)%2 is the prime flag of odd m, even for negative L.
The exact signed factorization L=[(P-C)*(P+C)]_N+C(N/2) is verified in
factored_linear_barrier.py. Its standard linear-sieve plug-in fails the
stated optimistic leading-term benchmark; this does not make L negative.

The conditional batch requires correct input PARITIES; integer typing and
L(6)%2=1 do not establish that truth. The canonical generator starts with
L(6)=1 and proves each new stage using only earlier output parities. Positivity
never gates propagation. No exact-count bootstrap, full prime square, or
ordinary prime sieve is called in the production pipeline. The small-prime
square-start marking is the explicit arithmetic construction, not a prime oracle.
This proves finite lower bounds and their parity invariant, not that L>0
universally. Its external novelty has not been assessed.

Analytic guarantee, independently checked by Sol on 2026-09-08:
For every fixed a>0, all but O_a(X/log(X)**a) even N in [X,2X] satisfy
  L(N) >= (1-log(2)**2-O(loglog(X)/log(X))) * M(N),
  M(N) = singular_series(N)*N/log(N)**2.
Consequently L(N)>=M(N)/2>0 eventually outside that exceptional set.
The threshold and constants are not numerical; this does not certify an
uncomputed finite interval or show the exceptional set is empty.

A stronger exceptional-SIZE guarantee is now checked in
prime_pair_transfer.py and monotone_euler_cutoff.py: for some fixed
epsilon>0, L(N)>0 for all but
O(X**(1-epsilon)) even N in [X,2X], for sufficiently large X. More precisely
epsilon=delta/4 for any sufficiently small fixed positive delta, after a
permissible monotone cutoff choice in the analytic proof. This does
not upgrade the half-main-term lower bound above to that smaller exceptional
set. The exponent and starting threshold are not numerical, and individual
remaining targets are not certified by an almost-all count.

Proof dependencies and argument, retained with the bound they concern:
1. Put Y=2X and z=floor(cuberoot(X-3)). Let C0 contain the composites <=Y
   with least prime factor >z, S its semiprimes, and T=C0 minus S. For
   sufficiently large X, T consists only of triprimes. Each factor lies
   between z+1 and Y/(z+1)**2, so #T=O(X/log(X)**3) by the prime upper
   bound. If D(U;N)=[U*U]_N-U(N/2), monotonicity of distinct unordered
   pairs gives 0<=D(C0;N)-D(S;N)<=2*#T. The canonical composite set at
   N is contained in C0; hence L(N)>=G(N)-D(S;N)-O(X/log(X)**3).
2. S(n) is half the ordered count of p*r=n, p,r>z, plus half the flag
   for a prime square p*p, p>z. For q<=log(Y)**b and (h,q)=1, all such
   factors are coprime to q. Apply Siegel-Walfisz to
     sum_{z<p<=y/z} [pi(y/p;q,h/p)-pi(z;q,h/p)],
   where h/p denotes h times the inverse of p modulo q, then PNT
   partial summation in p. Uniformly 0<=y<=Y, the semiprime
   progression count equals phi(q)**-1 times integral(k_z(t),z*z,y),
   with error O_{a,b}(Y/log(Y)**a) for every fixed a,b. Both counts and
   integrals are zero for y<=z*z. Squares cost O(sqrt(Y)/log(Y)), and
   the summed inner errors use sum_p(y/p+z)=O(Y). The exact kernel is
     k_z(t)=log(log(t)/log(z)-1)/log(t), t>z*z; zero otherwise.
   It is the derivative of half the ordered double prime integral.
3. Write ell=log(Y), Q=ell**b and take disjoint major arcs about h/q,
   q<=Q and (h,q)=1, of half-width 2Q/Y; eventually 4Q**3<Y. Abel
   summation of (2)
   gives S_hat(h/q+beta)=mu(q)/phi(q)*V(beta)+O(Y/ell**d), where
     V(beta)=integral(k_z(t)*exp(2*pi*i*beta*t),z*z,Y).
   The residue sum and beta integration lose at most 2b log powers;
   start (2) with more saving. Take b>2a+30 and d>3b+a+10. Replacing
   S_hat**2 by its major term costs O(Y/ell**(d-3b)) uniformly in N.
4. Off those arcs, Dirichlet with floor(Y/Q) gives Q<q<=Y/Q and
   |alpha-h/q|<=q**-2. Split the ordered factor sum into O(ell**2)
   dyadic blocks, with both scales between z/2 and Y/z, and retain
   the product cutoff p*r<=Y. Salmensuu Lemma 4.2, r=1, parameter
   c=a+12, gives each block's squared modulus O(Y**2/ell**c).
   The squared sum loses four log powers. Prime squares are negligible.
   Thus sup_minor |S_hat|**2=O(Y**2/ell**(a+8)). Parseval and #S<=Y
   bound the sum of squared minor-arc coefficients by Y**3/ell**(a+8).
   A coefficient exceeds Y/ell**3 for at most O(Y/ell**(a+2)) targets.
5. The kernel has variation O(1/ell) on [z*z,Y], so |V(beta)| is at most a
   constant times min(Y,1/|beta|)/ell. The truncated singular series
   has modulus <=sum_{q<=Q}1/phi(q)=O(sqrt(Q)), using
   phi(q)>=sqrt(q/2). Extending the beta integral to the real line
   therefore costs O(Y/(sqrt(Q)*ell**2)). The resulting real integral
   is J(N)=integral(k_z(t)*k_z(N-t),t).
6. The absolute Ramanujan tail T_Q(n)=sum_{q>Q}mu(q)**2*|c_q(n)|/phi(q)**2
   is <=Q**(-1/2)*F(n), where
     F(n)=product_p(1+sqrt(p)*|c_p(n)|/(p-1)**2).
   Put u_p=sqrt(p)/(p-1)**2 and
     h_p=(sqrt(p)/(p-1)-u_p)/(1+u_p)>=0.
   Then F(n)=K*product_{p|n}(1+h_p), K=product_p(1+u_p)<infinity,
   and h_p=O(p**(-1/2)). Expanding the nonnegative divisor product
   gives sum_{n<=Y}F(n)<=K*Y*product_p(1+h_p/p)=O(Y). Thus the tail
   is <=1/ell outside O(Y*ell/sqrt(Q)) targets. This replaces the
   truncated series by the full Goldbach singular series.
7. Trim J at t or N-t<X/ell**3, costing O(X/ell**5). On the remainder,
   k_z(t)=(log(2)+O(log(ell)/ell))/ell. Therefore uniformly X<=N<=2X,
     J(N)=(log(2)**2+O(loglog(X)/log(X)))*N/log(N)**2.
   Combining (3)-(6) gives D(S;N)=(log(2)**2+O(loglog(X)/log(X)))*M(N)
   outside O_a(X/log(X)**a) targets; removing the diagonal costs <=1.
   The full singular series is uniformly positive on even N, so the
   additive O(X/log(X)**3) errors are absorbed into the relative error.
8. The already checked prime-only Vaughan mean-square theorem and the
   unweighted conversion in notes/adaptive-moment-almost-all.md give
   G(N)=(1+O(loglog(X)/log(X)))*M(N) with the same exceptional-set bound.
   Union the two exceptional sets and apply (1). Finally the positive
   series log(2)=2*sum_{j>=0}(1/3)**(2*j+1)/(2*j+1) is <25/36, so
   1-log(2)**2>671/1296=1/2+23/1296. This proves the stated half bound.

Analytic sources:
* Siegel-Walfisz: Ford, large sieve notes, handwritten p.63, Theorem SW,
  https://ford126.web.illinois.edu/sieve_notes_large_sieve.pdf . Separate
  the principal-character main term; the cancellation bound is nonprincipal.
* Type II estimate: Salmensuu, Lemma 4.2, printed p.9,
  https://arxiv.org/pdf/2106.00778 . Its bounded coefficients and explicit
  product cutoff are required here; no prime-pair distribution is assumed.
* Prime mean square: Vaughan, The Hardy-Littlewood Method, 2nd ed.,
  Theorem 3.7, p.36, with the normalization already checked in
  notes/fixed-precision-weight-obstruction.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from time import perf_counter

from cubic_batch import _block_shape, _build_survivors, _extract, _pack_binary
from cubic_sieve import exact_floor_cuberoot


def _odd_floor(n: int) -> int:
    return n if n % 2 else n - 1


def recover_parity_primes(bounds: list[int]) -> tuple[int, int, list[int]]:
    """Conditional decoder: returns prefix end, classified odd end, prime list.

    The list is indexed by targets6,8,...; L(2m) has list index m-3.
    An arbitrary integer sequence passing these checks has no primality meaning.
    """
    if not isinstance(bounds, list) or not bounds:
        raise ValueError("nonempty contiguous integer bound prefix required")
    if any(type(value) is not int for value in bounds) or bounds[0] % 2 != 1:
        raise ValueError("exact integer values and the known odd parity at6 required")
    endpoint = 2 * len(bounds) + 4
    classified = _odd_floor(endpoint // 2)
    return endpoint, classified, [m for m in range(3, classified + 1, 2)
                                  if bounds[m - 3] % 2]


def _factor_gains(bounds: list[int], first: int, last: int, z: int,
                  classified: int, primes: list[int], factors: list[int]) -> tuple:
    """Conditional refinement: inputs must also be LOWER bounds for G.

    For q|N, T=N/q>=2q, C_q*C_q=G(T)-2*e_q, where e_q counts prime
    p<q with T-p prime. Both d_q=1_prime(T/2) and J(T)-2*e_q have the
    true same-factor count's parity, and each is <=that count. Therefore
    K_q=max(d_q,J(T)-2*e_q) is a valid bound with the exact parity.
    Adding K_q-d_q to the diagonal-only bound preserves parity and can
    only improve it. This uses earlier bound VALUES, never assumes J=G.

    Range: T-p<=T-3<=(N-3)/q<=Hmax/(z+1); these odd flags are known.
    Thus T<=classified+3<=prefix_end, including the smallest prefix6.
    Each gain <=G(T)<=T/2. At most two distinct q>z divide even N:
    three would have odd product >(N-3)>=N/2 yet dividing N. Hence
    total gain <=N/(z+1)=O(N**(2/3)), and it is zero on powers of two.
    No exception-elimination theorem is proved.
    """
    flags = bytearray(classified + 1)
    for p in primes:
        flags[p] = 1
    gains = [0] * ((last - first) // 2 + 1)
    used = largest = 0
    endpoint = 2 * len(bounds) + 4
    for q in factors:
        small = [p for p in primes if p < q]
        start = max(2 * q * q, ((first + 2 * q - 1) // (2 * q)) * (2 * q))
        for target in range(start, last + 1, 2 * q):
            t = target // q
            if t > endpoint or t - 3 > classified:
                raise RuntimeError("earlier bound or prime flag range is insufficient")
            excluded = sum(flags[t - p] for p in small)
            diagonal = flags[t // 2]
            same_lower = max(diagonal, bounds[(t - 6) // 2] - 2 * excluded)
            gain = same_lower - diagonal
            if gain % 2:
                raise RuntimeError("earlier bound parity contradicts recovered prime flags")
            gains[(target - first) // 2] += gain
            used += 1
            largest = max(largest, t)
    if any(gain > (first + 2 * i) // (z + 1) for i, gain in enumerate(gains)):
        raise RuntimeError("same-factor gain exceeds the proved arithmetic ceiling")
    return gains, used, largest


def parity_batch(bounds: list[int], first: int, count: int, *,
                 same_factor: bool = False) -> dict:
    """Build a later finite band, conditional on truthful earlier parities.

    same_factor additionally requires every supplied value to be <=G at
    its label. Range/type checks cannot establish this mathematical premise.
    The canonical generator below establishes both premises by induction.
    """
    if type(same_factor) is not bool:
        raise ValueError("same_factor must be an exact boolean")
    started = perf_counter()
    last, high, z = _block_shape(first, count)
    endpoint, classified, small_primes = recover_parity_primes(bounds)
    cofactor_limit = _odd_floor(high // (z + 1))
    if first <= endpoint:
        raise ValueError("all batch targets must follow the supplied prefix")
    if z > classified or cofactor_limit > classified:
        raise ValueError("earlier parity prefix is too short for this cubic band")
    recovery_seconds = perf_counter() - started

    built_at = perf_counter()
    survivors, composites, residual_primes = _build_survivors(small_primes, z, high)
    construction_seconds = perf_counter() - built_at
    multiplied_at = perf_counter()
    slots = len(survivors)
    digit_bytes = max(1, (slots.bit_length() + 7) // 8)  # base>slots
    a = _pack_binary(survivors, digit_bytes)
    c = _pack_binary(composites, digit_bytes)
    ms = _extract(a * a, first, count, digit_bytes)
    acs = _extract(a * c, first, count, digit_bytes)
    convolution_seconds = perf_counter() - multiplied_at
    corrected_at = perf_counter()
    gains, correction_terms, largest_input = ([0] * count, 0, 0)
    if same_factor:
        gains, correction_terms, largest_input = _factor_gains(
            bounds, first, last, z, classified, small_primes, residual_primes)
    correction_seconds = perf_counter() - corrected_at
    rows = []
    for i, (m, ac) in enumerate(zip(ms, acs)):
        target = first + 2 * i
        center = target // 2
        diagonal = composites[(center - 3) // 2] if center % 2 else 0
        lower = m - 2 * ac + diagonal  # signed arithmetic after decoding
        row = {"target_even": target, "M": m, "AC": ac,
               "composite_diagonal": diagonal, "L": lower + gains[i]}
        if same_factor:
            row.update({"base_L": lower, "same_factor_gain": gains[i]})
        rows.append(row)
    nonpositive = [row["target_even"] for row in rows if row["L"] <= 0]
    unresolved = [row["target_even"] for row in rows
                  if row["L"] <= 0 and row["L"] % 2 == 0]
    return {
        "first_even": first, "last_even": last, "target_count": count,
        "input_prefix_end": endpoint, "classified_last_odd": classified,
        "cubic_cutoff": z, "required_cofactor_limit": cofactor_limit,
        "minimum_row": min(rows, key=lambda row: row["L"]),
        "nonpositive_targets": nonpositive, "unresolved_targets": unresolved,
        "certified_target_count": count - len(unresolved), "rows": rows,
        "same_factor_refinement": same_factor,
        "same_factor_terms": correction_terms,
        "largest_correction_input": largest_input,
        "seconds": {"parity_recovery": recovery_seconds,
                    "construction": construction_seconds,
                    "convolution": convolution_seconds,
                    "same_factor_correction": correction_seconds,
                    "pipeline_total": perf_counter() - started},
        "input_meaning": ("conditional on parity-correct LOWER bounds at all earlier labels"
                          if same_factor else
                          "conditional on correct G parity at every supplied earlier label"),
        "scope": "finite parity-preserving lower bounds; universal positivity unproved",
    }


def generate_prefix(endpoint: int, *, same_factor: bool = False) -> dict:
    """Generate every L(6),L(8),...,L(endpoint), starting only with L(6)=1.

    End each stage at the cube-root band boundary or the current input limit.
    Cofactor odd-floor<=B is equivalent to H<(B+2)*(z+1), with B odd.
    This exact integer condition permits the first stage6 ->10.
    With same_factor=True, each stage also uses earlier lower-bound values;
    _factor_gains proves their lower-bound and parity premises inductively.
    """
    if type(same_factor) is not bool:
        raise ValueError("same_factor must be an exact boolean")
    if type(endpoint) is not int or endpoint < 6 or endpoint % 2:
        raise ValueError("endpoint must be an even exact integer at least6")
    started = perf_counter()
    bounds = [1]
    stages = []
    previous = 6
    while previous < endpoint:
        first = previous + 2
        z = exact_floor_cuberoot(first - 3)
        classified = _odd_floor(previous // 2)
        high = _odd_floor(min((z + 1) ** 3 - 1, (classified + 2) * (z + 1) - 1))
        last = min(endpoint, high + 3)
        if last < first:
            raise RuntimeError("well-founded recursion failed to advance")
        batch = parity_batch(bounds, first, (last - first) // 2 + 1,
                             same_factor=same_factor)
        bounds.extend(row["L"] for row in batch["rows"])
        stages.append({"previous_end": previous, "target_end": last,
                       "cubic_cutoff": z, "classified_last_odd": classified,
                       "required_cofactor_limit": batch["required_cofactor_limit"]})
        previous = last
    return {
        "canonical_base": {"target_even": 6, "L": 1}, "final_end": endpoint,
        "same_factor_refinement": same_factor,
        "lower_bounds": bounds, "stages": stages,
        "minimum_lower_bound": min(bounds),
        "nonpositive_targets": [6 + 2 * i for i, value in enumerate(bounds) if value <= 0],
        "unresolved_targets": [6 + 2 * i for i, value in enumerate(bounds)
                               if value <= 0 and value % 2 == 0],
        "lower_bounds_sha256": hashlib.sha256(
            ",".join(map(str, bounds)).encode("ascii")).hexdigest(),
        "seconds": perf_counter() - started,
        "input_meaning": ("canonical induction from L(6)=1 using earlier lower bounds and parity"
                          if same_factor else
                          "canonical induction from L(6)=1 using only earlier output parity"),
    }


def canonical_experiment(*, same_factor: bool = False) -> dict:
    """Frozen same-range experiment; input generation is part of total cost."""
    started = perf_counter()
    prefix = generate_prefix(20000, same_factor=same_factor)
    result = parity_batch(prefix["lower_bounds"], 1002000, 1000,
                          same_factor=same_factor)
    result["method"] = "canonical parity-preserving lower-bound bootstrap"
    result["input_meaning"] = prefix["input_meaning"]
    result["prefix_summary"] = {key: value for key, value in prefix.items()
                                if key not in ("lower_bounds", "input_meaning")}
    result["seconds"]["input_generation"] = prefix["seconds"]
    result["seconds"]["complete_total"] = perf_counter() - started
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-controls", action="store_true")
    parser.add_argument("--same-factor", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = canonical_experiment(same_factor=args.same_factor)
    rows = {row["target_even"]: row for row in result.pop("rows")}
    # Read only the already-verified same-block baseline, outside production timing.
    baseline = json.loads(Path(__file__).with_name("evidence").joinpath(
        "cubic-batch-prefix.json").read_text(encoding="utf-8"))
    if (baseline["first_even"], baseline["last_even"]) != (
            result["first_even"], result["last_even"]):
        raise RuntimeError("baseline target range differs")
    previous_failures = set(baseline["nonpositive_targets"])
    result["comparison"] = {
        "baseline": "evidence/cubic-batch-prefix.json",
        "baseline_complete_seconds": baseline["seconds"]["complete_total"],
        "baseline_minimum_raw": baseline["minimum_row"]["raw"],
        "lost_certifications": [n for n in result["unresolved_targets"]
                                if n not in previous_failures],
        "scope": "same fixed block; single-run timings do not establish a speedup",
    }
    if args.same_factor:
        result["refinement_summary"] = {
            "improved_targets": sum(row["same_factor_gain"] > 0 for row in rows.values()),
            "maximum_gain_row": max(rows.values(), key=lambda row: row["same_factor_gain"]),
            "total_gain": sum(row["same_factor_gain"] for row in rows.values()),
            "new_certifications": [n for n, row in rows.items()
                                   if row["base_L"] <= 0 and row["base_L"] % 2 == 0
                                   and (row["L"] > 0 or row["L"] % 2)],
        }
    if args.check_controls:
        from cubic_sieve import cubic_sieve_count
        from redistribution import sieve
        validation_started = perf_counter()
        high = result["last_even"] - 3
        flags = sieve(high)  # independent full-range flags, VALIDATION ONLY
        z = result["cubic_cutoff"]
        rough = bytearray(b"\1") * (high + 1)
        for p in range(3, z + 1, 2):
            if flags[p]:
                rough[p * p::2 * p] = b"\0" * len(range(p * p, high + 1, 2 * p))
        result["independent_controls"] = []
        control_targets = {result["first_even"], result["minimum_row"]["target_even"],
                           result["last_even"]}
        if args.same_factor:
            control_targets.add(result["refinement_summary"]["maximum_gain_row"]["target_even"])
        for target in sorted(control_targets):
            m = ac = 0
            for a in range(3, target - 2, 2):
                if rough[a] and rough[target - a]:
                    m += 1
                    ac += not flags[a]
            center = target // 2
            diagonal = int(bool(center % 2 and rough[center] and not flags[center]))
            row = rows[target]
            reference = cubic_sieve_count(target)
            if (row["M"], row["AC"], row["composite_diagonal"], row.get("base_L", row["L"])) != (
                    m, ac, diagonal, m - 2 * ac + diagonal):
                raise RuntimeError(f"direct-array disagreement at {target}")
            if not row["L"] <= reference["union_bound_raw"] <= reference["result"]:
                raise RuntimeError(f"lower-bound disagreement at {target}")
            if (reference["result"] - row["L"]) % 2:
                raise RuntimeError(f"parity disagreement at {target}")
            result["independent_controls"].append({**row, "reference_G": reference["result"],
                "reference_raw": reference["union_bound_raw"],
                "bound_loss": reference["union_bound_raw"] - row["L"]})
        result["seconds"]["independent_validation"] = perf_counter() - validation_started
    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
