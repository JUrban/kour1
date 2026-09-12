#!/usr/bin/env python3
"""Check the actual free-word identities without using GAP."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def product(*words):
    result=[]
    for word in words:
        for letter in word:
            if result and letter==-result[-1]:result.pop()
            else:result.append(letter)
    return tuple(result)


def inv(w):return tuple(-x for x in reversed(w))


def main():
    fixture=json.loads((ROOT/'results/20.124-fixture.json').read_text())
    images=[tuple(w) for w in fixture['images']];levels=fixture['levels']
    assert len(images)==len(levels)==76
    for level,w in zip(levels,images):
        assert product(w)==w and all(levels[abs(a)-1]<level for a in w)
        assert all(w.count(i)==w.count(-i) for i in range(1,77))
    def phi(w):return product(*(images[a-1] if a>0 else inv(images[-a-1]) for a in w))
    def iterates(w):
        out=[];v=phi(w)
        while v:
            out.append(v);v=phi(v)
            assert len(out)<=4
        return out
    def T(w):return product(w,*iterates(w))
    def D(w):return product(w,inv(phi(w)))
    def B(w):return product(*iterates(w))
    depths=set();maximum=0
    for w in fixture['words']:
        w=tuple(w);assert product(w)==w
        assert D(T(w))==w and T(D(w))==w and B(D(w))==phi(w)
        depths.add(len(iterates(w))+1);maximum=max(maximum,len(B(w)))
    for g,h in fixture['rbpairs']:
        bg=B(g);bh=B(h)
        assert product(bg,bh)==B(product(g,bg,h,inv(bg)))
    for i,w in fixture['image_witnesses']:
        assert images[i-1]==tuple(w)
        assert B(product([i],inv(w)))==tuple(w)
    rejected=[]
    for name,operation in [('reverse_factors',lambda w:product(*reversed(iterates(w)))),
                           ('truncate_after_first',phi)]:
        found=None
        for i in range(1,13):
            for j in range(1,13):
                g=(i,);h=(j,);bg=operation(g);bh=operation(h)
                if product(bg,bh)!=operation(product(g,bg,h,inv(bg))):
                    found=[i,j];break
            if found:break
        assert found is not None
        rejected.append(dict(mutation=name,witness=found))
    wrong_T=lambda w:product(w,*iterates(w)[:-1])
    assert D(wrong_T((7,)))!=(7,)
    rejected.append(dict(mutation='omit_last_inverse_factor',witness=[7]))
    assert phi(phi(phi(phi((13,)))))
    rejected.append(dict(mutation='uniform_four_iterate_termination',witness=[13]))
    assert any(levels[abs(a)-1]==3 for a in images[12])
    assert set(depths)=={1,2,3,4,5}
    summary=dict(status='PASS',generators=76,words=len(fixture['words']),
                 rbpairs=len(fixture['rbpairs']),image_witnesses=len(fixture['image_witnesses']),
                 depths=sorted(depths),maximum_output_length=maximum,rejected_mutations=rejected)
    print(json.dumps(summary,sort_keys=True));print('PASS_20_124_WORDS')


if __name__=='__main__':main()
