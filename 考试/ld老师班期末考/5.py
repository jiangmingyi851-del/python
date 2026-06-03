n=int(input())
ans=0
for i in range(1,n+1):
    if i%7==0 or '7'in str(i):
        continue
    ans+=i*i
print(ans)


