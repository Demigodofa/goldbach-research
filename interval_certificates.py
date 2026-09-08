"""Certified sum intervals from counts of holes in two odd-integer intervals.

Certificate theorem: A and B contain only primes, lie in odd intervals of
lengths m,n, and together omit h of their interval positions. If h<min(m,n),
then A+B contains every even integer from a+c+2h through b+d-2h.
No individual Goldbach witness is used to derive the certificate.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json

from redistribution import sieve, trial_prime


@dataclass(frozen=True)
class OddInterval:
    first: int
    last: int
    prime_count: int

    @property
    def slots(self) -> int:
        return (self.last-self.first)//2 + 1

    @property
    def holes(self) -> int:
        return self.slots-self.prime_count

    def validate(self) -> None:
        if any(type(v) is not int for v in [self.first,self.last,self.prime_count]):
            raise ValueError("interval values and counts must be integers")
        if self.first < 3 or self.last < self.first or self.first%2 != 1 or self.last%2 != 1:
            raise ValueError("need nonempty odd interval beginning at least 3")
        if not 0 <= self.prime_count <= self.slots:
            raise ValueError("invalid prime count")


def count_interval(a: int, b: int, prime_flags: bytearray) -> OddInterval:
    z=OddInterval(a,b,sum(prime_flags[a:b+1:2]))
    z.validate()
    if b >= len(prime_flags):
        raise ValueError("prime table does not cover the interval")
    return z


def certify(a: OddInterval, b: OddInterval) -> dict:
    a.validate()
    b.validate()
    holes=a.holes+b.holes
    lower, upper=a.first+b.first+2*holes,a.last+b.last-2*holes
    sufficient=holes < min(a.slots,b.slots)
    return {"method":"two_interval_hole_bound", "left":asdict(a),
            "right":asdict(b), "left_slots":a.slots,"right_slots":b.slots,
            "total_holes":holes,"guarantee":sufficient,
            "covered_even_first":lower if sufficient else None,
            "covered_even_last":upper if sufficient else None,
            "covered_even_count":(upper-lower)//2+1 if sufficient else 0,
            "uniform_prime_pair_lower_bound":1 if sufficient else None,
            "proof":"each missing interval value destroys at most one candidate pair for a fixed sum; candidate count exceeds total holes throughout the certified interval",
            "on_failure":"inconclusive bound; no Goldbach counterexample claim"}


def check_certificate(z: dict, prime_flags: bytearray) -> None:
    verify_serialized(z,prime_flags)
    if not z["guarantee"]:
        return
    left=z["left"]
    right=z["right"]
    for n in range(z["covered_even_first"],z["covered_even_last"]+1,2):
        witnesses=[p for p in range(left["first"],left["last"]+1,2)
                   if right["first"] <= n-p <= right["last"]
                   and prime_flags[p] and prime_flags[n-p]]
        assert witnesses,(n,z)


def verify_serialized(z: dict,prime_flags: bytearray) -> dict:
    left=OddInterval(**z["left"])
    right=OddInterval(**z["right"])
    for interval in [left,right]:
        interval.validate()
        counted=count_interval(interval.first,interval.last,prime_flags)
        if counted!=interval:
            raise ValueError("serialized prime count does not match exact input data")
    expected=certify(left,right)
    if z!=expected:
        raise ValueError("serialized interval certificate metadata is inconsistent")
    return {"status":"passed","covered_even_count":z["covered_even_count"]}


def self_check() -> dict:
    # Exhaustively verify the general combinatorial theorem on arbitrary sets,
    # not just primes. This catches indexing and endpoint errors independently.
    cases=0
    for m in range(1,7):
        for n in range(1,7):
            for amask in range(1<<m):
                aset={i for i in range(m) if amask>>i&1}
                for bmask in range(1<<n):
                    bset={j for j in range(n) if bmask>>j&1}
                    h=m+n-len(aset)-len(bset)
                    if h < min(m,n):
                        sums={i+j for i in aset for j in bset}
                        assert all(t in sums for t in range(h,m+n-1-h))
                    cases+=1
    flags=sieve(1000)
    a=count_interval(3,13,flags)
    b=count_interval(3,7,flags)
    z=certify(a,b)
    assert (z["covered_even_first"],z["covered_even_last"])==(8,18)
    check_certificate(z,flags)
    assert all(bool(flags[n])==trial_prime(n) for n in range(1001))
    return {"status":"passed","arbitrary_set_cases":cases,
            "toy_certificate":z}


def demo() -> dict:
    flags=sieve(10001)
    examples=[]
    for a,b,c,d in [(3,13,3,7),(3,47,3,47),(3,113,3,113),
                      (3,2001,3,2001),(8001,10001,8001,10001)]:
        z=certify(count_interval(a,b,flags),count_interval(c,d,flags))
        check_certificate(z,flags)
        examples.append(z)
    return {"experiment":"span_certification_without_individual_witness_search",
            "certificates":examples}


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("mode",choices=["check","demo"])
    args=parser.parse_args()
    print(json.dumps(self_check() if args.mode=="check" else demo(),indent=2))


if __name__=="__main__":
    main()
