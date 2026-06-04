
n=int(input())
MOD=998244353
for i in range(n):
    t=int(input())
    l1=list(map(int,input().split()))
    freq=[0]*(t)
    for j in range(t):
        freq[l1[j]-1]+=1
    b=[f for f in freq if f!=0]
    b.sort(reverse=True)
    ans=1
    for j in b:
        ans*=j+1
    lim=b[0]
    f=[0]*(lim)
    f[0]=1
    for v in b:
        if v==lim:
            continue
        g=f[:]
        for j in range(v,lim):
            g[j]=g[j]+v*f[j-v]
        f=g[:]
    ans=((ans-sum(f))%MOD)
    print(ans)
    


    

                


            



