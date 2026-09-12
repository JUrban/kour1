#!/usr/bin/env python3
"""Check the word and all R-module basis products using F3 matrices."""
import copy
import itertools
import json
from pathlib import Path
from check_21_76 import block, identity, mm, scalar


def verify(c):
    assert c['word'] == 'VUVuVUvuv'
    assert c['generators'] == dict(U=[1,1,0,1],u=[1,2,0,1],V=[1,0,4,1],v=[1,0,8,1])
    generators = {k:block(v) for k,v in c['generators'].items()}
    assert mm(generators['U'], generators['u']) == identity(4)
    assert mm(generators['V'], generators['v']) == identity(4)
    assert len(c['prefixes']) == 10 and block(c['prefixes'][0]) == identity(4)
    w = identity(4)
    for letter, expected in zip(c['word'], c['prefixes'][1:]):
        w = mm(w, generators[letter])
        assert w == block(expected)
    assert w == block([1,5,0,1])
    assert c['witness_parameter'] == 5 and c['original_upper_constants'] == [0,1,2] and c['beta'] == 4
    assert 5 not in c['original_upper_constants']
    return w


def run():
    c = json.loads(Path('results/19.48-word.json').read_text())
    verify(c)
    mutants = []
    d=copy.deepcopy(c); d['prefixes'][-1][1]=3; mutants.append(d)
    d=copy.deepcopy(c); d['generators']['v'][2]=4; mutants.append(d)
    d=copy.deepcopy(c); d['word']=d['word'][:-1]; mutants.append(d)
    for d in mutants:
        try:
            verify(d)
        except AssertionError:
            pass
        else:
            raise AssertionError('corrupted word was accepted')
    # Each monomial is (degree in t, field coefficient). These bases are
    # J=(t,jt), A=(1,jt), B=(1+j,t), as free F3[t]-modules.
    def basis(i,j):
        return [(0,1),(1,3)] if (i,j)==(0,1) else [(0,4),(1,1)] if (i,j)==(1,0) else [(1,1),(1,3)]
    def allowed(i,j,degree,value):
        if degree > 0:
            return True
        constants = [0,1,2] if (i,j)==(0,1) else [0,4,8] if (i,j)==(1,0) else [0]
        return value in [scalar(x) for x in constants]
    controls = 0
    for n in range(3,9):
        for i,k,j in itertools.permutations(range(n),3):
            for (a,x),(b,y) in itertools.product(basis(i,k),basis(k,j)):
                assert allowed(i,j,a+b,mm(scalar(x),scalar(y)))
                controls += 1
    # Bilinear multiplication makes basis controls sufficient for each
    # listed rank; the written ideal argument covers every rank.
    assert controls == 3024
    return dict(status='PASS',word_factors=9,prefixes=10,mutations_rejected=3,
                basis_product_controls=controls,ranks=list(range(3,9)),
                witness_parameter='2+j',R='F3[t]',K='F9(t)',extension_degree=2)


if __name__ == '__main__':
    r=run()
    Path('results/19.48-controls.json').write_text(json.dumps(r,indent=2)+'\n')
    print('PASS_1948_CONTROLS',json.dumps(r,sort_keys=True))
