"""Small exact row spaces over F3, using sparse elimination rows."""


class Space:
    def __init__(self,rows=()):
        self.rows={};self.sparse={}
        for row in rows:self.add(row)
    def reduce(self,row):
        v=list(row)
        for i in sorted(self.rows):
            c=v[i]
            if c:
                for j,x in self.sparse[i]:v[j]=(v[j]-c*x)%3
        return v
    def add(self,row):
        v=self.reduce(row)
        if not any(v):return None
        i=next(i for i,x in enumerate(v) if x)
        if v[i]==2:v=[2*x%3 for x in v]
        row=bytes(v);self.rows[i]=row;self.sparse[i]=[(j,x) for j,x in enumerate(row) if x]
        return row
    def contains(self,row):return not any(self.reduce(row))
    def basis(self):return [self.rows[i] for i in sorted(self.rows)]
    def rank(self):return len(self.rows)
