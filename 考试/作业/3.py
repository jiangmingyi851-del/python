visited=[False]*1001
visited[1]=True
prime=[]
for i in range(2,1001):
    if not visited[i]:
        prime.append(i)
        for j in range(i*i,1001,i):
            visited[j]=True
a,b=map(int,input().split())
k=min(a,b)
count=[]
for i in prime:
    if i>k:
        break
    if a%i==0 and b%i==0:
        num=1
        while a%i==0 and b%i==0:
            num+=1
            a//=i
            b//=i
        count.append(num)
    if a==1 or b==1:
        break
ans=1
for i in count:
    ans*=i
print(ans)
        
