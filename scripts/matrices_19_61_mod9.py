#!/usr/bin/env python3
"""Native arithmetic wrapper and exact reference controls for the Z/9 experiment."""
import ast
import ctypes
import hashlib
import json
from pathlib import Path
import random

D=14
IDENTITY=bytes(int(i==j) for i in range(D) for j in range(D))


class Matrices:
    def __init__(self):
        path=Path('results/19.61-matrices-mod9.so').resolve()
        self.library=ctypes.CDLL(str(path));self.function=self.library.multiply_1961
        self.function.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_uint32]
        self.function.restype=ctypes.c_uint32
    def multiply(self,a,b,modulus=9):
        assert type(a) is bytes and type(b) is bytes and len(a)==len(b)==196
        out=ctypes.create_string_buffer(196)
        assert self.function(a,b,out,modulus)==0
        return out.raw


def roots_mod9():
    source=Path('results/19.61-g2-integral.grows')
    packet=json.loads(Path('results/19.61-g2-summary.json').read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==packet['sha256'][str(source)]
    roots,powers,adj,cartan=ast.literal_eval(source.read_text())
    assert cartan==[[2,-1],[-3,2]]
    powers=[[tuple(x for row in a for x in row) for a in rr] for rr in powers]
    matrices=[[bytes(sum(pow(t,k)*row[k][v] for k in range(len(row)))%9 for v in range(196))
               for t in range(9)] for row in powers]
    return roots,matrices


def python_multiply(a,b,p):
    return bytes(sum(a[D*i+k]*b[D*k+j] for k in range(D))%p for i in range(D) for j in range(D))


def controls():
    native=Matrices();roots,matrices=roots_mod9();rng=random.Random(196109);dense=0;laws=0
    for p in [3,9]:
        for _ in range(64):
            a=bytes(rng.randrange(p) for _ in range(196));b=bytes(rng.randrange(p) for _ in range(196))
            assert native.multiply(a,b,p)==python_multiply(a,b,p);dense+=1
        for row in matrices:
            rr=[bytes(x%p for x in row[t]) for t in range(p)]
            assert len(set(rr))==p
            for t in range(p):
                for u in range(p):
                    assert native.multiply(rr[t],rr[u],p)==python_multiply(rr[t],rr[u],p)==rr[(t+u)%p]
                    laws+=1
    return dict(dense_products=dense,root_group_laws=laws,
                source_sha256=hashlib.sha256(Path('scripts/matrices_19_61_mod9.c').read_bytes()).hexdigest(),
                library_sha256=hashlib.sha256(Path('results/19.61-matrices-mod9.so').read_bytes()).hexdigest())


if __name__=='__main__':
    result=controls();Path('results/19.61-mod9-native-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_1961_MOD9_NATIVE_CONTROLS',json.dumps(result,sort_keys=True))
