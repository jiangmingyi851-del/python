import sys
def min_length(s,l):
    num=0
    for i in s:
        n=min(i,l-i)
        num=max(num,n)
    return num
def max_length(s,l):
    num=0
    for i in s:
        n=max(i,l-i)
        num=max(num,n)
    return num
a=int(sys.stdin.readline().strip())
li=[]
for i in range(a):
    l,n=map(int,sys.stdin.readline().strip().split())
    s=list(map(int,sys.stdin.readline().strip().split()))
    if len(s)!=n:
        continue
    li.append((s,l))
for s,l in li:
    print(min_length(s,l),max_length(s,l))



