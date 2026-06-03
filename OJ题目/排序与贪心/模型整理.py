from collections import defaultdict
class llm:
    def __init__(self,model):
        self.name,self.vol=model.split('-')
        self.num=int(self.vol[:-1]) if self.vol[:-1].isnumeric() else float(self.vol[:-1])
        self.unit=self.vol[-1]
    def __lt__(self, other):
        assert isinstance(other, llm)
        assert self.name==other.name
        if self.unit!=other.unit:
            return self.unit=='M'
        else:
            return self.num<other.num
dic=defaultdict(list)
n=int(input())
for i in range(n):
    model=input()
    lm=llm(model)
    dic[lm.name].append(lm)
l=sorted(dic.keys())
for name in l:
    v=sorted(dic[name])
    print(f'{name}: {", ".join([lm.vol for lm in v])}')



