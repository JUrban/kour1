#!/usr/bin/env python3
"""Independent code-intersection and quaternion controls for 21.121(a)."""
from itertools import product
import json


def codewords(k):
    return [tuple((a & v).bit_count() % 2 for v in range(1, 2**k))
            for a in range(2**k)]


def partitions_with_zero(n):
    # Restricted-growth strings for set partitions of {dummy,1,...,n};
    # the block containing dummy has label zero and is the unused support.
    def extend(labels, maximum):
        if len(labels) == n:
            yield tuple(labels)
            return
        for label in range(maximum + 2):
            yield from extend(labels + [label], max(maximum, label))
    yield from extend([], 0)


def in_disjoint_support_span(word, labels):
    entries = {0: 0}
    for bit, label in zip(word, labels):
        if label in entries and entries[label] != bit:
            return False
        entries[label] = bit
    return True


def quaternion_multiply(a, b):
    # Low two bits encode 1,i,j,k; the high bit encodes a minus sign.
    x, y = a & 3, b & 3
    negative = int((x == y and x != 0) or (x, y) in {(2, 1), (3, 2), (1, 3)})
    return (x ^ y) | ((((a >> 2) ^ (b >> 2) ^ negative) & 1) << 2)


def inverse(a):
    return a ^ 4 if a & 3 else a


def automorphism(a):
    return (a & 4) | {0: 0, 1: 2, 2: 3, 3: 1}[a & 3]


def commutator(a, b):
    value = 0
    for term in (inverse(a), inverse(b), a, b):
        value = quaternion_multiply(value, term)
    return value


def main():
    rows = []
    for k in range(1, 4):
        words = codewords(k)
        assert len(set(words)) == 2**k
        assert all(sum(w) == 2**(k-1) for w in words[1:])
        checked = 0
        for labels in partitions_with_zero(2**k - 1):
            r = max(labels, default=0)
            intersection_size = sum(in_disjoint_support_span(w, labels) for w in words)
            assert intersection_size > 0 and intersection_size & (intersection_size - 1) == 0
            assert intersection_size <= r + 1, (k, labels, intersection_size)
            checked += 1
        rows.append({'k': k, 'disjoint_support_spaces': checked})
    # Verify the quaternion implementation is associative and the displayed
    # order-three map is an automorphism, before checking commutators.
    for a, b, c in product(range(8), repeat=3):
        assert quaternion_multiply(quaternion_multiply(a, b), c) == quaternion_multiply(a, quaternion_multiply(b, c))
    for a, b in product(range(8), repeat=2):
        assert automorphism(quaternion_multiply(a, b)) == quaternion_multiply(automorphism(a), automorphism(b))
    for a in range(8):
        assert quaternion_multiply(a, inverse(a)) == 0
        assert automorphism(automorphism(automorphism(a))) == a
        expected = 4 if a & 3 else 0
        assert commutator(a, automorphism(a)) == expected
        assert commutator(a, automorphism(automorphism(a))) == expected
    print(json.dumps({'result': 'PASS', 'code_lemma': rows,
                      'quaternion_associativity_triples': 512,
                      'automorphism_product_pairs': 64,
                      'quaternion_commutator_checks': 16}, sort_keys=True))


if __name__ == '__main__':
    main()
