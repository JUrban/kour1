#!/usr/bin/env python3
"""Exact palindromic length in a free group, with a minimum factorization.

Input words use nonzero signed generator indices. The proof is in
research/16.9-proof.md. Time O(L^3), space O(L^2), for input length L.
"""
import argparse
import json


def free_reduce(word):
    out = []
    for a in word:
        if not isinstance(a, int) or a == 0:
            raise ValueError('free letters must be nonzero integers')
        if out and out[-1] == -a:
            out.pop()
        else:
            out.append(a)
    return out


def involution_reduce(word):
    out = []
    for a in word:
        if out and out[-1] == a:
            out.pop()
        else:
            out.append(a)
    return out


def encode(word):
    return [x for a in word for x in ([a, 0] if a > 0 else [0, -a])]


def decode_even(word):
    if len(word) % 2:
        raise ValueError('the involution word must have even parity')
    return free_reduce([a if i % 2 == 0 else -a
                        for i, a in enumerate(word) if a != 0])


def pairing_table(word):
    n = len(word)
    cost = [[0]*(n+1) for _ in range(n+1)]
    choice = [[-1]*(n+1) for _ in range(n+1)]
    for size in range(1, n+1):
        for i in range(n-size+1):
            j = i+size
            cost[i][j] = 1+cost[i+1][j]
            for k in range(i+1, j):
                if word[i] == word[k]:
                    candidate = cost[i+1][k]+cost[k+1][j]
                    if candidate < cost[i][j]:
                        cost[i][j] = candidate
                        choice[i][j] = k
    return cost, choice


def deletion_positions(choice, start, end):
    deleted = []
    pending = [(start, end)]
    while pending:
        i, j = pending.pop()
        if i == j:
            continue
        k = choice[i][j]
        if k == -1:
            deleted.append(i)
            pending.append((i+1, j))
        else:
            pending.extend([(k+1, j), (i+1, k)])
    return sorted(deleted)


def palindromic_factorization(word):
    word = free_reduce(word)
    encoded = encode(word)
    extended = encoded+[0]
    cost, choice = pairing_table(extended)
    even, odd = cost[0][len(encoded)], cost[0][len(extended)]
    parity = int(odd < even)
    target = extended if parity else encoded
    removed = set(deletion_positions(choice, 0, len(target)))
    prefix, factors = [], []
    for i, a in enumerate(target):
        if i in removed:
            reflection = prefix+[a]+prefix[::-1]
            p = decode_even(reflection+[0])
            if len(factors) % 2:
                p = [-x for x in p]
            factors.append(p)
        else:
            if prefix and prefix[-1] == a:
                prefix.pop()
            else:
                prefix.append(a)
    assert not prefix
    return dict(word=word, length=min(even, odd), reflection_lengths=[even, odd],
                involution_endpoint_parity=parity,
                deletion_positions=sorted(removed), palindromes=factors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('word', nargs='*', type=int)
    args = parser.parse_args()
    print(json.dumps(palindromic_factorization(args.word), indent=2))
