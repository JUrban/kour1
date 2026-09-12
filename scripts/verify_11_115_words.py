#!/usr/bin/env python3
"""Independent Schreier rewriting and semidirect normal-form controls."""
import copy
import hashlib
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
MODULI = [2,3,4,5,7,8,11]


def reduce(word):
    stack = []
    for x in word:
        assert isinstance(x, int) and x != 0
        if stack and stack[-1] == -x:
            stack.pop()
        else:
            stack.append(x)
    return tuple(stack)


def inverse(word):
    return tuple(-x for x in reversed(word))


def substitute(word, images):
    return reduce(x for letter in word for x in
                  (images[letter-1] if letter > 0 else inverse(images[-letter-1])))


def comm(u, v):
    return reduce(inverse(u)+inverse(v)+tuple(u)+tuple(v))


def model_check(model):
    m = model['m']
    assert m in MODULI and model['index'] == m and model['rank'] == m+1
    basis = [tuple(x) for x in model['basis']]
    forward = [tuple(x) for x in model['forward']]
    backward = [tuple(x) for x in model['backward']]
    assert basis == [(1,)*m]+[(1,)*i+(2,)+(-1,)*i for i in range(m)]
    assert len(forward) == len(backward) == m+1
    for i, word in enumerate(basis):
        assert substitute(forward[i],basis) == reduce((1,)+word+(-1,))
        assert substitute(backward[i],basis) == reduce((-1,)+word+(1,))
        assert substitute(forward[i],backward) == (i+1,)
        assert substitute(backward[i],forward) == (i+1,)
    for i in range(m):
        ci = comm((1,),(i+2,))
        target = comm((1,),(i+3,)) if i < m-1 else (1,)+comm((1,),(2,))+(-1,)
        assert substitute(ci,forward) == reduce(target)
    return basis


def rewrite(word, m):
    """Exact X normal form: original word = expand(output) * a^residue."""
    residue, out = 0, []
    for x in word:
        if x == 1:
            residue += 1
            if residue == m:
                out.append(1); residue = 0
        elif x == -1:
            residue -= 1
            if residue < 0:
                out.append(-1); residue = m-1
        else:
            assert abs(x) == 2
            out.append((residue+2)*(1 if x > 0 else -1))
    return reduce(out), residue


def normal_form(word, m):
    """In the quotient: normal form in F_m semidirect Z, with b_i indexed 1..m."""
    k, out = 0, []
    for x in word:
        if abs(x) == 1:
            k += x
        else:
            assert abs(x) == 2
            out.append((k % m+1)*(1 if x > 0 else -1))
    return reduce(out), k


def multiply(left, right, m):
    u, k = left; v, l = right
    shifted = tuple(((abs(x)-1+k) % m+1)*(1 if x > 0 else -1) for x in v)
    return reduce(u+shifted), k+l


def words(depth):
    yield ()
    level = [()]
    for _ in range(depth):
        level = [w+(x,) for w in level for x in [-2,-1,1,2] if not w or x != -w[-1]]
        yield from level


def main():
    models = [json.loads((ROOT/f'results/11.115-model-{m}.json').read_text()) for m in MODULI]
    rejected = []
    for name, change in [
        ('wrong_basis_power', lambda d: d['basis'][0].append(1)),
        ('omitted_wrap_conjugation', lambda d: d['forward'].__setitem__(-1,[2])),
        ('wrong_inverse', lambda d: d['backward'].__setitem__(1,[3])),
        ('wrong_index', lambda d: d.update(index=3)),
        ('wrong_rank', lambda d: d.update(rank=2)),
    ]:
        broken = copy.deepcopy(models[0]); change(broken)
        try:
            model_check(broken)
        except (AssertionError, IndexError):
            rejected.append(name)
        else:
            raise AssertionError('accepted '+name)
    exhaustive = list(words(8))
    assert len(exhaustive) == 13121
    rng = random.Random(11115)
    stats = dict(exhaustive_words=0, long_words=0, normal_form_products=0, associativity_triples=0)
    for model in models:
        m = model['m']; basis = model_check(model)
        samples = exhaustive + [reduce(rng.choice([-2,-1,1,2]) for _ in range(80)) for _ in range(1000)]
        for w in samples:
            t, residue = rewrite(w,m)
            assert reduce(substitute(t,basis)+(1,)*residue) == w
            free_word = reduce((abs(x)-1)*(1 if x>0 else -1) for x in t if abs(x)>1)
            power = m*sum(x for x in t if abs(x)==1)+residue
            assert normal_form(w,m) == (free_word,power)
        # Rewriting is inverse to substitution on each Schreier basis generator.
        for i, w in enumerate(basis):
            assert rewrite(w,m) == ((i+1,),0)
        for _ in range(1000):
            x,y,z = [rng.choice(samples) for _ in range(3)]
            nx,ny,nz = [normal_form(w,m) for w in [x,y,z]]
            assert multiply(nx,ny,m) == normal_form(reduce(x+y),m)
            assert multiply(multiply(nx,ny,m),nz,m) == multiply(nx,multiply(ny,nz,m),m)
            stats['normal_form_products'] += 1; stats['associativity_triples'] += 1
        stats['exhaustive_words'] += len(exhaustive); stats['long_words'] += 1000
    result = dict(status='PASS',moduli=MODULI,stats=stats,rejected_corruptions=rejected,
                  scope='Exact finite word controls for a separately proved infinite-subgroup counterexample.')
    (ROOT/'results/11.115-words-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
    print('PASS_11_115_WORDS models=7 rejected_corruptions=5')


if __name__ == '__main__':
    main()
