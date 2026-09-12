#!/usr/bin/env python3
"""Exhaustive native/Python agreement on every table of sizes two and three."""
import ctypes
import hashlib
import itertools
import json
from pathlib import Path


def load():
    library=ctypes.CDLL(str(Path('results/20.21-table-associativity.so').resolve()))
    function=library.table_associativity_2021
    function.argtypes=[ctypes.POINTER(ctypes.c_uint8),ctypes.c_uint32]
    function.restype=ctypes.c_uint64
    def check(data,n):
        assert len(data)==n*n
        buffer=(ctypes.c_uint8*len(data)).from_buffer_copy(bytes(data))
        return function(buffer,n)
    return check


def python_check(t,n):
    for a,b,c in itertools.product(range(n),repeat=3):
        if t[t[n*a+b]*n+c]!=t[n*a+t[n*b+c]]:return 1+(a*n+b)*n+c
    return 0


def run():
    native=load();reports=[]
    for n in [2,3]:
        tables=associative=0
        for table in itertools.product(range(n),repeat=n*n):
            a=native(table,n);b=python_check(table,n)
            assert a==b;(tables,associative)=(tables+1,associative+int(a==0))
        reports.append(dict(size=n,tables=tables,associative=associative))
    for n in [64,128,256]:
        table=[(a+b)%n for a in range(n) for b in range(n)]
        assert native(table,n)==python_check(table,n)==0
        table[n+1]=(table[n+1]+1)%n
        assert native(table,n)==python_check(table,n)!=0
    assert native([0,1,1,2],2)==2**64-1
    return dict(exhaustive=reports,large_sizes=[64,128,256],large_mutations=3,
                invalid_entry_rejected=True,source_sha256=hashlib.sha256(Path('scripts/table_associativity_20_21.c').read_bytes()).hexdigest(),
                library_sha256=hashlib.sha256(Path('results/20.21-table-associativity.so').read_bytes()).hexdigest())


if __name__=='__main__':
    result=run();Path('results/20.21-associativity-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_2021_NATIVE_ASSOCIATIVITY',json.dumps(result,sort_keys=True))
