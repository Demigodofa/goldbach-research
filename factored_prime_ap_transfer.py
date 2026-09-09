"""An actual factored-modulus component beyond the square-root Type I range.

Owner: Kevin's Goldbach research. Purpose: test a stronger prime-distribution
input against the retained signed cutoff identity, and preserve its exact
usable range and support obstruction. Finite guards check algebra and exponent
conditions; they do not numerically test the analytic theorem or its onset.
Independent Sol theory/actual-file review: PASS. PNT normalization and the
nonreduced truncated model were explicitly checked; no material correction.

QUESTION AND RESULT.
Can a beyond-half AP theorem handle the actual p*d divisor expansion with a
large prime p, bounded Mobius/polynomial coefficients, and moving residue m?
Yes, on the explicitly factored subset below. The resulting signed component
is O_A(Y/log(Y)^A) for every fixed A, uniformly in the permitted coefficients
and central targets. The level reaches Y^(2501/5000)=Y^0.5002. This is NOT a
bound for all moduli of that size, for the entire Vaughan remainder, or for
an arbitrary physical tuple mask. No new prime-pair coverage follows.

PRIMARY INPUT AND EXACT FACTOR GEOMETRY.
1. Maynard, Primes in arithmetic progressions to large moduli III: Uniform
   residue classes, arXiv:2006.08250v1, Theorem1.2, printedp3:
   https://arxiv.org/pdf/2006.08250
   For 0<sigma<1/1000, write Qj=x^alpha_j, sum alpha_j=1/2+sigma.
   The restrictions are
    40sigma<alpha2<1/20-7sigma,
    1/10+12sigma-alpha2<alpha3<1/10-4sigma-3alpha2/5.
   The theorem bounds the absolute prime-count AP discrepancies, summed over
   qj<=Qj, with nested residue suprema, by O_A,sigma(x/log(x)^A).
   A common arbitrary residue m qualifies: choose b=m modulo q1*q2.
   It is not restricted to a fixed small integer. No well-factorability of
   the coefficients is needed for this absolute estimate.
2. Choose sigma=1/2000 and
    (alpha1,alpha2,alpha3)=(787/2000,1/40,41/500).
   The four strict inequality margins are (1/200,43/2000,1/1000,1/1000).
   Put eta=1/10000 and actual caps
    P=floor Y^(1967/5000), A0=floor Y^(249/10000),
    B0=floor Y^(819/10000).
   Each actual exponent is alpha_j-eta; their sum is2501/5000>1/2.
   For every x in[Y/2,Y], these caps lie below x^alpha_j eventually,
   with the SAME fixed sigma and source constants. This explicit slack
   avoids assuming uniformity in a moving source parameter sigma(x).
3. Retain gamma in(5/12,1/2), U=V=floor Y^(gamma/2), S=Y^delta,
   0<delta<=1/4800, E=1_(Y/2,Y]*(Lambda-Gamma_S), and fixed smooth F
   compactly supported in(1/2,1)^2, with central even m in[5Y/4,7Y/4].
   Let |lambda_d|<=1, support d<=V, lambda1=1. This includes all the
   previously retained polynomial cutoffs. Define good pairs(p,d) by
    U<p<=P prime, d<=V, d=h*a*b, p*h<=P, a<=A0, b<=B0.
   Assign each good pair ONE deterministic triple(p*h,a,b). Equivalently,
   r=p*d admits a factorization with the three stated caps: p>V>A0,B0
   forces p into the first factor. Each r has unique prime factor p>V.
   Thus (p,d)->r->chosen triple is injective, and coefficients
   log(p)*lambda_d are bounded by logY, without multiplicity. The h=1
   subfamily has d<=Y^0.1068<V; allowing h>1 keeps useful larger divisors.

THE ACTUAL TRANSFER.
4. Let zeta(p,d) be ANY complex coefficient bounded by1, depending on
   Y,m,p,d, but independent of the progression variable k. Define
    T_good=-sum_(good pairs(p,d)) log(p)lambda_d zeta(p,d)
             *sum_(k>=1) F(p*d*k/Y,(m-p*d*k)/Y) E(m-p*d*k).       (1)
   In particular zeta may restrict to p*d>sqrtY. This is an EXACT selected
   component of the existing prime-slot divisor expansion. The excluded
   c=1 compensation vanishes here since p<=P<Y/2 eventually. It does not
   vanish throughout the full expansion and has not been dropped there.
5. First restrict to (r,m)=1. For any endpoint x in[Y/2,Y], the source
   theorem and the injective canonical assignment give an absolute summed
   estimate for pi(x;r,m)-pi(x)/phi(r). All targets m qualify uniformly.
   Abel summation with the COMMON function
    w_m(t)=F((m-t)/Y,t/Y)
   and then log(t) charges O_F(logY) variation. The prime-slot weight
   charges another logY, absorbed by selecting a larger source log saving.
   We integrate the summed endpoint estimate; we do NOT claim a maximum
   over unrelated modulus-dependent endpoints. Strong PNT and
   sum_(r<=D)1/phi(r)<<log(2D) replace the pi main by integral w_m/phi(r).
   Strong PNT source: Tao2014 Notes2, Corollary39/Exercise40,
   https://terrytao.wordpress.com/2014/12/09/254a-notes-2-complex-analytic-multiplicative-number-theory/
   This is separate from the excluded Notes7 proposition.
6. Proper prime powers in the partner cost Y^(1/2+o(1)): for each ell^j
   in(Y/2,Y], j>=2, possible moduli divide the NONZERO integer m-ell^j
   when F is nonzero. Use its divisor bound, log(p)<=logY, and
   Lambda(ell^j)<=logY. In nonreduced progressions, a prime partner>Y/2
   would have to divide r<=Y^0.5002<Y/2, impossible eventually. The same
   prime-power bound therefore pays the nonreduced Lambda contribution.
7. The ELEMENTARY Gamma comparison from ramanujan_type_i.py step1 extends
   independently of BV to every r<=D=Y^0.5002. Its complete progression
   mean is sum_(q|r)mu(q)G(logq/logS)c_q(m)/phi(q); the full mean is
    r/phi(r)*1_((r,m)=1).
   Thus the comparison includes nonreduced residues with full mean zero.
   Summing the missing q>S means and incomplete periods costs
    O_G(Y logY S^(-1/2) exp(O(sqrt(logY))) + D S^4).
   Passing from progression length to the real integral adds at most
   O(D log(2D)); smooth Abel summation has bounded variation. The additional
   log(p) costs one logarithm. Both errors remain power-small: the period
   exponent is2501/5000+4delta<1. No prime theorem is being silently used
   beyond its proved factor geometry. Combining steps5-7 proves
    |T_good| <<_(A,F,delta,gamma) Y/log(Y)^A.                 (2)

BOUNDARIES AND A FAILED ALTERNATIVE IMPORT.
8. The modulus set is nonempty in its beyond-half part asymptotically:
   choose p,a,b prime in fixed-relative intervals below their caps. Their
   product has exponent0.5002, d=a*b<V, and polynomial lambda_d is nonzero.
   PNT proves existence for sufficiently large Y, not a numerical onset.
   The complement remains open, including prime slots larger than P and
   divisor weights without the required factor split. Formula(2) is a
   real partial estimate; it does not imply a relative saving for the full
   correlation by taking absolute values or summing uncovered ranges.
9. Maynard II, arXiv:2006.07088v1, Definitions1-2 and Theorem1.1, printedp2:
   https://arxiv.org/pdf/2006.07088
   requires triply well-factorable weights at level Q<=x^(3/5-epsilon),
   and its constant depends on the fixed residue a. It does not directly
   supply uniformity for a=m~Y. There is also an EXACT coefficient support
   obstruction: the balanced split Q1=Q2=Q3=Q^(1/3) forces any triply
   well-factorable coefficient at an integer with prime factor>Q^(1/3)
   to vanish. Here every nonzero selected coefficient contains
   p>floor Y^(gamma/2), hence p>Y^(gamma/2), gamma/2>5/24>1/5,
   whereas even the maximum permitted level has Q^(1/3)<Y^(1/5).
   Level padding cannot repair this. The obstruction applies to every
   nonzero coefficient in this prime-slot family, not to all sieve weights
   or to other uses of Maynard's method. The polynomial identity is retained.

FOLLOW-ON: THE WHOLE SOURCE FACTOR RANGE MISSES A WEIGHTED FAMILY.
Independent Sol follow-on theory/actual-file review: PASS for steps10-16;
the intact variance target and multiplicity-three diagonal were checked.
10. Every admissible parameter choice in THEOREM1.2 satisfies
     Q2<x^(1/20), Q3<x^(1/10), Q1<x^(2/5-11sigma)<x^(2/5).
    Indeed Q2*Q3>x^(1/10+12sigma), while their total product is
    x^(1/2+sigma). Thus any integer r with least prime factor>x^(1/10)
    and r>x^(2/5) is outside EVERY allowed triple factorization: its
    second and third factors would have to be1, leaving first factor r.
    This is independent of the caps chosen in steps2-3. It concerns
    Theorem1.2, not all of Maynard's results or all distribution methods.
11. Fix the positive exponent intervals
     a0=3/10, a1=a0+1/50000,
     b0=1/5+1/10000, b1=b0+1/50000.
    Let p,d be primes with Y^a0<p<=Y^a1, Y^b0<d<=Y^b1. Their moduli
    r=p*d lie between Y^0.5001 and Y^0.50014, inside the saved numerical
    levelY^0.5002 but outside EVERY source triple range for x in[Y/2,Y].
    The prime intervals are disjoint; d<V<p for every fixed
    nu=gamma/2 in(5/24,1/4), eventually. Distinct pairs give distinct r.
    Ordinary PNT establishes the asymptotic family; no onset is claimed.
12. For the retained fixed-degree cutoff lambda_d=mu(d)
    *(1-log(d)/log(V))_+^k, k>=9 FIXED, the actual expansion coefficient
     A_(p*d)=-log(p)*lambda_d=log(p)*(1-log(d)/log(V))^k
    is positive on this family. Put L=logY. Its natural density mass has
    the ACTUAL asymptotic
     M_Y=sum_(p,d) A_(p*d)/phi(p*d) = c_(nu,k)*L+o(L),
     c_(nu,k)=(a1-a0)*integral_(b0,b1) (1-b/nu)^k db/b > 0.       (3)
    This follows by separating the p and d sums. Strong PNT and Abel give
    sum_p log(p)/(p-1)=(a1-a0)L+o(L) and convergence of the weighted
    reciprocal-prime d sum to the displayed integral. Replacing denominators
    by p and d costs vanishing tails. log(V)/L->nu pays the floor; the
    weight converges uniformly on[b0,b1], away from its cutoff endpoint.
    The integrand is positive and decreasing, so explicit rational bounds
    on c are the interval length times its two endpoint values, multiplied
    by(a1-a0). The constant can be tiny; no optimized size is asserted.
13. Restricting(3) to (p*d,m)=1 leaves the SAME leading constant uniformly
    for m in[5Y/4,7Y/4]. Such an m has O(1) prime divisors in either
    fixed positive-exponent interval. The lost mass is
    O(L*(Y^(-a0)+Y^(-b0)))=o(1), using the same reciprocal-prime bounds.
    In particular a target cannot absorb this family into its nonreduced
    moduli. This is a density-weight assertion, not a prime-pair assertion.
14. There is also an actual MODEL consequence. Define the common integral
     I_F(t)=integral_R F(t-v,v) dv,
    and G_family=sum_(p,d) A_(p*d) sum_j F(pd*j/Y,(m-pd*j)/Y)
                                      *Gamma_S(m-pd*j).
    The elementary all-modulus comparison in step7, still at D=Y^0.5002,
    gives uniformly in central m
     G_family=Y I_F(m/Y) M_Y(m)+o(Y)
             =c_(nu,k) I_F(m/Y) YL+o(YL).                       (4)
    Its nonreduced truncated model contribution is paid, not set to zero.
    If F>=0 and F>=f0>0 on[.7,.8]^2, then for
    m/Y in[29/20,31/20], I_F(m/Y)>=f0/20. Thus this selected model
    component has positive YL scale. It is not a lower bound on E or on
    the full remainder; selecting only prime d destroys other divisor signs.
15. Exactly, the remaining selected correlation is
     T_family=P_family-G_family,
    where P_family replaces Gamma_S in(4) by the ACTUAL Lambda partner.
    Its proper-power part is O(Y^(.5+o(1))) by step6; the prime part stays
    open. Neither(3) nor(4) estimates this difference or proves the actual
    prime main term. A sufficient o(Y) bound here would require agreement
    to o(1/L) relative to the YL model scale, with F bounded below as above.
    Merely discarding this family by its coefficient size, or tuning the
    Theorem1.2 caps, cannot supply that bound. Full prime-pair coverage
    would additionally require the other remaining components.
16. To ask for actual cancellation without discarding the coupled primes,
    set R=Y^(a1+b1)=Y^(25007/50000) and
     B_r(m)=sum_j F(rj/Y,(m-rj)/Y)E(m-rj),
     H_Y(m)=sum_(r in the family)|B_r(m)|^2.
    Strong PNT at the upper endpoints gives the separate COEFFICIENT fact
     N_Y=sum_r A_r^2 ~ c2 R,
     c2=(a1/b1)*(1-b1/nu)^(2k)>0.
    Indeed sum_p(logp)^2~a1 L Y^a1, while the d sum of the squared
    polynomial weight is asymptotic to(1-b1/nu)^(2k)Y^b1/(b1 L).
    Lower endpoints are power-smaller. Exact Cauchy gives
     |T_family|^2<=N_Y H_Y(m).
    A SUFFICIENT, still unproved, fixed-target variance estimate is
     H_Y(m)=o(Y^2/R)=o(Y^(74993/50000)).                      (5)
    Its diagonal is already O_F(YL). To see this, an n in(Y/2,Y] has
    s p-prime divisors and t d-prime divisors satisfying a0*s+b0*t<1.
    The possible positive pairs are(1,1),(1,2),(1,3),(2,1), so at most3
    moduli r=p*d in this family divide n. Apply the ACTUAL bound
    sum|E|^2<<YL from optimized_cofactor_cutoff.py, with n=m-partner.
    This diagonal is o(Y^2/R). Writing b_(r,j)=F E at that tuple,
     H=diagonal+2 Re sum_r sum_(j1<j2) b_(r,j1) conjugate(b_(r,j2)),
    the remaining requirement is an upper bound for this real off-diagonal
    contribution; no absolute bound or independence is needed.
    Its partners q_i=m-rj_i obey q1-q2=r(j2-j1) and retain the common
    two-prime modulus. Equations(3)-(4) and the small diagonal do not prove
    (5). This preserves an intact correlation as the next concrete target.

The geometric exclusion is universal within the stated SOURCE theorem.
The positive coefficient mass is only for the stated FIXED-degree polynomial
family. Other cutoffs, growing degrees, identities, and distribution inputs
are not ruled out. The earlier cutoff-freedom and good-modulus estimates stay
available. A next pursuit must attack the actual centered prime sum or change
the arithmetic decomposition; another admissible-cap search repeats this gate.
"""
from fractions import Fraction as F

from major_arc_kernel import _factorization
from optimized_cofactor_cutoff import _weights
from unexceptional_vaughan_gate import _divisors, _positive


def source_exponent_margins(sigma, alpha2, alpha3):
    """Exact strict margins of Maynard III Theorem1.2; reject floats."""
    if any(type(x) not in (int, F) for x in (sigma, alpha2, alpha3)):
        raise ValueError('exact rational exponents required')
    sigma, alpha2, alpha3 = map(F, (sigma, alpha2, alpha3))
    alpha1 = F(1, 2)+sigma-alpha2-alpha3
    margins = (alpha2-40*sigma, F(1, 20)-7*sigma-alpha2,
               alpha3-F(1, 10)-12*sigma+alpha2,
               F(1, 10)-4*sigma-F(3, 5)*alpha2-alpha3)
    if not 0 < sigma < F(1, 1000) or min(alpha1, *margins) <= 0:
        raise ValueError('outside the strict source exponent domain')
    return (alpha1, alpha2, alpha3), margins


def transfer_geometry(gamma=F(49, 100), delta=F(1, 4800), trim=F(1, 10000)):
    """Return actual factor caps, modulus exponent, and paid power margins."""
    if any(type(x) not in (int, F) for x in (gamma, delta, trim)):
        raise ValueError('exact rational parameters required')
    gamma, delta, trim = map(F, (gamma, delta, trim))
    alphas, _ = source_exponent_margins(F(1, 2000), F(1, 40), F(41, 500))
    caps = tuple(a-trim for a in alphas)
    level = sum(caps, F(0))
    if not (F(5, 12) < gamma < F(1, 2) and 0 < delta <= F(1, 4800)
            and trim > 0 and min(caps) > 0 and level > F(1, 2)
            and caps[1]+caps[2] < gamma/2 < caps[0] < F(1, 2)
            and level+4*delta < 1):
        raise ValueError('transfer domain or genuine beyond-half gain fails')
    return caps, level, (delta/2, 1-level-4*delta, F(1, 2))


def canonical_factorization(n, first_cap, second_cap):
    """One split, or None; enumeration is for small exact fixtures only."""
    for value, name in ((n, 'n'), (first_cap, 'first cap'), (second_cap, 'second cap')):
        _positive(value, name)
    return next(((a, n//a) for a in _divisors(n)
                 if a <= first_cap and n//a <= second_cap), None)


def canonical_cofactor_split(p, d, large_cap, first_cap, second_cap):
    """A single (p*h,a,b) factorization of p*d, including h>1."""
    for value, name in ((p, 'p'), (d, 'd'), (large_cap, 'large cap'),
                        (first_cap, 'first cap'), (second_cap, 'second cap')):
        _positive(value, name)
    for h in _divisors(d):
        if p*h <= large_cap:
            pair = canonical_factorization(d//h, first_cap, second_cap)
            if pair is not None:
                return (p*h,)+pair
    return None


def selected_modulus_coefficients(prime_cap, first_cap, second_cap, weights):
    """r -> (p, coefficient of log p), with one split and unique p>V.

    This retains the negative sign in T_good. No progression-variable mask.
    Finite parameters need not satisfy any asymptotic source hypothesis.
    """
    for value, name in ((prime_cap, 'prime cap'), (first_cap, 'first cap'),
                        (second_cap, 'second cap')):
        _positive(value, name)
    weights = _weights(weights)
    cutoff = len(weights)-1
    out = {}
    for p in range(cutoff+1, prime_cap+1):
        if _factorization(p) != ((p, 1),):
            continue
        for d in range(1, cutoff+1):
            if weights[d] and canonical_cofactor_split(
                    p, d, prime_cap, first_cap, second_cap) is not None:
                out[p*d] = (p, -weights[d])
    return out


def selected_log_vector(n, prime_cap, first_cap, second_cap, weights):
    """Exact selected coefficient at n in a basis of formal prime logarithms."""
    _positive(n, 'n')
    out = {}
    for r, (p, coefficient) in selected_modulus_coefficients(
            prime_cap, first_cap, second_cap, weights).items():
        if n % r == 0:
            out[p] = out.get(p, F(0))+coefficient
    return tuple((p, c) for p, c in sorted(out.items()) if c)


def balanced_factorizations(n, level, order=3):
    """All balanced supported tuples: an empty set forces coefficient zero.

    Pure finite support certificate; nonempty tuples do not prove that an
    arbitrary sequence is well-factorable. No analytic theorem is tested.
    """
    _positive(n, 'n')
    _positive(level, 'level')
    _positive(order, 'order')
    if order > 8:
        raise ValueError('finite fixture order cap is8')
    def descend(remaining, slots):
        if slots == 1:
            return ((remaining,),) if remaining**order <= level else ()
        return tuple((d,)+tail for d in _divisors(remaining)
                     if d**order <= level
                     for tail in descend(remaining//d, slots-1))
    return descend(n, order)


def two_prime_gap_geometry(nu=F(49, 200)):
    """Exact fixed exponent rectangle and source/cutoff separation margins."""
    if type(nu) not in (int, F) or not F(5, 24) < nu < F(1, 4):
        raise ValueError('require exact nu in(5/24,1/4)')
    nu = F(nu)
    a0, a1 = F(3, 10), F(3, 10)+F(1, 50000)
    b0, b1 = F(1, 5)+F(1, 10000), F(1, 5)+F(1, 10000)+F(1, 50000)
    margins = (b0-F(1, 10), a0+b0-F(2, 5), a0+b0-F(1, 2),
               F(2501, 5000)-a1-b1, nu-b1, a0-nu)
    return (a0, a1, b0, b1), margins


def polynomial_gap_mass_bounds(nu=F(49, 200), degree=9):
    """Rational bounds for the LIMIT c in M_Y/logY -> c, not finite M_Y."""
    _positive(degree, 'degree')
    if degree < 9:
        raise ValueError('retained polynomial family has fixed degree>=9')
    (a0, a1, b0, b1), _ = two_prime_gap_geometry(nu)
    width = (a1-a0)*(b1-b0)
    return (width*(1-b1/nu)**degree/b1, width*(1-b0/nu)**degree/b0)


def small_factor_support_obstruction(n, large_cap, first_cap, second_cap):
    """Sufficient finite certificate of NO triple under the given caps.

    False means this certificate does not decide, not that a split exists.
    """
    for value, name in ((n, 'n'), (large_cap, 'large cap'),
                        (first_cap, 'first cap'), (second_cap, 'second cap')):
        _positive(value, name)
    return n > 1 and n > large_cap and _factorization(n)[0][0] > max(first_cap, second_cap)


def gap_variance_budget(nu=F(49, 200), degree=9):
    """Actual coefficient norm's limiting constant and OPEN variance exponent."""
    polynomial_gap_mass_bounds(nu, degree)  # shared fixed-family input gate
    (a0, a1, b0, b1), _ = two_prime_gap_geometry(nu)
    norm_constant = a1/b1*(1-b1/nu)**(2*degree)
    level = a1+b1
    return norm_constant, level, 2-level


def gap_prime_divisor_counts():
    """All positive counts allowed by the exact n<=Y product constraint."""
    (a0, _, b0, _), _ = two_prime_gap_geometry()
    return tuple((s, t) for s in range(1, 1//a0+1)
                 for t in range(1, 1//b0+1) if a0*s+b0*t < 1)
