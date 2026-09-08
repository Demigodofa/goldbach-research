# A calculation that certifies an interval at once

Status: proved elementary counting lemma; numerical implementation has a
separate exhaustive combinatorial check. New-to-this-task only.
Purpose: implement Kevin's proposal to remove entire certified intervals from
the unresolved set and let later stages operate on the remaining gaps.

Let I={a,a+2,...,b} and J={c,c+2,...,d}, with odd endpoints at least3.
Let m=|I|, n=|J|. Suppose exactly alpha members of I and beta members of J
are known prime. Put h=(m-alpha)+(n-beta), the combined count of nonprimes.

**Theorem.** If h<min(m,n), every even integer N in

    a+c+2h <= N <= b+d-2h

is the sum of a prime in I and a prime in J.

**Proof.** Write N=a+c+2t. A candidate pair is uniquely specified by
`i+j=t`, where `0<=i<m`, `0<=j<n`. Its count is

    R(t)=max(0,min(m-1,t)-max(0,t-n+1)+1).

For h<=t<=m+n-2-h and h<min(m,n), this count is at least h+1.
Each nonprime position in I eliminates at most one candidate pair at that
fixed sum; each nonprime position in J also eliminates at most one. Thus at
most h candidates are spoiled. At least one pair is entirely prime. The
argument holds for every t in the displayed interval without selecting or
checking its individual witness. Double counting a spoiled pair only makes
the lower bound conservative. QED.

**Small worked certificate.** I={3,5,7,9,11,13} has five primes among six
slots. J={3,5,7} has three among three slots. Hence h=1<3. The theorem
certifies all six even integers 8,10,12,14,16,18 at once, with lower bound1.
Its inputs are the two intervals and their exact prime counts, not six
Goldbach decompositions.

**Composing certificates.** Store each certificate's inclusive even endpoints,
assumptions, proved lower bound, and source counts. Two intervals [L1,U1] and
[L2,U2] with L2<=U1+2 merge into one even interval [min(L1,L2),max(U1,U2)].
If L2>U1+2, preserve the gap [U1+2,L2-2]. This merge rule cannot fill an
uncertified gap. The union of finitely many certificates proves only that
finite union. A separate uniform statement for every N beyond a threshold
would convert a finite-prefix check into a proof of Goldbach.

**Limit.** The sufficient inequality may fail even when every sum is valid.
On larger prime intervals, the count of nonprime holes can overwhelm this
simple bound. Failure of the certificate is an unresolved interval, never a
counterexample. Next investigate whether residue restrictions or more precise
overlap bounds reduce the conservative hole count enough to certify larger
blocks. Keep all hypotheses and their quantifiers explicit.
