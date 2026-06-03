m,n=map(int,input().split())
ans=0
index=-1
for i in range(m):
    li=list(map(int,input().split()))
    s=sum(li)
    if s>ans:
        ans=s
        index=i
print(index)
print(ans)
    
    