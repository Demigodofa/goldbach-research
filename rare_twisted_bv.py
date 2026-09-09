"""Relative distribution of the rare-sign prime weight and enlarged pruning.

Owner: Kevin's research. Purpose: control a further part of the unresolved
semiprime correlation by an averaged, rather than per-progression, estimate.
Finite helpers verify character cancellation, conductor fibres and the
small residue filter. They do not prove analytic estimates or detect zeros.

Sol checked the theory and actual files. Five focused exact tests passed
normally and with Python -O; these tests verify finite algebra only.

Deduction independently checked by Sol:
Keep the actual primitive quadratic character chi_D and zero beta from
multi_rare_partner.py, 24<D<=Y^(delta/4), 0<t=(1-beta)*L<=1/L, L=log(Y).
Choose the fixed delta sufficiently small for the fixed saving below, and set
  Q=floor(Y^(9/20)/D^3).
Then
  sum_{d<=Q} max_{(a,d)=1, I interval in[Y/2,Y]}
    |sum_{p in I, p=a mod d}log(p)*chi_D(p)
                      +integral_I v^(beta-1)dv/phi(d)| << Y*t/L^6. (1)
The principal resonance when D divides d is INCLUDED in the error budget,
not claimed absent. This fixes the saving at6 and chooses delta accordingly;
it does not assert every logarithmic saving with the same delta. Onsets and
constants are ineffective. The maximal interval statement is only in the bulk.

Sources, all three used with their actual conductor ranges:
* Bulk quantitative Linnik, deduced in relative_type_i.py from
  Thorner--Zaman Theorem2.1 and equation(4.2), including Y/2>=q^C and
  the log(1/e) gain in exp(-c*log(Y)/log(q)*log(1/e)). This replaces the
  earlier Tao exposition whose Proposition23 proof has an acknowledged gap.
  https://arxiv.org/html/2108.10878#S2
  https://arxiv.org/html/2108.10878#S4
* Grimmelt--Teravainen Lemma7.3(2): sum over ALL primitive characters
  up to R of corrected Lambda interval errors, divided by |I|+Y/R,
  is <<t*exp(-c*L/log(R)). Requires R>=exp(sqrt(L)) and an actual
  exceptional zero of level R and fixed quality.
  https://arxiv.org/html/2508.16400v2#S7.SS2
* Drappeau--Fiorilli Lemma2.1: for 2<=W<=H<=sqrt(Y), the induced-character
  mean above conductor W is <<L^C0*(Y/W+H*sqrt(Y)+Y^(5/6)).
  https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/tlm3.12030

Proof of (1):
1. Begin with Lambda. Orthogonality modulo d introduces characters psi;
   let r be their ORIGINAL primitive conductor and let
     tau=(chi_D*psi_r)^*
   be the primitive character inducing the product. Twisting by the fixed
   quadratic character is an involution on characters of the profinite unit
   group. In particular distinct primitive psi_r give distinct primitive tau,
   even when conductor factors cancel. Sorting induced characters gives
     sum_{d<=Q,r|d}1/phi(d)<<L/phi(r).
   Replacing induced values by primitive values costs O(Q*L^2) in total.
2. Set V=ceil(t^(-2)*L^16), W=ceil(D^2*t^(-2)*L^(C0+12)). Existing Siegel
   bounds imply V<=D^(1/4), W<=D^3, t=Y^(-o(1)), and D exceeds every
   fixed logarithmic power, eventually. For original r<=V, lift the product
   to lcm(D,r)<=D^(5/4). Choose delta once so quantitative Linnik supplies
   exponent at least28 throughout [Y/2,Y]. The principal projection vanishes
   since r<D; the exceptional projection is1 exactly for r=1. Thus the
   product-character interval sum has main -1_(r=1)*integral v^(beta-1)
   and error O(Y*(t^28+L^2/D)+L^2), without an extra totient factor.
   Summing the low original conductors costs
     O(Y*V*L*(t^28+L^2/D)+V*L^3+Q*L^2).
   After dividing by Y*t/L^6, the first term is t^25*L^23<=L^(-2);
   the second is O(t^(-3)*L^25/D)=o(1). The rest is power-small.
3. Next take original r>V but transformed conductor cond(tau)<=W. The
   inducer weight is at most C*L/sqrt(V), using phi(r)>=sqrt(r/2).
   Apply the aggregate Gallagher estimate at
     R=max(W,ceil(exp(sqrt(L))))<=Y^(1/7).
   It includes D, and beta has its required fixed quality eventually because
   (1-beta)*log(R)<=t/7. Multiplying the interval-normalized estimate by2Y
   bounds the unweighted sum of all corrected primitive errors by O(Y*t).
   Injectivity therefore bounds this middle range by
     O(Y*t*L/sqrt(V))=O(Y*t^2/L^7).
   The transformed exceptional character tau=chi_D would mean r=1, already
   treated. The transformed PRINCIPAL character means psi_r=chi_D, r=D;
   its main term costs at most Y*L/phi(D)=o(Y*t/L^6). This is the resonance
   retained in (1); it is not silently discarded by a false orthogonality claim.
   Discrete-main versus integral errors concern only these two characters.
4. For transformed conductor>W, set ell=lcm(D,d)<=D*Q. For each d,
   inflation followed by multiplication by chi_D injects its character group
   into characters modulo ell. Each ell has at most tau(D) preimages d,
   since ell/d divides D, and 1/phi(d)<=D/phi(ell). The induced-character
   source thus bounds this range by
     D*tau(D)*L^C0*(Y/W+(D*Q)*sqrt(Y)+Y^(5/6)).
   Since tau(D)<=D, these terms are at most
     Y*t^2/L^12 + Y^(19/20)*L^C0 + Y^(5/6+delta/2)*L^C0.
   All are o(Y*t/L^6). Also W<=D*Q<=sqrt(Y) for sufficiently small delta.
   Combining the three disjoint ranges proves the Lambda version. Passing
   to primes costs at most Q*sqrt(Y)*L^2<=Y^(19/20)*L^2, also harmless.

Application to the existing suppressed target m:
5. The condition that m-p be a unit modulo D is automatic for unit p except
   when 3|D and 3 does not divide m. In that case it is p=-m mod3. Put
   b=3 in this case and b=1 otherwise. Combine (1) with the previously proved
   ordinary relative BV estimate and the projector (1+chi_D(p))/2, using
   progression modulus b*e<=Q. For squarefree e coprime to Dm, its reduced
   CRT class has main X/phi(e), where
     X=1/(2*phi(b))*integral_J(1-v^(beta-1))dv.
   This equals the original X because A/phi(D)=1/phi(b). Other local prime
   divisors have zero density and zero actual prime count, as before. Hence
   for E*=floor(Q/3), the all-squarefree remainder budget is O(Y*t/L^6).
6. Let w*=floor(sqrt(E*)). Eventually w*>w. Upper sieve each positive-sign
   prime q in(w,w*] with level floor(E*/q), retaining the ORIGINAL cutoff z.
   Its ratio is at least log(sqrt(E*))/log(z)-o(1), a sufficiently large
   fixed constant. The same one-large-factor map (q,d)->q*d is injective
   across all q. From multi_rare_partner.py, sum_{q>w}1/q over q<=Y is O(t).
   The removed prime-log mass is therefore
     O(X*V_z*t+Y*t/L^6).
   Uniformly V_z<<S_2(m)/log(z), by the elementary Euler product. Multiplying
   by 2*log(Y) bounds the semiprime part of E_1 with q<=w* by
     O(Y*S_2(m)*t^2+Y*t/L^5)=o(Y*t).
   Thus for the SAME weighted total T (no change of its definition),
     T=P+E_1(q>w*)+o(Y*t),
   with a nonnegative discarded contribution. Positivity of T and control of
   the remaining semiprime correlation are both still unproved. No new
   actual prime-pair coverage, zero, numerical onset or historical novelty follows.
"""
from fractions import Fraction as F
from math import gcd, lcm

from exceptional_character_model import character_values
from major_arc_kernel import _factorization
from rare_prime_sieve import suppressed_residue_split


def twist_primitive_character(conductor: int, incoming: int = 1, *, two_sign: int = 1,
                              incoming_two_sign: int = 1
                              ) -> tuple[int, int, tuple[int, ...]]:
    """Return (common modulus, primitive conductor, primitive real values).

    Twist the supplied primitive REAL characters and remove induced zeros
    using values on units of the common modulus. incoming=1 is principal.
    This finite verifier caps each input at10000 and the common modulus at100000;
    the proof covers complex characters too, by group-theoretic injectivity.
    """
    if (type(conductor) is not int or not 3 <= conductor <= 10000
            or type(incoming) is not int or not 1 <= incoming <= 10000):
        raise ValueError("require 3<=conductor<=10000 and 1<=incoming<=10000")
    period = lcm(conductor, incoming)
    if period > 100000:
        raise ValueError("common modulus exceeds the finite verifier limit100000")
    fixed = character_values(conductor, two_sign=two_sign)
    if incoming == 1:
        if type(incoming_two_sign) is not int or incoming_two_sign != 1:
            raise ValueError("principal incoming character requires sign1")
        original = (1,)
    else:
        original = character_values(incoming, two_sign=incoming_two_sign)
    units = [(a, fixed[a % conductor]*original[a % incoming])
             for a in range(period) if gcd(a, period) == 1]
    divisors = [1]
    for prime, exponent in _factorization(period):
        divisors = [d*prime**power for d in divisors for power in range(exponent+1)]
    for candidate in sorted(divisors):
        residues = {}
        for a, value in units:
            residue = a % candidate
            if residue in residues and residues[residue] != value:
                break
            residues[residue] = value
        else:
            values = tuple(residues[a] if gcd(a, candidate) == 1 else 0
                           for a in range(candidate))
            return period, candidate, values
    raise RuntimeError("the common modulus must induce its own character")


def inflation_fibres(conductor: int, limit: int) -> tuple[tuple[int, tuple[int, ...]], ...]:
    """Group d<=limit by lcm(conductor,d); this is integer algebra, not a sieve bound."""
    if (type(conductor) is not int or not 1 <= conductor <= 1000
            or type(limit) is not int or not 1 <= limit <= 10000):
        raise ValueError("require 1<=conductor<=1000 and 1<=limit<=10000")
    fibres = {}
    for d in range(1, limit+1):
        fibres.setdefault(lcm(conductor, d), []).append(d)
    return tuple((ell, tuple(ds)) for ell, ds in sorted(fibres.items()))


def suppressed_prime_progression(conductor: int, target: int, *, two_sign: int = 1
                                 ) -> tuple[int, int, F]:
    """Return (b, residue modulo b, coefficient of integral(1-v^(beta-1))).

    Requires the existing finite suppression family. For unit first entries,
    only this modulus1 or3 filter is needed in addition to the sign+ projector.
    No beta, zero existence or actual prime-density assertion is an input.
    """
    proportion, _, _ = suppressed_residue_split(conductor, target, two_sign=two_sign)
    modulus = 3 if conductor % 3 == 0 and target % 3 else 1
    return modulus, (-target) % modulus, proportion/2
