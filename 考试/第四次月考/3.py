from functools import lru_cache
n=input()
@lru_cache(maxsize=None)
def fix(n):
    if len(n)<=2:
        return n
    else:
        l=len(n)
        r=(l-1)//2
        return fix(n[1:r+1])+n[0]+fix(n[r+1:])
print(fix(n))