"""A resonant countermodel to a generic transfer into semiprime AP variance.

Owner: Kevin's Goldbach research. Purpose: determine whether the available
Type I, second-moment and Fourier controls alone can imply the newly isolated
variance bound. Preserve the exact missing prime-structure requirement.
This is an ARTIFICIAL comparison-error sequence, not Lambda-Gamma_S, a
prime-pair counterexample, or an estimate of the actual Goldbach remainder.
Independent Sol theory/actual-file review: PASS for the countermodel and
weighted variance reassessment. Review corrected an unqualified ordering
claim: the two sufficient variance conditions are not globally ordered.

QUESTION AND DISPOSITION.
Can completion plus the known generic error controls license the transfer of
the retained smooth Kloosterman estimates into the actual semiprime-modulus
variance? Those controls alone cannot do so. The sequence below has absolute
Type I saving by a fixed power, bounded pointwise size, a small second moment,
and Fourier supremum O(Y^0.50018 logY), but violates the proposed variance
target and produces a positive signed family sum of order at leastY logY.
It shows which information a transfer must additionally use; it does not
rule out the actual-prime dispersion route or the earlier good-modulus bound.

SETUP AND EXACT PRIMITIVE-DENOMINATOR CONSTRUCTION.
1. Reuse the prime rectangle of factored_prime_ap_transfer.py:
    a0=3/10, a1=a0+1/50000, b0=1/5+1/10000, b1=b0+1/50000,
    P={p prime:Y^a0<p<=Y^a1}, D={d prime:Y^b0<d<=Y^b1}.
   Put s0=a0+b0=.5001, s1=a1+b1=.50014, and Rmin=Y^s0,Rmax=Y^s1.
   The sets are disjoint. Let Y tend to infinity through positive multiples
   of4, m0=3Y/2 even, I=(Y/2,Y]. Set
    C_P=sum_(p in P)1/p, C_D=sum_(d in D)1/d,
    f(N)=sum_(p,d)c_(pd)(N)/(pd), E_*(q)=1_I(q) f(m0-q).
   For s(N),t(N) the counts of distinct P- and D-prime divisors, exactly
    f(N)=(s(N)-C_P)(t(N)-C_D).                            (1)
   This follows from c_p(N)=p*1_(p|N)-1 and coprime multiplicativity.
   Thus the lower proper-divisor contributions are canceled, leaving only
   primitive additive frequencies with FULL denominator pd. Omitting any
   of these subtractions changes the Type I conclusion.
2. PNT/Abel, already checked in the preceding module, gives
    C_P->log(a1/a0), C_D->log(b1/b0),
   both strictly below1/1000. Hence C_P,C_D<=1/1000 eventually. For
   q in I, N=m0-q is in[Y/2,Y). The exact product constraints give
   s<=3,t<=4,st<=3, as previously proved. Consequently |E_*|<=4 and
    sum_q |E_*(q)|^2<=16Y.                               (2)
   At every such N divisible by any family modulus r=pd, (1) instead gives
    f(N)>=(1-C_P)(1-C_D)>1/2.                            (3)
   These are pointwise assertions about this defined sequence, not primes.

ABSOLUTE TYPE I AND STRONG FOURIER SMALLNESS BOTH HOLD.
3. Fix gamma=49/100. More generally the argument works for fixed
   5/12<gamma<1-s1; it is not a claim for every gamma<1/2 with this SAME
   rectangle. For h<=Y^gamma, any integer shift b and integer interval J,
   the I-support intersects the j-sum in one interval. For each r=pd>h,
   the complete progression mean of c_r(m0-b+hj)/r is ZERO: a primitive
   frequency a/r resonates only when r divides h.
   More explicitly the component is
    1_(pd|N) - (1/d)1_(p|N) - (1/p)1_(d|N) + 1/(pd).
   Count the three indicators along the progression. After their zero means
   cancel, the endpoint discrepancy is at most1+1/p+1/d<2, regardless of
   interval length, shift, or common factors of h with p or d. Therefore
    sum_(h<=Y^gamma) max_J |sum_(j in J)E_*(b-hj)|
      <=2 Y^gamma #P #D <<Y^(gamma+s1)/(logY)^2.          (4)
   At gamma49/100 the exponent is49507/50000=.99014<1. This is smaller
   than Y/log(Y)^A for every fixedA, uniformly in b. It includes the
   interval restrictions in the saved TI input, not just complete periods.
4. Write Ehat_*(theta)=sum_q E_*(q)e(theta q). Its exact expansion has
   frequencies a/r, (a,r)=1, r in the family, coefficient magnitude1/r,
   a harmless phase e(a m0/r), and the SAME interval Dirichlet kernel.
   All reduced fractions are distinct and cyclically Rmax^(-2)-separated.
   For any such separated set T, sorting by distance to theta and summing
   the harmonic tail gives the elementary estimate
    sum_(alpha in T)min(Y,1/||theta-alpha||)
       <<(Y+Rmax^2)log(2Y).
   Values at zero distance are interpreted asY. At mostO(1+Rmax^2/Y)
   points occupy a distance1/Y neighborhood; the remaining annuli give
   the displayed logarithm. Since1/r<=1/Rmin, this proves
    ||Ehat_*||_infinity <<Y^(2s1-s0)logY
                         =Y^(25009/50000)logY.           (5)
   This is actual Fourier smallness of E_*. It is much stronger than the
   saved exponent1-1/4096 for the MODEL kernel, but does NOT identify E_*
   with that model's fixed smooth/short-period input. A theorem requiring
   those inputs cannot be applied merely by citing (4)-(5).

THE VARIANCE AND SIGNED-FAMILY TARGETS FAIL FOR THIS SEQUENCE.
5. Choose any fixed nonnegative smooth F compactly supported in(.5,1)^2,
   with F>=f0>0 on[.7,.8]^2, as allowed in the preceding proof. Define
    B_r^* = sum_j F(rj/Y,(m0-rj)/Y)E_*(m0-rj),
    H_* = sum_(r in family)|B_r^*|^2.
   Every summand is nonnegative by(3). The subinterval .7Y<=rj<=.8Y
   has at leastY/(20r) integers eventually, uniformly in r<=Rmax=o(Y).
   Thus B_r^*>=f0Y/(40r), and
    H_* >=(f0^2/1600)Y^2 sum_(p,d)1/(pd)^2.              (6)
   Partial summation of PNT at the LOWER endpoints gives
    sum_(p in P)1/p^2 ~Y^(-a0)/(a0 logY),
    sum_(d in D)1/d^2 ~Y^(-b0)/(b0 logY).
   Upper endpoint tails are power-smaller. Consequently
    H_* >>_(F) Y^(2-s0)/(logY)^2.
   Its ratio to the proposed variance scaleY^(2-s1) tends to infinity:
    Y^(s1-s0)/(logY)^2 -> infinity.                       (7)
   The diagonal remains O_F(Y) by(2) and the multiplicity-three bound.
   Hence even a negligible diagonal, (4), (5), and the L2 bound together
   do not license the requisite real off-diagonal upper bound.
6. This is not merely an overstrong Cauchy target failing. For the ACTUAL
   fixed-degree polynomial family coefficients A_r>0 from the preceding
   module (gamma49/100, nu49/200, fixedk>=9), define its sum against E_*.
   By(3) and the same subinterval count,
    T_family(E_*)=sum_r A_r B_r^* >=(f0Y/40)sum_r A_r/r.
   Uniformly phi(r)/r->1 on the family, while the preceding proved
   sum A_r/phi(r)~c_(nu,k)logY with c>0. Therefore
    T_family(E_*) >>_(F,k) YlogY.                         (8)
   The coefficient mass alone had not bounded the actual E correlation;
   (8) concerns only the explicitly constructed E_*, on whose rows we have
   now proved a positive pointwise value. No prime indicator is fabricated.

A NATURALLY WEIGHTED VARIANCE TARGET FOR THE ACTUAL PRIMES.
7. The previous unweighted target H=o(Y^2/Rmax) remains sufficient. It is
   not necessary and couples a coefficient norm concentrated near Rmax to
   a variance that can be concentrated near Rmin. Avoid requiring that
   extra power of precision in the next test. For the ACTUAL E, define
    w_r=A_r/r>0, M=sum_r w_r~c_(nu,k)L,
    e_r=(r/Y)B_r(m), K_Y(m)=sum_r w_r |e_r|^2.
   EXACTLY T_family/Y=sum_r w_r e_r, so weighted Cauchy gives
    |T_family/Y|^2<=M K_Y(m).
   The sufficient weighted variance target is therefore
    K_Y(m)=o(1/L),                                       (9)
   or, equivalently, mean square o(1/L^2) under the probability weights
   w_r/M. This does not assert actual relative equidistribution in every
   individual progression. It remains sufficient rather than necessary.
8. Its ACTUAL diagonal is already harmless. Since A_r<=L, r<=Rmax,
   at most3 family moduli divide any n in the physical interval, and the
   saved actual second moment is O(YL),
    K_diag=Y^(-2)sum_r A_r r sum_j |F E|^2
            <<_F (Rmax/Y)L^2=o(1/L).                     (10)
   What remains is an upper bound for
    2 Re Y^(-2)sum_r A_r r sum_(j1<j2)b_(r,j1)conj(b_(r,j2)),
   with b_(r,j)=F(rj/Y,(m-rj)/Y)E(m-rj). The common prime factors and all
   physical weights stay in the expression. Neither norm-only Cauchy nor
   the earlier MODEL completion supplies this upper bound.
   Our countermodel also fails this weighted sufficient target: by(3),
    e_r^*>=f0/40, K_* >=(f0^2/1600)M >>_(F,k)L.
   Hence the missing prime-specific input is not an artifact of the old
   unweighted normalization. Use(9) for the next intact-variance attempt;
   preserve the earlier estimate as a valid alternative sufficient condition.
   These two sufficient conditions are not globally ordered: the weighting
   removes the endpoint power mismatch near Rmin, but can demand finer
   logarithmic precision near Rmax. Neither is proved for the actual E.

WHAT THIS CHANGES.
The useful model Kloosterman estimates, polynomial identities, actual good-
modulus transfer, and actual diagonal remain valid. This stronger test rules
out a GENERIC inference using only the displayed norms and Type I estimates.
The construction does not satisfy the defining equality E=Lambda-Gamma_S,
and no CROSS, nonnegative prime representation or prime support is claimed.
Completion/dispersion can still work if it retains an additional arithmetic
property of the actual primes which excludes this full-denominator resonance.
Next question: can the COMPLETE signed cutoff identity cancel this resonance
between divisor sectors, without requiring each sector to be small? Test
the actual-first-prime pairing against this diagnostic E_* and its cutoff
compensation, then isolate what still fails for the true E. A successful
calculation for E_* would not be a true-prime correlation estimate. Preserve
the polynomial identity; do not rerun another generic norm improvement.
No universal coverage, actual signed prime estimate, or numerical onset.

All analytic source input here is the already checked ordinary PNT in Tao
2014 Notes2 Cor39/Ex40, referenced in factored_prime_ap_transfer.py. The
remaining construction, finite progression counts and spacing proof are
derived above; no new external theorem or prior-art claim is imported.
"""
from fractions import Fraction as F

from factored_prime_ap_transfer import two_prime_gap_geometry
from major_arc_kernel import _factorization, ramanujan
from unexceptional_vaughan_gate import _positive


def _prime_sets(left, right):
    left, right = tuple(left), tuple(right)
    if not left or not right or len(set(left)) != len(left) or len(set(right)) != len(right):
        raise ValueError('two nonempty sets of distinct primes required')
    if set(left) & set(right):
        raise ValueError('prime sets must be disjoint')
    for p in left+right:
        if type(p) is not int or p < 2 or _factorization(p) != ((p, 1),):
            raise ValueError('every entry must be a prime integer')
    return left, right


def resonant_value_pair(n, left, right):
    """Direct Ramanujan sum and independent prime-divisor count factorization."""
    if type(n) is not int:
        raise ValueError('integer argument required')
    left, right = _prime_sets(left, right)
    cp, cd = sum((F(1, p) for p in left), F(0)), sum((F(1, d) for d in right), F(0))
    direct = sum((F(ramanujan(p*d, n), p*d) for p in left for d in right), F(0))
    factored = (sum(n % p == 0 for p in left)-cp)*(sum(n % d == 0 for d in right)-cd)
    return direct, factored


def primitive_progression_pair(p, d, shift, step, first, last):
    """Finite exact component sum, complete mean and paid endpoint bound."""
    _prime_sets((p,), (d,))
    _positive(step, 'step')
    if any(type(x) is not int for x in (shift, first, last)) or first > last:
        raise ValueError('integer shift and nonempty inclusive interval required')
    r = p*d
    total = sum((F(ramanujan(r, shift+step*j), r) for j in range(first, last+1)), F(0))
    mean = F(ramanujan(r, shift), r) if step % r == 0 else F(0)
    endpoint = 1+F(1, p)+F(1, d)
    return total, (last-first+1)*mean, endpoint


def resonant_exponents(gamma=F(49, 100)):
    """TI/Fourier exponents and positive violation gap for this fixed family."""
    if type(gamma) not in (int, F):
        raise ValueError('exact gamma required')
    (a0, a1, b0, b1), _ = two_prime_gap_geometry()
    s0, s1 = a0+b0, a1+b1
    if not F(5, 12) < gamma < 1-s1:
        raise ValueError('this family needs gamma<1-s1 for the TI proof')
    return gamma+s1, 2*s1-s0, 2-s0, 2-s1, s1-s0


def resonant_rows(y, left, right):
    """Small finite rows on both physical intervals, with F replaced by1.

    These fixtures test exact support and coherence only. Their chosen prime
    sets need not satisfy the asymptotic exponent rectangle or PNT bounds.
    """
    _positive(y, 'y')
    if y % 4:
        raise ValueError('Y must be a multiple of4 so m0=3Y/2 is even')
    left, right = _prime_sets(left, right)
    return {p*d: tuple(resonant_value_pair(p*d*j, left, right)[0]
                       for j in range(y//(2*p*d)+1, (y-1)//(p*d)+1))
            for p in left for d in right}


def weighted_progression_energy(y, coefficients, rows):
    """Exact real T, density mass M, normalized K, and K diagonal.

    Coefficients are nonnegative rational samples of A_r, not prime logs.
    Rows contain rational samples of the physical F E values. No analytic
    estimate follows from computing this finite identity.
    """
    _positive(y, 'y')
    coefficients, rows = dict(coefficients), {r: tuple(row) for r, row in rows.items()}
    if not coefficients or coefficients.keys() != rows.keys():
        raise ValueError('the same nonempty modulus keys are required')
    total, mass, energy, diagonal = F(0), F(0), F(0), F(0)
    for r, coefficient in coefficients.items():
        _positive(r, 'modulus')
        if type(coefficient) not in (int, F) or coefficient < 0:
            raise ValueError('nonnegative rational coefficient required')
        if any(type(v) not in (int, F) for v in rows[r]):
            raise ValueError('rational row samples required')
        row_sum = sum(rows[r], F(0))
        total += coefficient*row_sum
        mass += F(coefficient, r)
        energy += F(coefficient*r, y*y)*row_sum**2
        diagonal += F(coefficient*r, y*y)*sum((v*v for v in rows[r]), F(0))
    if mass <= 0:
        raise ValueError('positive density mass required')
    return total, mass, energy, diagonal
