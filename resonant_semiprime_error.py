"""A resonant countermodel to a generic transfer into semiprime AP variance.

Owner: Kevin's Goldbach research. Purpose: determine whether the available
Type I, second-moment and Fourier controls alone can imply the newly isolated
variance bound. Preserve the exact missing prime-structure requirement.
This is an ARTIFICIAL comparison-error sequence, not Lambda-Gamma_S, a
prime-pair counterexample, or an estimate of the actual Goldbach remainder.
Independent Sol theory/actual-file review: PASS for the countermodel and
weighted variance reassessment. Review corrected an unqualified ordering
claim: the two sufficient variance conditions are not globally ordered.
The subsequent complete-layer application and diagnostic cancellation in
sections8-11 also received independent Sol theory/actual-file PASS; ten
finite guards pass normally and under Python -O, with no new correction.

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
   unweighted normalization. Both are valid sufficient conditions for this
   ISOLATED rectangle; neither is necessary for the full remainder, as the
   complete-layer calculation below now demonstrates.
   These two sufficient conditions are not globally ordered: the weighting
   removes the endpoint power mismatch near Rmin, but can demand finer
   logarithmic precision near Rmax. Neither is proved for the actual E.

COMPLETE DIVISOR LAYERS ALREADY CANCEL FOR THE ACTUAL PRIME ERROR.
8. Write C_F(A,E)=sum_n A(n)F(n/Y,(m-n)/Y)E(m-n), retaining the saved
   unexceptional setup, gamma49/100 and U=V=floor(Y^(gamma/2)). For ANY
   subset J of {2,...,V}, put w_d=-lambda_d on J and zero elsewhere, with
   |lambda_d|<=1. The COMPLETE internal-Lambda layer is exactly
    L_J(n)=sum_(d in J,b>U,db|n)w_d Lambda(b)
          =sum_(d in J,d|n)w_d log(n/d)
           -sum_(d in J,b<=U,db|n)w_d Lambda(b).            (11)
   This is just Lambda*1=log. The first term is divisor-weighted Type I
   with d<=V and one Abel logarithm. Group the second by h=db<=UV;
   its coefficient is bounded by sum_(b|h)Lambda(b)=log h. Thus the
   EXISTING TI estimate gives, for the ACTUAL E=Lambda-Gamma_S,
    C_F(L_J,E)=O_A(Y/L^A) for every fixed A.               (12)
   The same conclusion holds for E_* by(4), paying at most a logarithm.
   All weights depend only on d (and possibly Y,m), with common smooth F;
   a prime-range or cofactor-dependent mask is not licensed inside(11).
   Removing internal proper powers costs at most Y U^(-1/2)L^3 in L1,
   by the saved positive tuple proof. After ||E||_infinity<<Y^(2delta+o(1))
   this is power-small at the saved delta cap. For E_*, use |E_*|<=4.
   Therefore(12) holds also for the complete PRIME layer L_J,p. No c=1
   compensation appears: d>=2 makes c=d*k>=2 for every p, including p~Y.
   This is an APPLICATION of optimized_cofactor_cutoff.py (02e1627),
   not a new prime-distribution theorem. Zeroing lambda on J preserves
   lambda1=1 and changes R_lambda,p by exactly L_J,p. Every nontrivial
   divisor layer can be removed this way, separately or all at once.
9. In particular take J=D from(1), with the retained fixed polynomial
   lambda_d=-(1-log d/log V)^k, k>=9. Let T_D,out be its prime-layer
   correlation restricted to ALL p>U outside P, with no further tuple mask.
   The two pieces partition L_D,p exactly, so for the ACTUAL E,
    T_D,out(E)=-T_family(E)+O_A(Y/L^A).                    (13)
   The same holds for E_*. Equation(13) does not estimate either piece
   individually, and does not follow from the newer factored-modulus input.
   It shows that solving the isolated rectangle variance is unnecessarily
   strong for removing this COMPLETE layer from the global remainder.

THE DIAGNOSTIC HAS A NONZERO FULL REMAINDER, DESPITE THAT CANCELLATION.
10. Keep F>=f0>0 on[.7,.8]^2 and write
     I_F=integral F(v,1.5-v)dv>0,
     C0=log(a1/a0)log(b1/b0)>0.
   Every Lambda-supported n in I has s(n)=t(n)=0 eventually: for a P-prime
   base its first three powers are below Y/2 since 3a1=.90006<1, whereas
   the fourth exceeds Y since 4a0=1.2>1. For a D-prime base use
   4b1=.80048<1<5b0=1.0005. Other prime bases cannot have P or D divisors.
   Thus f(n)=C_P C_D on ALL prime powers in the physical interval. Strong
   ordinary PNT, already sourced below, gives
    C_F(Lambda,E_*)=C0 Y I_F+O_A(Y/L^A).                  (14)
   Here C_P=log(a1/a0)+O_A(L^-A), likewise C_D, by partial summation.
   The full identity in optimized_cofactor_cutoff.py, its compensation
   controlled by(4) and one Abel logarithm, and the paid pruning give
    C_F(R_lambda,p,E_*)=C0 Y I_F+O_A(Y/L^A),              (15)
   uniformly for ALL normalized bounded cutoffs lambda supported<=V.
   Positivity and any ratio limit below require I_F>0; nonnegative F alone
   would not suffice. This is a pairing with an ARTIFICIAL partner.
11. There is also a precise size for the cancelling diagnostic pieces.
   On n=pd*j<=Y put s'=s(n)-1 and t'=t(n)-1. Since 2(a0+b0)>1,
   two P primes and two D primes cannot all divide n, so s't'=0. Exactly
    f(pd*j)=(1-C_P)(1-C_D)+(1-C_D)s'+(1-C_P)t'.
   The otherwise present fourth term s't' vanishes ONLY in this window.
   Smooth progression counting for each extra prime divisor of j gives
    B_pd^*=(Y/(pd)) I_F [1-C_P C_D-(1-C_D)/p-(1-C_P)/d]
           +O_F(1+#P+#D).                               (16)
   The fixed-degree polynomial coefficients satisfy
    M=sum A_pd/(pd)=c L+O_A(L^-A),
    c=(a1-a0) integral_(b0)^b1 (1-b/nu)^k db/b>0,
   again by strong PNT. Floor V changes this by a fixed power-small error.
   Multiplying the counting errors by A_pd<=L and summing costs
   O_F(L #P #D(1+#P+#D))<<Y^(s1+a1)L=Y^.80016 L.
   The reciprocal-p/d corrections cost O(Y^(1-b0)L); all are power-small.
   Consequently
    T_family(E_*)=(1-C0)c I_F Y L+O_A(Y/L^A),             (17)
    T_D,out(E_*)=-(1-C0)c I_F Y L+O_A(Y/L^A).            (18)
   The second follows from the ACTUAL complete-layer mechanism(11)-(12).
   If instead T_rest means the ENTIRE remainder minus this rectangle,
   its expansion is -(1-C0)c I_F Y L+C0 I_F Y+O_A(Y/L^A) by(15).
   Both corresponding ratios to T_family tend to -1. The full artificial
   remainder retains a positive Y main term; this does not refute the
   one-sided lower bound sought for actual prime-pair coverage.

WHAT THIS CHANGES.
The useful model Kloosterman estimates, polynomial identities, actual good-
modulus transfer, and actual diagonal remain valid. This stronger test rules
out a GENERIC inference using only the displayed norms and Type I estimates.
The construction does not satisfy the defining equality E=Lambda-Gamma_S,
and no CROSS, nonnegative prime representation or prime support is claimed.
Completion/dispersion can still work if it retains an additional arithmetic
property of the actual primes which excludes this full-denominator resonance.
The complete-layer question is now answered by(11)-(18), with the actual
scope separated from the diagnostic. Retire the isolated rectangle variance
as a REQUIRED next gate for the full problem; preserve it as an optional
sufficient condition and the factored-modulus theorem as a usable tool.
All lambda_d for d>1 can be zeroed, leaving lambda=delta_1. Its exact
prime remainder is -sum_(p|n,p>U,n!=p)log p. This is a simpler expression
of the SAME missing correlation, not its solution. Polynomial weights can
still help organize its arithmetic even though their full compensation is
TI-small. Next concrete question: can a one-sided bound for prime factors
of m-q, with q prime and m FIXED, improve this remainder's lower bound?
First derive the exact log-factor inequality required, allowing the legal
asymmetric choice lambda=delta_1, U=floor(Y^gamma), and test whether it is
merely the same correlation rewritten. Then check any proposed arithmetic
input for uniformity in m~Y and the needed sign/constant; an average over m
or a theorem only for shift1 is insufficient. No new coverage or full
actual estimate follows here; the asymmetric next test is not yet done.

All analytic source input here is the already checked ordinary PNT in Tao
2014 Notes2 Cor39/Ex40, referenced in factored_prime_ap_transfer.py. The
remaining construction, finite progression counts and spacing proof are
derived above; no new external theorem or prior-art claim is imported.
"""
from fractions import Fraction as F

from factored_prime_ap_transfer import two_prime_gap_geometry
from major_arc_kernel import _factorization, ramanujan
from optimized_cofactor_cutoff import _weights
from unexceptional_vaughan_gate import _add, _clean, _divisors, _positive, mangoldt_log_vector


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


def complete_divisor_layer_vectors(n, internal_cutoff, weights, indices):
    """Exact signed full-Lambda, prime-only, and log-minus-low layer vectors.

    Only nontrivial divisor indices are accepted: lambda1 cannot be removed
    while retaining cutoff normalization and the prime c=1 compensation.
    The prime-only vector includes ALL internal primes above the cutoff.
    """
    _positive(n, 'n')
    _positive(internal_cutoff, 'internal cutoff')
    weights = _weights(weights)
    indices = tuple(indices)
    if (any(type(d) is not int or not 2 <= d < len(weights) for d in indices)
            or len(set(indices)) != len(indices)):
        raise ValueError('distinct supported divisor indices d>=2 required')
    full, prime, compensation = {}, {}, {}
    for d in indices:
        if n % d:
            continue
        weight = -weights[d]
        _add(compensation, _factorization(n//d), weight)
        for b in _divisors(n//d):
            term = mangoldt_log_vector(b)
            if b <= internal_cutoff:
                _add(compensation, term, -weight)
            else:
                _add(full, term, weight)
                if _factorization(b) == ((b, 1),):
                    _add(prime, term, weight)
    return tuple(_clean(v) for v in (full, prime, compensation))


def conditional_resonance_terms(n, p, d, left, right):
    """Four exact terms, preserving extra-P times extra-D outside the window."""
    _positive(n, 'n')
    left, right = _prime_sets(left, right)
    if p not in left or d not in right or n % (p*d):
        raise ValueError('a selected modulus p*d must divide n')
    cp = sum((F(1, q) for q in left), F(0))
    cd = sum((F(1, q) for q in right), F(0))
    extra_p = sum(n % q == 0 for q in left)-1
    extra_d = sum(n % q == 0 for q in right)-1
    return ((1-cp)*(1-cd), (1-cd)*extra_p, (1-cp)*extra_d, F(extra_p*extra_d))


def resonance_power_gaps():
    """Strict exponents excluding selected prime bases from Lambda's window."""
    (a0, a1, b0, b1), _ = two_prime_gap_geometry()
    return (3*a1, 4*a0), (4*b1, 5*b0), 2*(a0+b0), (a0+b0)+(a1-a0)+(b1-b0)+a1
