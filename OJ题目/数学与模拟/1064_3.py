t=int(input())
for i in range(t):
    n,q=map(int,input().split())
    a=list(map(int,input().split()))
    a.sort()
    b=[]
    b0=0
    for i,j in enumerate(a):
        a1=bin(j)
        b.append(a1)
        b0^=j
    b0=bin(b0)
    for i in range(q):
        target=int(input())
        tar=bin(target)
        if tar==b0:
            print(0)
        else:
            
        


