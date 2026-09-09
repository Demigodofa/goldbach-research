"""Bridge the two roughness cutoffs and obtain conditional prime-pair mass.

Owner: Kevin's Goldbach research. Purpose: preserve the direct small-prime
affine adaptation, its precise conditional coverage and exact algebra guards.
No manuscript, claim of historical novelty, exceptional zero or numerical onset.
Sol independently reviewed the derivation, actual proof/code and nine exact
tests, including the all-residue corollary: PASS. Tests passed normally and
under Python -O (0.021s each); finite tests verify algebra, not the theorem.

THEOREM AND SCOPE.
Keep ALL hypotheses of rare_class_elimination.py and rare_divisor_calibration.py:
 chi primitive quadratic modulo D>24 with an ACTUAL zero
 beta0=1-1/(eta log D), Y=D^V, V>=log^3 eta, t=V/eta<=1/log Y,
 m even in[5Y/4,7Y/4], m in F_D, original fixed epsilon,delta,u,
 theta=delta/u<1/5, z_old=ceil(Y^theta), U=K log eta, z=Y^(1/U).
Let g(x/Y) be a fixed nonnegative uniformly smooth weight supported where
x,m-x are strictly between Y/2 and Y, and I_g=int g(x/Y)dx.
Write lambda=1*chi, W=chi*log=lambda*Lambda. Let S_z be the actual sum
 (1/2)sum_(P^-(x),P^-(m-x)>=z) g(x/Y)log(x)lambda(x)W(m-x),
with conductor-unit masks; P^-(1)=infinity. Thus P(z) uses primes STRICTLY
below z. Define S_theta with BOTH least prime factors STRICTLY >z_old.
The positive-sign-first actual prime-pair sum is P_g. Then
 0<=S_z-S_theta
   <<_theta S_2(m)Y t^2 U^8 log(2U)
             +Y^(7/9+theta+o(1))+S_2(m)Y eta^-20
   =o_theta(Yt).                                               (1)
Consequently the reviewed two different-cutoff results now COMPOSE:
 P_g=S_2(m)t I_g+o_theta(Yt).                                   (2)
For a smooth nonnegative g with I_g>>Y, this proves a prime pair for every
target satisfying these hypotheses once eta is sufficiently large.
The onset is ineffective and conditional on the actual zero AND stated
parameter range. No eligible zero or numerical target is certified here.
Formula(2) is confined to F_D; the corollary below supplies existence for
the other residue classes. No assertion covers all exceptional-zero regimes,
the unexceptional alternative, or every sufficiently large even integer.
This is conditional coverage of an eligible band, NOT Goldbach.

Sources: the direct Poisson proof in rare_affine_small_cofactor.py, using
Matomaki--Merikoski arXiv:2112.11412v2 Proposition2.3's PROOF, equations
(33)--(39), Lemmas2.2,2.4,3.2,3.3,3.8:
 https://arxiv.org/html/2112.11412v2 . Rechecked2026-09-09.
The stated source proposition and the earlier repo theorem do NOT cover
the new coefficients automatically; the changes are proved below.
Keep the corrected PLUS upper-beta remainder of source equation(22), the
corrected Henriot NEW Theorem5 exact-valuation conventions, and bulk Linnik
from Thorner--Zaman as deduced in relative_type_i.py. Do not revive Tao's
acknowledged Proposition23 gap or unchanged blocked source fetches.

I. A POSITIVE FACTORIZATION COVER OF THE DIFFERENCE.
1. Both variables in S_z are z-rough and <=Y, so each has Omega<=U and
   tau<=2^U. Remove squareful variables and variables sharing a prime.
   The former have at most O(Y/z) possible x. A shared prime divides m;
   there are O(U) such primes >=z and sum 1/r=O(U/z). Their total weighted
   contribution is at most Y/z*exp(O(U))*L^2, L=log Y. This is Y eta^-B
   for ANY fixed B: z=D^(V/U) dominates every fixed power of eta and L<=eta.
   Do not write Y^(1-1/U+o(1)) and assume an unspecified o(1) is smaller
   than 1/U. The explicit exp(O(U)) cost is what licenses this removal.
2. On squarefree units, lambda(x)>0 iff ALL primes dividing x have sign+.
   The suppressed residue condition then forces chi(m-x)=-1. On this
   negative side W(n)>0 iff n has exactly one negative-sign prime; if
   n=rM with that prime r, then W(n)=lambda(M)log r.
   Every surviving term in S_z-S_theta has a prime r in[z,z_old] dividing
   x or n=m-x. There are exactly THREE nonzero factorization types:
    (a) chi(r)=+1, x=rq: lambda(x)=2lambda(q);
    (b) chi(r)=+1, n=rq: W(n)=2W(q), because chi(q)=-1;
    (c) chi(r)=-1, n=rq: W(n)=lambda(q)log r.
   In(c), all primes of q have sign+. The identities use squarefreeness
   and (r,q)=1; the prior removal is necessary. A negative prime of x,
   or three negative primes of n, gives zero weight and needs no cover.
   If r|m it divides BOTH original variables, already removed.
3. All three reduced relations have the form
     p+r q=m, q comparable to Q=Y/r, p comparable to Y,
   with r prime in[z,z_old], (r,Dm)=1 and q,p z-rough. Dropping additional
   squarefree, coprimality and factor-order restrictions only enlarges
   the nonnegative majorants. Use a uniform nonnegative smooth majorant
   F(q/Q,p/Y), equal to1 on[1/2,1]^2, supported in[2/5,11/10]^2.
   The factor g is paid by its fixed sup norm. The three contributions
   are respectively bounded by fixed constants times
     L sum F lambda(q)W(p),
     L sum F W(q)lambda(p),
     L^2 sum F lambda(q)lambda(p).                         (3)
   The last majorization pays log(x)log(r)/2<=L^2/2. A union bound over
   ALL eligible r is legitimate even if a term has several witnesses.
   No extra maximum prime-factor count is needed on top of the summed r.

II. DIRECT AFFINE ESTIMATES FOR THESE SMALL PRIME COEFFICIENTS.
4. Reuse the smooth hyperbolas of rare_divisor_calibration.py. Write
   q=ab,p=cd; a<<sqrt(Q), c<<sqrt(Y), and r a b+c d=m. Always eliminate
   the variable of the LARGE-scale second form p, even when W is on q.
   After three beta-sieve indices e,d1,d2<=R=Y^(1/1000), the congruence is
      r e a d1 b = m (mod d2 c).
   Native (r,d2 c)=1 is retained in EVERY summand: r>=z implies r does
   not divide d2, and r|c would contradict (r,m)=1 on actual terms.
   With the same source coprimality removals, Poisson's modulus is D d2 c,
   NEVER D r d2 c. Its inverse phase gains inverse(r) mod d2 c.
   The physical integration variable has length Q; after q=Qs, p=Y(m/Y-s),
   both forms have uniform derivatives. W logarithms divided by L and
   the smooth dyadic partitions have uniform derivative bounds in either
   placement; log(Q) is comparable to L since theta<1/5.
5. The frequency cutoff is
     |k|<<Y^epsilon D d1 d2 A1 A2/Q.
   Apply source Lemma3.8 to the first small factor, keeping r as an
   invertible parameter. The integral's Q cancels the cutoff's 1/Q.
   Exactly as in rare_affine_small_cofactor.py, each r has nonzero error
     O(D^2 R^(7/2)Y^(3/4+o(1))+D R sqrt(Q)Y^o(1))
        =O(D^2Y^(7/9+o(1))).                             (4)
   O(L^2) boxes and the at most L^2 normalization costs are included.
   Since r<=ceil(Y^theta), Q>=Y^(1-theta)/2 and eventually Q>>Y^(4/5).
   Corrected Henriot's fixed coefficient-norm condition therefore holds
   for primitive forms q and m-rq, norm<=3Y, just as in the older proof.
6. The older theorem required P^-(M)>Y^theta. We do NOT apply that theorem
   to the new r. The only changed arithmetic facts needed by its proof are:
     r is a SINGLE prime, r>=z>D, (r,Dm)=1.
   Thus relaxed sieve-tail local factors at r are 1+O_a0(1/r), uniformly
   bounded, and the two-root sieve product below z is unchanged. Source
   beta-sieve tail summation, with fixed large a0,K, costs
     O(S_2(m)Q L^C[U^6/z+exp(-a0 U/3000)])
       =O(S_2(m)Q eta^-B)
   after every fixed logarithmic normalization. The fixed C depends only
   on the proof's divisor powers, not U or r. Any shared q,p prime is
   handled directly on the original rough support, costing Q eta^-B;
   no tiny-interval Henriot assertion is used to remove it.
   In the zero mode, removing the remaining (r,c)=1 condition has harmonic
   cost O(L^C/r), because sum_(r|c,c<=sqrt(2Y))1/c<<L/r. Hence its
   normalized weighted contribution is O(Q L^C/r). Summed over r>=z
   this is at most Y L^C sum_(r>=z)r^-2<<Y L^C/(z-1)=Y eta^-B.
   Keep (r,c)=1 until the zero-mode step; do not remove it in an inverse.
   Other source removals retain their explicit U^C/z or exp(O(U))/z costs.

III. ONE OR TWO CHARACTER CANCELLATIONS, DEPENDING ON THE REMOVED PRIME.
7. Let s=chi(r). For q=v,p=m-rv, multiplication by r permutes D-units.
   The four complete conductor sums are A,0,0,-sA, where A is the
   original suppressed unit-pair count. In detail Bfirst=sB=0,
   Bsecond=B=0, C_r=sC=-sA. The exact combined local coefficients for
   fixed unit small factors a,c are chi(a)chi(c)/(acD) times
     (A,-(1+s)A) for (log p,log c) in lambda(q)W(p),
     (A,-(1+s)A) for (log q,log a) in W(q)lambda(p),
     (1-s)A for lambda(q)lambda(p).                       (5)
   The Jacobian is 1/a, not 1/(ra), because the physical variable is q.
   Sum orientation mains and ALL boxes BEFORE taking absolute values.
8. For s=+1, the zero modes of the first two sums in(3), before their
   outside L, are exactly
     (A/D)V2_D int F A_z(q)B_z(p)dq,
     (A/D)V2_D int F B_z(q)A_z(p)dq,
   up to the paid removals. For s=-1 the lambda/lambda zero mode is
     (2A/D)V2_D int F A_z(q)A_z(p)dq.
   Here A_z,B_z and V2_D are EXACTLY those of rare_divisor_calibration.py.
   Lemma2.4 applies to BOTH transition scales sqrt(Q),sqrt(Y), all lying
   in[Y^(1/10),Y^2]. Consequently
      A_z=O(E/U), B_z=2C_z(1+O(E)), E=O(tU^4+eta^-B),
      C_z comparable to L/U, (A/D)V2_D<<S_2(m)U^2/L^2.
   Therefore each positive-r sum in(3) is at most
      O(S_2(m)Q E)+O(D^2Y^(7/9+o(1)))+paid tails,
   while each negative-r sum is at most
      O(S_2(m)Q E^2)+O(D^2Y^(7/9+o(1)))+paid tails.       (6)
   This bounds actual positive sums by the absolute zero mode plus error;
   it does not assume positive individual character-divisor summands.

IV. SUMMING SMALL PRIMES AND COMPOSING THE RESULTS.
9. Bulk Linnik modulo D applies uniformly to every dyadic interval
   [B,2B] meeting[z,z_old], since log(B)/log D>=V/U+O(1/log D).
   The sum of log(r) over its positive primes is at most
      O(B[(1-beta0)log B+eta^(-cV/U)+L^2/D]).
   Dividing by B log B, and summing O(L) intervals, gives
    H_plus=sum_(z<=r<=z_old,chi(r)=+)1/r
       <<_theta t+log(2U)[eta^(-cV/U)+L^2/D]
       =O_theta(t)+O(eta^-B).                            (7)
   No prime-power subtraction is required for this positive upper bound.
   The error uses V/U>>log^2 eta and Siegel's D>>_H eta^H for every
   fixed H. Ordinary Mertens gives H_all<<log(2U). Since Q=Y/r, the
   two positive placements together cost O(S_2 Y t^2 U^4)+tiny error,
   and the negative placement costs O(S_2 Y t^2 U^8 log(2U))+tiny error.
   The at most O(Y^theta) coefficients in(4) cost
      Y^(7/9+theta+o(1)); theta<1/5 leaves a fixed margin of at least1/45.
   All Q-scale tails sum with H_all and remain S_2 Y eta^-20.
   Finally S_2(m)<<log eta, t<=1/sqrt(eta log D), D=Y^o(1),
   t=Y^-o(1). Every term in(1) is therefore o(Yt). This proves(1).
10. The reviewed dynamic calibration gives S_z=S_2(m)t I_g+o(Yt).
    The reviewed fixed-theta first-variable replacement, explicitly paid
    FULL/B_good pruning and rare_class_elimination.py give
       S_theta=P_g+o(Yt).
    Those statements previously did not compose. Equation(1) supplies
    the missing comparison and proves(2), with their SAME original
    parameter choices, smoothing, conductor masks and prime weights.
    Taking a fixed smooth minorant with I_g>>Y proves conditional positivity.
    No reflection factor2 is needed for existence or the positive-first
    formula; a symmetric g makes the full ordered sum exactly twice P_g.

V. COVERAGE OF EVERY RESIDUE CLASS IN THE SAME CONDITIONAL BAND.
11. For ANY even m, A>0. The leading multiplier in MM Theorem1.4 is
      kappa_D(m)=1+C/A.
    This follows directly from its formula and Lemma2.5(16),(18). CRT
    gives an odd-prime factor chi_p(-1) times 1 if p|m, or -1/(p-2)
    otherwise, in C/A. The primitive 2-part contributes 0 or +/-1.
    Therefore either |C/A|=1, C/A=0, or some p>=5 not dividing m forces
    |C/A|<=1/3. In particular
      kappa_D(m) is in {0} union [2/3,2].
    When C=-A, EVERY allowed unit pair has opposite signs; the involution
    v -> m-v makes B=0. Thus kappa=0 is EXACTLY the family F_D already
    covered by(2), not a further unexamined class.
12. If kappa>0, apply MM Theorem1.4 with h=m and V_m=log(m)/log D.
    Its error divided by S_2(m)m tends to0: the exponential terms vanish,
    and V_m log^6(eta)/eta=O(t log^6 eta)=o(1). The fixed gap2/3 leaves a
    positive von Mangoldt pair sum. Proper prime powers contribute only
    O(sqrt(m) log^3 m)=o(m), so an actual prime pair remains. Here the
    pair is not asserted to lie in the smaller interval(Y/2,Y].
    For kappa=0 use(2) with I_g>>Y instead. Consequently EVERY even
    m in[5Y/4,7Y/4] has a prime representation whenever the SAME actual-zero
    and Y-parameter hypotheses hold and eta is sufficiently large.
    The nonzero-kappa case uses an existing theorem; no novelty is claimed.
    The zero assumption and its restricted scale window remain essential;
    an actual eligible band has NOT been found or numerically certified.

This closes the cutoff gap ONLY in the stated regime. Older limitations
retain their scope: the formal polynomial identity is still not a signed
prime estimate, and crude dynamic W pointwise bounds still fail. The new
arithmetic ingredient is the small-prime factorization cover, which preserves
long affine variables and adds a second rarity factor before absolutes.
Finite routines below verify residue algebra and exact support; they do not
certify the analytic source estimates, a zero, or an effective prime count.
"""
from fractions import Fraction as F
from math import gcd

from exceptional_character_model import character_values
from major_arc_kernel import _factorization
from character_partner_weight import negative_log_coefficients


def affine_log_coefficients(conductor, target, multiplier, small_a, small_c, *, two_sign=1):
    """Direct and predicted lambda/W, W/lambda, lambda/lambda densities."""
    if any(type(v) is not int or v < 1 for v in (target, multiplier, small_a, small_c)):
        raise ValueError('positive integer target, multiplier and divisors required')
    chi = character_values(conductor, two_sign=two_sign)
    D, r, a, c = conductor, multiplier, small_a, small_c
    if gcd(r*a, c) != 1 or gcd(r*a*c, D) != 1:
        raise ValueError('native affine inverse and conductor units required')
    A = sum(bool(chi[v]) and bool(chi[(target-v) % D]) for v in range(D))
    B = sum(chi[v]*bool(chi[(target-v) % D]) for v in range(D))
    C = sum(chi[v]*chi[(target-v) % D] for v in range(D))
    if A == 0 or B != 0 or C != -A:
        raise ValueError('target must lie in the suppressed unit-pair family')
    direct = [0]*5
    for b in range(c*D):
        if (target-r*a*b) % c:
            continue
        d = (target-r*a*b)//c
        base_q = chi[a % D]*bool(chi[b % D])
        extra_q = chi[b % D]
        base_p = chi[c % D]*bool(chi[d % D])
        extra_p = chi[d % D]
        direct[0] += (base_q+extra_q)*base_p
        direct[1] += (base_q+extra_q)*(extra_p-base_p)
        direct[2] += base_q*(base_p+extra_p)
        direct[3] += (extra_q-base_q)*(base_p+extra_p)
        direct[4] += (base_q+extra_q)*(base_p+extra_p)
    norm = F(1, a*c*D)
    signed = A*chi[a % D]*chi[c % D]*norm
    s = chi[r % D]
    predicted = tuple(signed*v for v in (1, -(1+s), 1, -(1+s), 1-s))
    return tuple(v*norm for v in direct), predicted


def cutoff_witnesses(first, partner, conductor, cutoff, old_cutoff):
    """Nonzero squarefree factorization cover; endpoints are [cutoff, old]."""
    if any(type(v) is not int or v < 2 for v in (first, partner, cutoff, old_cutoff)):
        raise ValueError('integer variables and cutoffs >=2 required')
    if old_cutoff < cutoff:
        raise ValueError('old cutoff must be at least the dynamic cutoff')
    if gcd(first, partner) != 1:
        raise ValueError('shared-factor terms must be removed first')
    chi = character_values(conductor)
    if chi[first % conductor]*chi[partner % conductor] != -1:
        raise ValueError('opposite conductor-unit signs required')
    fx, fn = _factorization(first), _factorization(partner)
    if any(e != 1 for _, e in fx+fn):
        raise ValueError('squareful terms must be removed first')
    if any(p < cutoff for p, _ in fx+fn):
        raise ValueError('both variables must be rough at the dynamic cutoff')
    if any(chi[p % conductor] == -1 for p, _ in fx):
        return ()  # lambda(first)=0
    if not negative_log_coefficients(partner, conductor):
        return ()
    witnesses = []
    for r, _ in fx:
        if r <= old_cutoff:
            witnesses.append(('positive_first', r, first//r))
    for r, _ in fn:
        if r <= old_cutoff:
            kind = 'positive_partner' if chi[r % conductor] == 1 else 'negative_partner'
            witnesses.append((kind, r, partner//r))
    return tuple(witnesses)


def nonzero_mode_budget(theta):
    """Rounded direct aggregate exponent and fixed margin; not an analytic test."""
    if type(theta) is not F or not 0 < theta < F(1, 5):
        raise ValueError('require exact fixed 0<theta<1/5')
    exponent = F(7, 9)+theta
    return exponent, 1-exponent


def source_multiplier(conductor, target, *, two_sign=1):
    """Exact 1+C/A by residue count and the MM Theorem1.4 product."""
    if type(target) is not int or target < 2 or target % 2:
        raise ValueError('positive even target required')
    chi = character_values(conductor, two_sign=two_sign)
    A = sum(bool(chi[v]) and bool(chi[(target-v) % conductor]) for v in range(conductor))
    B = sum(chi[v]*bool(chi[(target-v) % conductor]) for v in range(conductor))
    C = sum(chi[v]*chi[(target-v) % conductor] for v in range(conductor))
    if not A:
        raise ValueError('no conductor-unit pairs')
    factors = _factorization(conductor)
    two_power = next((e for p, e in factors if p == 2), 0)
    phi_two = 1 if two_power == 0 else 2**(two_power-1)
    local = F(0) if target % phi_two else F(chi[-1]*(-1)**(target//phi_two))
    for p, _ in factors:
        if p != 2 and target % p:
            local *= F(-1, p-2)
    return (A, B, C), 1+F(C, A), 1+local
