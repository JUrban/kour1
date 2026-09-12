#!/usr/bin/env python3
"""Rebuild the wreath counterexample from elementary permutation arithmetic."""
import copy
from functools import lru_cache
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def product(x,y):
    return tuple(y[v-1] for v in x)


def inverse(x):
    out = [0]*len(x)
    for i,v in enumerate(x):out[v-1] = i+1
    return tuple(out)


@lru_cache(maxsize=None)
def closure(gens,degree):
    unit = tuple(range(1,degree+1)); seen = {unit}; todo = [unit]
    while todo:
        x = todo.pop()
        for y in gens:
            v = product(x,y)
            if v not in seen:seen.add(v);todo.append(v)
    return frozenset(seen)


def main():
    points = list(itertools.product(range(3),repeat=2)); pos = {p:i for i,p in enumerate(points)}
    quotient = set()
    for swap,sx,sy,tx,ty in itertools.product(range(2),[1,2],[1,2],range(3),range(3)):
        values = []
        for x,y in points:
            if swap:x,y=y,x
            values.append(pos[((sx*x+tx)%3,(sy*y+ty)%3)]+1)
        quotient.add(tuple(values))
    assert len(quotient) == 72
    unit9 = tuple(range(1,10)); unit18 = tuple(range(1,19))

    def lift(mask,q):
        return tuple(2*(q[i]-1)+(bit ^ (mask >> i & 1))+1 for i in range(9) for bit in range(2))

    full = frozenset(lift(mask,q) for mask in range(512) for q in quotient)
    base = frozenset(lift(mask,unit9) for mask in range(512))
    h = {q for q in quotient if q[0] == 1}
    a = frozenset(lift(mask,q) for mask in [0,1] for q in h)
    bs = [frozenset(g for g in full if g[2*i] == 2*i+1) for i in range(9)]
    assert len(full) == 36864 and len(base) == 512 and len(a) == 16
    assert all(len(b) == 2048 for b in bs) and len(set(bs)) == 9
    assert all(bs[i] == frozenset(g for g in full if g[2*i+1] == 2*i+2) for i in range(9))

    # Certify the needed quotient facts independently. A nontrivial normal
    # 2-subgroup would contain a nonidentity 2-element and its normal closure.
    two_elements = []; normal_closure_orders = []
    for x in quotient:
        if x == unit9:continue
        square = product(x,x)
        if product(square,square) == unit9:
            two_elements.append(x)
            conjugates = tuple(sorted({product(product(inverse(y),x),y) for y in quotient}))
            normal = closure(conjugates,9)
            assert len(normal) % 3 == 0
            normal_closure_orders.append(len(normal))
    assert two_elements
    # O2(Q)=1 follows, because the 2-part of |Q| is 8 and the displayed
    # signed affine group has no element of order eight.
    for x in quotient:
        if product(product(x,x),product(x,x)) == unit9:continue
        # Explicitly exclude order eight rather than assume it.
        x2=product(x,x);x4=product(x2,x2);assert product(x4,x4) != unit9

    flips = [lift(1 << i,unit9) for i in range(9)]
    centralizer = frozenset(g for g in full if all(product(g,z) == product(z,g) for z in flips))
    assert centralizer == base
    derived = frozenset(quotient); derived_orders = [len(derived)]
    while len(derived)>1:
        commutators = tuple(sorted({product(product(product(inverse(x),inverse(y)),x),y)
                                   for x in derived for y in derived}))
        new = closure(commutators,9);assert new != derived
        derived = new;derived_orders.append(len(derived))

    def validate(d):
        qe = list(map(tuple,d['q_elements']));ae = list(map(tuple,d['a_elements']))
        assert len(qe)==72 and set(qe)==quotient and len(ae)==16 and set(ae)==a
        qp={x:i for i,x in enumerate(qe)};ap={x:i for i,x in enumerate(ae)}
        assert d['q_table'] == [[qp[product(x,y)] for y in qe] for x in qe]
        assert d['a_table'] == [[ap[product(x,y)] for y in ae] for x in ae]
        assert d['orders'] == [36864,72,16,2048,512]
        generators = tuple(map(tuple,d['g_generators']))
        assert closure(generators,18) == full
        assert closure(tuple(map(tuple,d['b_generators'])),18) == bs[0]
        assert len(d['b_orbit_generators']) == 9 and d['b_orbit_orders'] == [2048]*9
        orbit_edges = 0
        for i,rows in enumerate(d['b_orbit_generators']):
            b_generators = tuple(map(tuple,rows))
            assert closure(b_generators,18) == bs[i]
            for g in generators:
                destination = (g[2*i]-1)//2
                assert all(product(product(inverse(g),x),g) in bs[destination] for x in b_generators)
                orbit_edges += 1
        # The orbit graph is complete: it is closed under the group generators,
        # and their action on the nine blocks is transitive.
        seen={0};todo=[0]
        while todo:
            i=todo.pop()
            for g in generators:
                j=(g[2*i]-1)//2
                if j not in seen:seen.add(j);todo.append(j)
        assert len(seen)==9
        encode=lambda k:sorted(ap[x] for x in k)
        norm=lambda f:sorted(encode(k) for k in f)
        table=[[a & u & v for v in bs] for u in bs]
        family=set().union(*(set(row) for row in table))
        minimal={k for k in family if not any(j<k for j in family)}
        smallest={k for k in family if len(k)==min(map(len,family))}
        assert d['a_meets_b']==[encode(a & b) for b in bs]
        assert d['pair_table']==[[encode(k) for k in row] for row in table]
        assert d['family']==norm(family) and d['minimal']==norm(minimal) and d['smallest']==norm(smallest)
        assert sorted(map(len,family))==[2,2,2,2,2,4,4,4,4,8]
        assert minimal==smallest and len(minimal)==5
        lower=closure(tuple(sorted(set().union(*smallest))),18)
        upper=closure(tuple(sorted(set().union(*minimal))),18)
        assert lower==upper==a and d['min']==encode(lower) and d['Min']==encode(upper)
        outside=table[0][1]
        assert len(outside)==2 and not outside<=base and d['outside']==encode(outside)
        return dict(family_orders=sorted(map(len,family)),pair_orders=sorted(len(k) for row in table for k in row),
                    orbit_generator_edges=orbit_edges,generator_count=len(generators))

    model=json.loads((ROOT/'results/20.122-minimum-native-model.json').read_text())
    checked=validate(model)
    corruptions={}
    d=copy.deepcopy(model);d['q_table'][0][0]=(d['q_table'][0][0]+1)%72;corruptions['wrong_quotient_product']=d
    d=copy.deepcopy(model);d['b_orbit_generators'].pop();corruptions['omitted_conjugate']=d
    d=copy.deepcopy(model);d['b_generators']=[list(unit18)];corruptions['wrong_point_stabilizer']=d
    d=copy.deepcopy(model);d['pair_table'][0][1]=[0];corruptions['invented_trivial_intersection']=d
    d=copy.deepcopy(model);d['outside']=[model['a_elements'].index(list(unit18)),model['a_elements'].index(list(flips[0]))]
    corruptions['inside_fitting_witness']=d
    d=copy.deepcopy(model);d['orders'][-1]=1024;corruptions['false_fitting_order']=d
    rejected=[]
    for name,d in corruptions.items():
        try:validate(d)
        except AssertionError:rejected.append(name)
        else:raise AssertionError(name)
    summary=dict(status='PASS',orders=model['orders'],quotient_products=72**2,a_products=16**2,
                 constructed_permutations=len(full),constructed_stabilizers=len(bs),stabilizer_orders=[len(b) for b in bs],
                 quotient_two_elements=len(two_elements),quotient_normal_closure_orders=sorted(normal_closure_orders),
                 quotient_derived_orders=derived_orders,centralizer_of_base_order=len(centralizer),
                 minimum_order=2,minimum_members=5,min_generated_order=16,Min_generated_order=16,
                 rejected_corruptions=rejected,**checked)
    (ROOT/'results/20.122-minimum-permutations-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True))
    print('PASS_20_122_MINIMUM_PERMUTATIONS rejected_corruptions=6')


if __name__=='__main__':main()
